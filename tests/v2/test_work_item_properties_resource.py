"""Offline coverage for `WorkItemProperties`/`WorkspaceWorkItemProperties` and
their `.options` (both scopes) / `.contexts` (workspace only) children. Asserts
every method's exact request URL. Properties/contexts validate `fields`; options
don't (the golden offers no `?fields=` there), though options do validate
`order_by`."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_item_properties import (
    WorkItemProperties,
    WorkItemPropertyContexts,
    WorkItemPropertyOptions,
    WorkspaceWorkItemProperties,
    WorkspaceWorkItemPropertyOptions,
)
from plane.config import Configuration
from plane.models.v2.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyContext,
    CreateWorkItemPropertyOption,
    UpdateWorkItemProperty,
    UpdateWorkItemPropertyOption,
)

PROJECT_BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-item-properties"
WORKSPACE_BASE = "https://api.example.com/api/v2/workspaces/acme/work-item-properties"


@pytest.fixture
def properties(config: Configuration) -> WorkItemProperties:
    return WorkItemProperties(V2Transport(config))


@pytest.fixture
def workspace_properties(config: Configuration) -> WorkspaceWorkItemProperties:
    return WorkspaceWorkItemProperties(V2Transport(config))


@pytest.fixture
def options(config: Configuration) -> WorkItemPropertyOptions:
    return WorkItemPropertyOptions(V2Transport(config))


@pytest.fixture
def workspace_options(config: Configuration) -> WorkspaceWorkItemPropertyOptions:
    return WorkspaceWorkItemPropertyOptions(V2Transport(config))


@pytest.fixture
def contexts(config: Configuration) -> WorkItemPropertyContexts:
    return WorkItemPropertyContexts(V2Transport(config))


def test_properties_attaches_its_children(properties: WorkItemProperties) -> None:
    assert isinstance(properties.options, WorkItemPropertyOptions)


def test_workspace_properties_attaches_its_children(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    assert isinstance(workspace_properties.options, WorkspaceWorkItemPropertyOptions)
    assert isinstance(workspace_properties.contexts, WorkItemPropertyContexts)


# -- WorkItemProperties (project-scoped) ----------------------------------------


@responses.activate
def test_list_properties(properties: WorkItemProperties) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "p1", "display_name": "Severity", "property_type": "OPTION"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = properties.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].property_type == "OPTION"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/"


@responses.activate
def test_sparse_response_leaves_absent_fields_unreadable(properties: WorkItemProperties) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={"data": [{"id": "p1"}], "pagination": {"style": "offset"}},
    )

    page = properties.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "p1"
    with pytest.raises(Exception, match="not available"):
        _ = page.data[0].display_name


def test_list_rejects_unknown_field_before_the_request(properties: WorkItemProperties) -> None:
    with pytest.raises(ValueError, match="bogus"):
        properties.list("acme", "ENG", fields=["bogus"])


@responses.activate
def test_create_then_patch_then_delete(properties: WorkItemProperties) -> None:
    responses.post(
        f"{PROJECT_BASE}/",
        json={"id": "p1", "display_name": "Severity", "property_type": "OPTION"},
        status=201,
    )
    responses.patch(f"{PROJECT_BASE}/p1/", json={"id": "p1", "display_name": "Priority Level"})
    responses.delete(f"{PROJECT_BASE}/p1/", status=204)

    created = properties.create(
        "acme", "ENG", CreateWorkItemProperty(display_name="Severity", property_type="OPTION")
    )
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/"

    updated = properties.update(
        "acme", "ENG", created.id, UpdateWorkItemProperty(display_name="Priority Level")
    )
    assert responses.calls[1].request.url == f"{PROJECT_BASE}/p1/"

    properties.delete("acme", "ENG", created.id)
    assert responses.calls[2].request.url == f"{PROJECT_BASE}/p1/"

    assert updated.display_name == "Priority Level"


@responses.activate
def test_retrieve_property(properties: WorkItemProperties) -> None:
    responses.get(f"{PROJECT_BASE}/p1/", json={"id": "p1", "display_name": "Severity"})

    row = properties.retrieve("acme", "ENG", "p1")

    assert row.id == "p1"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/p1/"


@responses.activate
def test_find_by_name_matches_the_machine_key(properties: WorkItemProperties) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "p1", "name": "story_points", "display_name": "Story Points"}],
            "pagination": {"style": "offset"},
        },
    )

    row = properties.find_by_name("acme", "ENG", "story_points")

    assert row.id == "p1"
    query = responses.calls[0].request.url
    assert "name=story_points" in query
    assert "display_name" not in query


@responses.activate
def test_find_by_display_name_matches_the_ui_label(properties: WorkItemProperties) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "p1", "name": "story_points", "display_name": "Story Points"}],
            "pagination": {"style": "offset"},
        },
    )

    row = properties.find_by_display_name("acme", "ENG", "Story Points")

    assert row.id == "p1"
    query = responses.calls[0].request.url
    assert "display_name=Story+Points" in query


# -- WorkItemProperties.options (project-scoped) --------------------------------


@responses.activate
def test_list_project_options(options: WorkItemPropertyOptions) -> None:
    responses.get(
        f"{PROJECT_BASE}/p1/options/",
        json={
            "data": [{"id": "o1", "name": "Critical"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = options.list("acme", "ENG", "p1")

    assert page.data[0].name == "Critical"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/p1/options/"


@responses.activate
def test_project_options_find_by_name(options: WorkItemPropertyOptions) -> None:
    responses.get(
        f"{PROJECT_BASE}/p1/options/",
        json={"data": [{"id": "o1", "name": "Critical"}], "pagination": {"style": "offset"}},
    )

    assert options.find_by_name("acme", "ENG", "p1", "Critical").id == "o1"


@responses.activate
def test_project_options_ignore_fields_kwarg_absence(options: WorkItemPropertyOptions) -> None:
    """The golden declares no `?fields=` for options; `list`/`retrieve` simply
    don't accept the kwarg (unlike `WorkItemProperties.list`, which does)."""
    responses.get(
        f"{PROJECT_BASE}/p1/options/", json={"data": [], "pagination": {"style": "offset"}}
    )

    options.list("acme", "ENG", "p1", name="Critical")

    query = responses.calls[0].request.url
    assert "name=Critical" in query
    assert "fields=" not in query


