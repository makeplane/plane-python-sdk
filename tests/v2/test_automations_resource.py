"""Offline coverage for project/workspace automations; covers a 204-no-body custom action
(`set_status`) and one returning a different model (`regenerate_webhook_secret`)."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.automations import ProjectAutomations, WorkspaceAutomations
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
    return ProjectAutomations(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_automations(config: Configuration) -> WorkspaceAutomations:
    return WorkspaceAutomations(V2Transport(config), slug="acme")


def test_project_automations_forward_scope_to_sub_resources(
    project_automations: ProjectAutomations,
) -> None:
    scope = {"slug": "acme", "project_id": "ENG"}
    assert project_automations.edges._scope == scope
    assert project_automations.nodes._scope == scope
    assert project_automations.activities._scope == scope


def test_workspace_automations_forward_scope_to_sub_resources(
    workspace_automations: WorkspaceAutomations,
) -> None:
    scope = {"slug": "acme"}
    assert workspace_automations.edges._scope == scope
    assert workspace_automations.nodes._scope == scope
    assert workspace_automations.activities._scope == scope


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

    page = project_automations.list()

    assert page.total_count == 1
    assert page.data[0].scope == "WorkItem"


@responses.activate
def test_project_list_passes_filters(project_automations: ProjectAutomations) -> None:
    responses.get(f"{PROJECT_BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    project_automations.list(is_enabled=True, status="published")

    query = responses.calls[0].request.url
    assert "is_enabled=True" in query
    assert "status=published" in query


def test_project_list_rejects_unknown_field_before_the_request(
    project_automations: ProjectAutomations,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        project_automations.list(fields=["bogus"])


@responses.activate
def test_sparse_response_leaves_absent_fields_none(
    project_automations: ProjectAutomations,
) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={"data": [{"id": "a1"}], "pagination": {"style": "offset"}},
    )

    page = project_automations.list(fields=["id"])

    assert page.data[0].id == "a1"
    assert page.data[0].name is None
    assert page.data[0].status is None


@responses.activate
def test_project_retrieve(project_automations: ProjectAutomations) -> None:
    responses.get(f"{PROJECT_BASE}/a1/", json={"id": "a1", "name": "Auto-close stale"})

    row = project_automations.retrieve("a1")

    assert row.id == "a1"


@responses.activate
def test_project_find_by_name(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "a1", "name": "Auto-close stale"}],
            "pagination": {"style": "offset"},
        },
    )

    assert project_automations.find_by_name("Auto-close stale").id == "a1"


@responses.activate
def test_project_create_sends_shell_fields_only(project_automations: ProjectAutomations) -> None:
    responses.post(f"{PROJECT_BASE}/", json={"id": "a1", "name": "New"}, status=201)

    project_automations.create(CreateAutomation(name="New", scope="WorkItem", description="desc"))

    body = json.loads(responses.calls[0].request.body)
    assert body == {"name": "New", "scope": "WorkItem", "description": "desc"}


@responses.activate
def test_project_update_uses_patch(project_automations: ProjectAutomations) -> None:
    responses.patch(f"{PROJECT_BASE}/a1/", json={"id": "a1", "name": "Renamed"})

    updated = project_automations.update("a1", UpdateAutomation(name="Renamed"))

    assert updated.name == "Renamed"


@responses.activate
def test_project_delete_returns_none(project_automations: ProjectAutomations) -> None:
    responses.delete(f"{PROJECT_BASE}/a1/", status=204)

    assert project_automations.delete("a1") is None


@responses.activate
def test_project_set_status_posts_body_and_returns_none(
    project_automations: ProjectAutomations,
) -> None:
    """204 no body -- distinct from `_action`, which always parses a row."""
    responses.post(f"{PROJECT_BASE}/a1/status/", status=204)

    result = project_automations.set_status("a1", is_enabled=True)

    assert result is None
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

    page = workspace_automations.list()

    assert page.data[0].id == "a2"
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_workspace_create(workspace_automations: WorkspaceAutomations) -> None:
    responses.post(f"{WORKSPACE_BASE}/", json={"id": "a2", "name": "Global"}, status=201)

    created = workspace_automations.create(CreateAutomation(name="Global", scope="Cycle"))

    assert created.id == "a2"


@responses.activate
def test_workspace_set_status(workspace_automations: WorkspaceAutomations) -> None:
    responses.post(f"{WORKSPACE_BASE}/a2/status/", status=204)

    assert workspace_automations.set_status("a2", is_enabled=False) is None
    body = json.loads(responses.calls[0].request.body)
    assert body == {"is_enabled": False}


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

    page = project_automations.edges.list("a1")
    assert page.data[0].id == "e1"

    created = project_automations.edges.create(
        "a1", CreateAutomationEdge(source_node_id="n1", target_node_id="n2")
    )
    assert created.id == "e1"

    fetched = project_automations.edges.retrieve("a1", "e1")
    assert fetched.id == "e1"

    updated = project_automations.edges.update(
        "a1", "e1", UpdateAutomationEdge(execution_order=2)
    )
    assert updated.execution_order == 2

    assert project_automations.edges.delete("a1", "e1") is None


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
        "a2", CreateAutomationEdge(source_node_id="n3", target_node_id="n4")
    )

    assert created.id == "e2"
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_edges_list_passes_node_filters(project_automations: ProjectAutomations) -> None:
    responses.get(f"{PROJECT_BASE}/a1/edges/", json={"data": [], "pagination": {"style": "offset"}})

    project_automations.edges.list("a1", source_node_id="n1")

    assert "source_node_id=n1" in responses.calls[0].request.url


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

    page = project_automations.nodes.list("a1")
    assert page.data[0].node_type == "trigger"

    created = project_automations.nodes.create(
        "a1",
        CreateAutomationNode(handler_name="record_created", name="On create", node_type="trigger"),
    )
    assert created.id == "n1"

    fetched = project_automations.nodes.retrieve("a1", "n1")
    assert fetched.id == "n1"

    updated = project_automations.nodes.update("a1", "n1", UpdateAutomationNode(is_enabled=False))
    assert updated.is_enabled is False

    assert project_automations.nodes.delete("a1", "n1") is None


@responses.activate
def test_project_nodes_find_by_name(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/nodes/",
        json={"data": [{"id": "n1", "name": "On create"}], "pagination": {"style": "offset"}},
    )

    assert project_automations.nodes.find_by_name("a1", "On create").id == "n1"


@responses.activate
def test_project_regenerate_webhook_secret_returns_a_different_model_than_the_resource(
    project_automations: ProjectAutomations,
) -> None:
    """Not `_action`: the response is `AutomationWebhookSecret`, not `AutomationNode`."""
    responses.post(
        f"{PROJECT_BASE}/a1/nodes/n1/regenerate-webhook-secret/", json={"secret": "whsec_abc"}
    )

    result = project_automations.nodes.regenerate_webhook_secret("a1", "n1")

    assert result.secret == "whsec_abc"


@responses.activate
def test_workspace_regenerate_webhook_secret_hits_the_workspace_level_path(
    workspace_automations: WorkspaceAutomations,
) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/a2/nodes/n2/regenerate-webhook-secret/", json={"secret": "whsec_xyz"}
    )

    result = workspace_automations.nodes.regenerate_webhook_secret("a2", "n2")

    assert result.secret == "whsec_xyz"
    assert "projects" not in responses.calls[0].request.url


# -- Sub-resources: activities (read-only) ----------------------------------------


@responses.activate
def test_project_activities_are_read_only(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/activities/",
        json={"data": [{"id": "act1", "verb": "triggered"}], "pagination": {"style": "offset"}},
    )
    responses.get(f"{PROJECT_BASE}/a1/activities/act1/", json={"id": "act1", "verb": "triggered"})

    page = project_automations.activities.list("a1")
    assert page.data[0].verb == "triggered"

    fetched = project_automations.activities.retrieve("a1", "act1")
    assert fetched.id == "act1"

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

    page = workspace_automations.activities.list("a2")

    assert page.data[0].id == "act2"
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_activities_pass_verb_filter(project_automations: ProjectAutomations) -> None:
    responses.get(
        f"{PROJECT_BASE}/a1/activities/", json={"data": [], "pagination": {"style": "offset"}}
    )

    project_automations.activities.list("a1", verb="triggered")

    assert "verb=triggered" in responses.calls[0].request.url
