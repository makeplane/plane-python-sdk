"""Offline coverage for project/workspace automations: CRUD, the `set_status` custom
action (204, no body), and the `edges`/`nodes`/`activities` children -- including
`nodes.regenerate_webhook_secret`, which answers with a different model
(`AutomationWebhookSecret`, not `AutomationNode`). Asserts every method's exact
request URL. Project-scoped resources are depth 3 (`slug, project, automation`);
workspace-scoped ones are depth 2 (`slug, automation`)."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.automations import (
    ProjectAutomationActivities,
    ProjectAutomationEdges,
    ProjectAutomationNodes,
    ProjectAutomations,
    WorkspaceAutomationActivities,
    WorkspaceAutomationEdges,
    WorkspaceAutomationNodes,
    WorkspaceAutomations,
)
from plane.config import Configuration
from plane.models.v2.automations import (
    CreateAutomation,
    CreateAutomationEdge,
    CreateAutomationNode,
    UpdateAutomation,
    UpdateAutomationEdge,
    UpdateAutomationNode,
)

PROJECT_BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/automations"
WORKSPACE_BASE = "https://api.example.com/api/v2/workspaces/acme/automations"


@pytest.fixture
def project_automations(config: Configuration) -> ProjectAutomations:
    return ProjectAutomations(V2Transport(config))


@pytest.fixture
def workspace_automations(config: Configuration) -> WorkspaceAutomations:
    return WorkspaceAutomations(V2Transport(config))


def test_project_automations_attaches_its_children(
    project_automations: ProjectAutomations,
) -> None:
    assert isinstance(project_automations.edges, ProjectAutomationEdges)
    assert isinstance(project_automations.nodes, ProjectAutomationNodes)
    assert isinstance(project_automations.activities, ProjectAutomationActivities)


def test_workspace_automations_attaches_its_children(
    workspace_automations: WorkspaceAutomations,
) -> None:
    assert isinstance(workspace_automations.edges, WorkspaceAutomationEdges)
    assert isinstance(workspace_automations.nodes, WorkspaceAutomationNodes)
    assert isinstance(workspace_automations.activities, WorkspaceAutomationActivities)


# -- Project-scoped CRUD --------------------------------------------------------


@responses.activate
def test_project_list(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "a1", "name": "Auto-close stale", "scope": "WorkItem"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = project_automations.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].scope == "WorkItem"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/"


@responses.activate
def test_project_list_passes_filters_and_pagination(
    project_automations: ProjectAutomations,
) -> None:
    responses.get(f"{PROJECT_BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    project_automations.list(
        "acme", "ENG", is_enabled=True, status="published", per_page=25, offset=50
    )

    query = responses.calls[0].request.url
    assert "is_enabled=True" in query
    assert "status=published" in query
    assert "per_page=25" in query
    assert "offset=50" in query


def test_project_list_rejects_unknown_field_before_the_request(
    project_automations: ProjectAutomations,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        project_automations.list("acme", "ENG", fields=["bogus"])


@responses.activate
def test_sparse_response_leaves_absent_fields_unreadable(
    project_automations: ProjectAutomations,
) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={"data": [{"id": "a1"}], "pagination": {"style": "offset"}},
    )

    page = project_automations.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "a1"
    with pytest.raises(Exception, match="not available"):
        _ = page.data[0].name


@responses.activate
def test_project_retrieve(project_automations: ProjectAutomations) -> None:
    responses.get(f"{PROJECT_BASE}/a1/", json={"id": "a1", "name": "Auto-close stale"})

    row = project_automations.retrieve("acme", "ENG", "a1")

    assert row.id == "a1"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/a1/"


@responses.activate
def test_project_find_by_name(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "a1", "name": "Auto-close stale"}],
            "pagination": {"style": "offset"},
        },
    )

    assert project_automations.find_by_name("acme", "ENG", "Auto-close stale").id == "a1"


@responses.activate
def test_project_create_sends_shell_fields_only(project_automations: ProjectAutomations) -> None:
    responses.post(f"{PROJECT_BASE}/", json={"id": "a1", "name": "New"}, status=201)

    project_automations.create(
        "acme", "ENG", CreateAutomation(name="New", scope="WorkItem", description="desc")
    )

    body = json.loads(responses.calls[0].request.body)
    assert body == {"name": "New", "scope": "WorkItem", "description": "desc"}
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/"


@responses.activate
def test_project_update_uses_patch(project_automations: ProjectAutomations) -> None:
    responses.patch(f"{PROJECT_BASE}/a1/", json={"id": "a1", "name": "Renamed"})

    updated = project_automations.update("acme", "ENG", "a1", UpdateAutomation(name="Renamed"))

    assert updated.name == "Renamed"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/a1/"


@responses.activate
def test_project_delete_returns_none(project_automations: ProjectAutomations) -> None:
    responses.delete(f"{PROJECT_BASE}/a1/", status=204)

    assert project_automations.delete("acme", "ENG", "a1") is None
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/a1/"


@responses.activate
def test_project_set_status_posts_body_and_returns_none(
    project_automations: ProjectAutomations,
) -> None:
    """204 no body -- distinct from `_action`, which always parses a row. Goes
    through the kernel's `_void_action`, not a hand-built URL."""
    responses.post(f"{PROJECT_BASE}/a1/status/", status=204)

    result = project_automations.set_status("acme", "ENG", "a1", is_enabled=True)

    assert result is None
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/a1/status/"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"is_enabled": True}