def test_project_options_list_rejects_unknown_order_by(options: WorkItemPropertyOptions) -> None:
    with pytest.raises(ValueError, match="bogus"):
        options.list("acme", "ENG", "p1", order_by="bogus")


@responses.activate
def test_project_options_crud(options: WorkItemPropertyOptions) -> None:
    responses.post(f"{PROJECT_BASE}/p1/options/", json={"id": "o1", "name": "Critical"}, status=201)
    responses.get(f"{PROJECT_BASE}/p1/options/o1/", json={"id": "o1", "name": "Critical"})
    responses.patch(f"{PROJECT_BASE}/p1/options/o1/", json={"id": "o1", "name": "Blocker"})
    responses.delete(f"{PROJECT_BASE}/p1/options/o1/", status=204)

    created = options.create("acme", "ENG", "p1", CreateWorkItemPropertyOption(name="Critical"))
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/p1/options/"

    fetched = options.retrieve("acme", "ENG", "p1", created.id)
    assert responses.calls[1].request.url == f"{PROJECT_BASE}/p1/options/o1/"

    updated = options.update(
        "acme", "ENG", "p1", created.id, UpdateWorkItemPropertyOption(name="Blocker")
    )
    assert responses.calls[2].request.url == f"{PROJECT_BASE}/p1/options/o1/"

    options.delete("acme", "ENG", "p1", created.id)
    assert responses.calls[3].request.url == f"{PROJECT_BASE}/p1/options/o1/"

    assert fetched.id == "o1"
    assert updated.name == "Blocker"


# -- WorkspaceWorkItemProperties (workspace-scoped) ------------------------------