# -- Workspace-scoped CRUD -------------------------------------------------------


@responses.activate
def test_workspace_list_hits_the_workspace_level_path_not_the_project_one(
    workspace_automations: WorkspaceAutomations,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={"data": [{"id": "a2"}], "pagination": {"style": "offset"}},
    )

    page = workspace_automations.list("acme")

    assert page.data[0].id == "a2"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/"


@responses.activate
def test_workspace_create(workspace_automations: WorkspaceAutomations) -> None:
    responses.post(f"{WORKSPACE_BASE}/", json={"id": "a2", "name": "Global"}, status=201)

    created = workspace_automations.create("acme", CreateAutomation(name="Global", scope="Cycle"))

    assert created.id == "a2"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/"


@responses.activate
def test_workspace_set_status(workspace_automations: WorkspaceAutomations) -> None:
    responses.post(f"{WORKSPACE_BASE}/a2/status/", status=204)

    assert workspace_automations.set_status("acme", "a2", is_enabled=False) is None
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/a2/status/"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"is_enabled": False}


# -- Navigation: a fetched automation reaches its children (edges, nodes,
# activities) -- see tests/v2/test_loaded_automations.py.


# -- Sub-resources: edges ---------------------------------------------------------


@responses.activate
def test_project_edges_crud(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/edges/",
        json={
            "data": [{"id": "e1", "source_node_id": "n1", "target_node_id": "n2"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{PROJECT_BASE}/a1/edges/",
        json={"id": "e1", "source_node_id": "n1", "target_node_id": "n2"},
        status=201,
    )
    responses.get(f"{PROJECT_BASE}/a1/edges/e1/", json={"id": "e1"})
    responses.patch(f"{PROJECT_BASE}/a1/edges/e1/", json={"id": "e1", "execution_order": 2})
    responses.delete(f"{PROJECT_BASE}/a1/edges/e1/", status=204)

    page = project_automations.edges.list("acme", "ENG", "a1")
    assert page.data[0].id == "e1"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/a1/edges/"

    created = project_automations.edges.create(
        "acme", "ENG", "a1", CreateAutomationEdge(source_node_id="n1", target_node_id="n2")
    )
    assert created.id == "e1"
    assert responses.calls[1].request.url == f"{PROJECT_BASE}/a1/edges/"

    fetched = project_automations.edges.retrieve("acme", "ENG", "a1", "e1")
    assert fetched.id == "e1"
    assert responses.calls[2].request.url == f"{PROJECT_BASE}/a1/edges/e1/"

    updated = project_automations.edges.update(
        "acme", "ENG", "a1", "e1", UpdateAutomationEdge(execution_order=2)
    )
    assert updated.execution_order == 2
    assert responses.calls[3].request.url == f"{PROJECT_BASE}/a1/edges/e1/"

    assert project_automations.edges.delete("acme", "ENG", "a1", "e1") is None
    assert responses.calls[4].request.url == f"{PROJECT_BASE}/a1/edges/e1/"


@responses.activate
def test_workspace_edges_create_hits_the_workspace_level_path(
    workspace_automations: WorkspaceAutomations,
) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/a2/edges/",
        json={"id": "e2", "source_node_id": "n3", "target_node_id": "n4"},
        status=201,
    )

    created = workspace_automations.edges.create(
        "acme", "a2", CreateAutomationEdge(source_node_id="n3", target_node_id="n4")
    )

    assert created.id == "e2"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/a2/edges/"


@responses.activate
def test_edges_list_passes_node_filters_and_order_by(
    project_automations: ProjectAutomations,
) -> None:
    responses.get(f"{PROJECT_BASE}/a1/edges/", json={"data": [], "pagination": {"style": "offset"}})

    project_automations.edges.list("acme", "ENG", "a1", source_node_id="n1", order_by="id")

    query = responses.calls[0].request.url
    assert "source_node_id=n1" in query
    assert "order_by=id" in query


# -- Sub-resources: nodes (+ regenerate_webhook_secret) --------------------------


@responses.activate
def test_project_nodes_crud(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/nodes/",
        json={
            "data": [{"id": "n1", "name": "On create", "node_type": "trigger"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{PROJECT_BASE}/a1/nodes/",
        json={"id": "n1", "name": "On create", "node_type": "trigger"},
        status=201,
    )
    responses.get(f"{PROJECT_BASE}/a1/nodes/n1/", json={"id": "n1"})
    responses.patch(f"{PROJECT_BASE}/a1/nodes/n1/", json={"id": "n1", "is_enabled": False})
    responses.delete(f"{PROJECT_BASE}/a1/nodes/n1/", status=204)

    page = project_automations.nodes.list("acme", "ENG", "a1")
    assert page.data[0].node_type == "trigger"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/a1/nodes/"

    created = project_automations.nodes.create(
        "acme",
        "ENG",
        "a1",
        CreateAutomationNode(handler_name="record_created", name="On create", node_type="trigger"),
    )
    assert created.id == "n1"
    assert responses.calls[1].request.url == f"{PROJECT_BASE}/a1/nodes/"

    fetched = project_automations.nodes.retrieve("acme", "ENG", "a1", "n1")
    assert fetched.id == "n1"
    assert responses.calls[2].request.url == f"{PROJECT_BASE}/a1/nodes/n1/"

    updated = project_automations.nodes.update(
        "acme", "ENG", "a1", "n1", UpdateAutomationNode(is_enabled=False)
    )
    assert updated.is_enabled is False
    assert responses.calls[3].request.url == f"{PROJECT_BASE}/a1/nodes/n1/"

    assert project_automations.nodes.delete("acme", "ENG", "a1", "n1") is None
    assert responses.calls[4].request.url == f"{PROJECT_BASE}/a1/nodes/n1/"


@responses.activate
def test_project_nodes_find_by_name(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/nodes/",
        json={"data": [{"id": "n1", "name": "On create"}], "pagination": {"style": "offset"}},
    )

    assert project_automations.nodes.find_by_name("acme", "ENG", "a1", "On create").id == "n1"


@responses.activate
def test_project_regenerate_webhook_secret_returns_a_different_model_than_the_resource(
    project_automations: ProjectAutomations,
) -> None:
    """Not `_action`: the response is `AutomationWebhookSecret`, not `AutomationNode`.
    Goes through the kernel's `_custom_action`, not a hand-built URL."""
    responses.post(
        f"{PROJECT_BASE}/a1/nodes/n1/regenerate-webhook-secret/", json={"secret": "whsec_abc"}
    )

    result = project_automations.nodes.regenerate_webhook_secret("acme", "ENG", "a1", "n1")

    assert result.secret == "whsec_abc"
    assert (
        responses.calls[0].request.url == f"{PROJECT_BASE}/a1/nodes/n1/regenerate-webhook-secret/"
    )


@responses.activate
def test_workspace_regenerate_webhook_secret_hits_the_workspace_level_path(
    workspace_automations: WorkspaceAutomations,
) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/a2/nodes/n2/regenerate-webhook-secret/", json={"secret": "whsec_xyz"}
    )

    result = workspace_automations.nodes.regenerate_webhook_secret("acme", "a2", "n2")

    assert result.secret == "whsec_xyz"
    assert (
        responses.calls[0].request.url == f"{WORKSPACE_BASE}/a2/nodes/n2/regenerate-webhook-secret/"
    )


# -- Sub-resources: activities (read-only) ----------------------------------------


@responses.activate
def test_project_activities_are_read_only(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/activities/",
        json={"data": [{"id": "act1", "verb": "triggered"}], "pagination": {"style": "offset"}},
    )
    responses.get(f"{PROJECT_BASE}/a1/activities/act1/", json={"id": "act1", "verb": "triggered"})

    page = project_automations.activities.list("acme", "ENG", "a1")
    assert page.data[0].verb == "triggered"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/a1/activities/"

    fetched = project_automations.activities.retrieve("acme", "ENG", "a1", "act1")
    assert fetched.id == "act1"
    assert responses.calls[1].request.url == f"{PROJECT_BASE}/a1/activities/act1/"

    assert project_automations.activities.operations == {
        "list": "project_automation_activities_list",
        "retrieve": "project_automation_activities_retrieve",
    }


@responses.activate
def test_workspace_activities_hit_the_workspace_level_path(
    workspace_automations: WorkspaceAutomations,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/a2/activities/",
        json={"data": [{"id": "act2"}], "pagination": {"style": "offset"}},
    )

    page = workspace_automations.activities.list("acme", "a2")

    assert page.data[0].id == "act2"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/a2/activities/"


@responses.activate
def test_activities_pass_verb_filter(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/activities/", json={"data": [], "pagination": {"style": "offset"}}
    )

    project_automations.activities.list("acme", "ENG", "a1", verb="triggered")

    assert "verb=triggered" in responses.calls[0].request.url