@responses.activate
def test_list_workspace_properties(workspace_properties: WorkspaceWorkItemProperties) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={
            "data": [{"id": "p1", "display_name": "Severity"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = workspace_properties.list("acme")

    assert page.total_count == 1
    assert page.data[0].display_name == "Severity"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/"


def test_workspace_properties_list_rejects_unknown_field(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        workspace_properties.list("acme", fields=["bogus"])


@responses.activate
def test_workspace_properties_create_then_delete(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/",
        json={"id": "p1", "display_name": "Severity", "property_type": "TEXT"},
        status=201,
    )
    responses.delete(f"{WORKSPACE_BASE}/p1/", status=204)

    created = workspace_properties.create(
        "acme", CreateWorkItemProperty(display_name="Severity", property_type="TEXT")
    )
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/"

    workspace_properties.delete("acme", created.id)
    assert responses.calls[1].request.url == f"{WORKSPACE_BASE}/p1/"

    assert created.id == "p1"


@responses.activate
def test_workspace_properties_find_by_name_matches_the_machine_key(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={
            "data": [{"id": "p1", "name": "story_points", "display_name": "Story Points"}],
            "pagination": {"style": "offset"},
        },
    )

    row = workspace_properties.find_by_name("acme", "story_points")

    assert row.id == "p1"
    assert "name=story_points" in responses.calls[0].request.url


@responses.activate
def test_workspace_properties_find_by_display_name_matches_the_ui_label(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={
            "data": [{"id": "p1", "name": "story_points", "display_name": "Story Points"}],
            "pagination": {"style": "offset"},
        },
    )

    row = workspace_properties.find_by_display_name("acme", "Story Points")

    assert row.id == "p1"
    assert "display_name=Story+Points" in responses.calls[0].request.url


# -- WorkspaceWorkItemProperties.contexts ----------------------------------------


@responses.activate
def test_list_contexts(contexts: WorkItemPropertyContexts) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/p1/contexts/",
        json={
            "data": [{"id": "c1", "is_required": True, "applies_to_all_projects": True}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = contexts.list("acme", "p1")

    assert page.data[0].applies_to_all_projects is True
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/p1/contexts/"


@responses.activate
def test_contexts_find_by_name(contexts: WorkItemPropertyContexts) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/p1/contexts/",
        json={
            "data": [{"id": "c1", "name": "Bug-only", "is_required": True}],
            "pagination": {"style": "offset"},
        },
    )

    assert contexts.find_by_name("acme", "p1", "Bug-only").id == "c1"


def test_contexts_list_rejects_unknown_field(contexts: WorkItemPropertyContexts) -> None:
    with pytest.raises(ValueError, match="bogus"):
        contexts.list("acme", "p1", fields=["bogus"])


@responses.activate
def test_contexts_create_then_patch_then_delete(contexts: WorkItemPropertyContexts) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/p1/contexts/", json={"id": "c1", "is_required": True}, status=201
    )
    responses.patch(f"{WORKSPACE_BASE}/p1/contexts/c1/", json={"id": "c1", "is_required": False})
    responses.delete(f"{WORKSPACE_BASE}/p1/contexts/c1/", status=204)

    created = contexts.create(
        "acme", "p1", CreateWorkItemPropertyContext(is_required=True, project_ids=["proj-1"])
    )
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/p1/contexts/"

    updated = contexts.update(
        "acme", "p1", created.id, CreateWorkItemPropertyContext(is_required=False)
    )
    assert responses.calls[1].request.url == f"{WORKSPACE_BASE}/p1/contexts/c1/"

    contexts.delete("acme", "p1", created.id)
    assert responses.calls[2].request.url == f"{WORKSPACE_BASE}/p1/contexts/c1/"

    assert updated.is_required is False


@responses.activate
def test_contexts_create_sends_write_only_ids(contexts: WorkItemPropertyContexts) -> None:
    responses.post(f"{WORKSPACE_BASE}/p1/contexts/", json={"id": "c1"}, status=201)

    contexts.create(
        "acme",
        "p1",
        CreateWorkItemPropertyContext(
            project_ids=["proj-1", "proj-2"], issue_type_ids=["type-1"], is_required=True
        ),
    )

    body = json.loads(responses.calls[0].request.body)
    assert body == {
        "project_ids": ["proj-1", "proj-2"],
        "issue_type_ids": ["type-1"],
        "is_required": True,
    }


# -- WorkspaceWorkItemProperties.options -----------------------------------------


@responses.activate
def test_list_workspace_options(workspace_options: WorkspaceWorkItemPropertyOptions) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/p1/options/",
        json={
            "data": [{"id": "o1", "name": "Critical"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = workspace_options.list("acme", "p1")

    assert page.data[0].name == "Critical"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/p1/options/"


@responses.activate
def test_workspace_options_find_by_name(
    workspace_options: WorkspaceWorkItemPropertyOptions,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/p1/options/",
        json={"data": [{"id": "o1", "name": "Critical"}], "pagination": {"style": "offset"}},
    )

    assert workspace_options.find_by_name("acme", "p1", "Critical").id == "o1"


def test_workspace_options_list_rejects_unknown_order_by(
    workspace_options: WorkspaceWorkItemPropertyOptions,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        workspace_options.list("acme", "p1", order_by="bogus")


@responses.activate
def test_workspace_options_crud(workspace_options: WorkspaceWorkItemPropertyOptions) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/p1/options/", json={"id": "o1", "name": "Critical"}, status=201
    )
    responses.get(f"{WORKSPACE_BASE}/p1/options/o1/", json={"id": "o1", "name": "Critical"})
    responses.patch(f"{WORKSPACE_BASE}/p1/options/o1/", json={"id": "o1", "name": "Blocker"})
    responses.delete(f"{WORKSPACE_BASE}/p1/options/o1/", status=204)

    created = workspace_options.create("acme", "p1", CreateWorkItemPropertyOption(name="Critical"))
    fetched = workspace_options.retrieve("acme", "p1", created.id)
    updated = workspace_options.update(
        "acme", "p1", created.id, UpdateWorkItemPropertyOption(name="Blocker")
    )
    workspace_options.delete("acme", "p1", created.id)

    assert fetched.id == "o1"
    assert updated.name == "Blocker"
    assert responses.calls[3].request.url == f"{WORKSPACE_BASE}/p1/options/o1/"


# -- Navigation: a fetched property reaches its options/contexts -- see
# tests/v2/test_loaded_work_item_properties.py.
