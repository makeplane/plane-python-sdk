"""Offline coverage for work item properties + `.options`/`.contexts`; properties/contexts validate
`fields`, options don't, though options do validate `order_by`."""

import pytest
import responses
from responses import matchers

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
    return WorkItemProperties(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_properties(config: Configuration) -> WorkspaceWorkItemProperties:
    return WorkspaceWorkItemProperties(V2Transport(config), slug="acme")


@pytest.fixture
def options(config: Configuration) -> WorkItemPropertyOptions:
    return WorkItemPropertyOptions(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_options(config: Configuration) -> WorkspaceWorkItemPropertyOptions:
    return WorkspaceWorkItemPropertyOptions(V2Transport(config), slug="acme")


@pytest.fixture
def contexts(config: Configuration) -> WorkItemPropertyContexts:
    return WorkItemPropertyContexts(V2Transport(config), slug="acme")


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

    page = properties.list()

    assert page.total_count == 1
    assert page.data[0].property_type == "OPTION"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(properties: WorkItemProperties) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={"data": [{"id": "p1"}], "pagination": {"style": "offset"}},
    )

    page = properties.list(fields=["id"])

    assert page.data[0].id == "p1"
    assert page.data[0].display_name is None


def test_list_rejects_unknown_field_before_the_request(properties: WorkItemProperties) -> None:
    with pytest.raises(ValueError, match="bogus"):
        properties.list(fields=["bogus"])


@responses.activate
def test_create_then_patch_then_delete(properties: WorkItemProperties) -> None:
    responses.post(
        f"{PROJECT_BASE}/",
        json={"id": "p1", "display_name": "Severity", "property_type": "OPTION"},
        status=201,
    )
    responses.patch(
        f"{PROJECT_BASE}/p1/",
        json={"id": "p1", "display_name": "Priority Level"},
    )
    responses.delete(f"{PROJECT_BASE}/p1/", status=204)

    created = properties.create(
        CreateWorkItemProperty(display_name="Severity", property_type="OPTION")
    )
    updated = properties.update(created.id, UpdateWorkItemProperty(display_name="Priority Level"))
    properties.delete(created.id)

    assert updated.display_name == "Priority Level"


@responses.activate
def test_retrieve_property(properties: WorkItemProperties) -> None:
    responses.get(f"{PROJECT_BASE}/p1/", json={"id": "p1", "display_name": "Severity"})

    row = properties.retrieve("p1")

    assert row.id == "p1"


@responses.activate
def test_find_by_name(properties: WorkItemProperties) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "p1", "name": "story_points", "display_name": "Story Points"}],
            "pagination": {"style": "offset"},
        },
        match=[
            matchers.query_param_matcher(
                {"name": "story_points", "per_page": "2", "count": "False"}
            )
        ],
    )

    assert properties.find_by_name("story_points").id == "p1"


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

    page = options.list("p1")

    assert page.data[0].name == "Critical"


@responses.activate
def test_project_options_find_by_name(options: WorkItemPropertyOptions) -> None:
    responses.get(
        f"{PROJECT_BASE}/p1/options/",
        json={"data": [{"id": "o1", "name": "Critical"}], "pagination": {"style": "offset"}},
        match=[
            matchers.query_param_matcher({"name": "Critical", "per_page": "2", "count": "False"})
        ],
    )

    assert options.find_by_name("p1", "Critical").id == "o1"


@responses.activate
def test_project_options_list_ignores_fields_kwarg_absence(
    options: WorkItemPropertyOptions,
) -> None:
    """The golden declares no `?fields=` for options; `list`/`retrieve` simply
    don't accept the kwarg (unlike `WorkItemProperties.list`, which does)."""
    responses.get(
        f"{PROJECT_BASE}/p1/options/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    options.list("p1", name="Critical")

    query = responses.calls[0].request.url
    assert "name=Critical" in query
    assert "fields=" not in query


def test_project_options_list_rejects_unknown_order_by(options: WorkItemPropertyOptions) -> None:
    with pytest.raises(ValueError, match="bogus"):
        options.list("p1", order_by="bogus")


@responses.activate
def test_project_options_crud(options: WorkItemPropertyOptions) -> None:
    responses.post(
        f"{PROJECT_BASE}/p1/options/",
        json={"id": "o1", "name": "Critical"},
        status=201,
    )
    responses.get(f"{PROJECT_BASE}/p1/options/o1/", json={"id": "o1", "name": "Critical"})
    responses.patch(f"{PROJECT_BASE}/p1/options/o1/", json={"id": "o1", "name": "Blocker"})
    responses.delete(f"{PROJECT_BASE}/p1/options/o1/", status=204)

    created = options.create("p1", CreateWorkItemPropertyOption(name="Critical"))
    fetched = options.retrieve("p1", created.id)
    updated = options.update("p1", created.id, UpdateWorkItemPropertyOption(name="Blocker"))
    options.delete("p1", created.id)

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

    page = workspace_properties.list()

    assert page.total_count == 1
    assert page.data[0].display_name == "Severity"


def test_workspace_properties_list_rejects_unknown_field(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        workspace_properties.list(fields=["bogus"])


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
        CreateWorkItemProperty(display_name="Severity", property_type="TEXT")
    )
    workspace_properties.delete(created.id)

    assert created.id == "p1"


@responses.activate
def test_workspace_properties_find_by_name(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={
            "data": [{"id": "p1", "name": "story_points", "display_name": "Story Points"}],
            "pagination": {"style": "offset"},
        },
        match=[
            matchers.query_param_matcher(
                {"name": "story_points", "per_page": "2", "count": "False"}
            )
        ],
    )

    assert workspace_properties.find_by_name("story_points").id == "p1"


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

    page = contexts.list("p1")

    assert page.data[0].applies_to_all_projects is True


@responses.activate
def test_contexts_find_by_name(contexts: WorkItemPropertyContexts) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/p1/contexts/",
        json={
            "data": [{"id": "c1", "name": "Bug-only", "is_required": True}],
            "pagination": {"style": "offset"},
        },
        match=[
            matchers.query_param_matcher({"name": "Bug-only", "per_page": "2", "count": "False"})
        ],
    )

    assert contexts.find_by_name("p1", "Bug-only").id == "c1"


def test_contexts_list_rejects_unknown_field(contexts: WorkItemPropertyContexts) -> None:
    with pytest.raises(ValueError, match="bogus"):
        contexts.list("p1", fields=["bogus"])


@responses.activate
def test_contexts_create_then_patch_then_delete(contexts: WorkItemPropertyContexts) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/p1/contexts/",
        json={"id": "c1", "is_required": True},
        status=201,
    )
    responses.patch(f"{WORKSPACE_BASE}/p1/contexts/c1/", json={"id": "c1", "is_required": False})
    responses.delete(f"{WORKSPACE_BASE}/p1/contexts/c1/", status=204)

    created = contexts.create(
        "p1", CreateWorkItemPropertyContext(is_required=True, project_ids=["proj-1"])
    )
    updated = contexts.update("p1", created.id, CreateWorkItemPropertyContext(is_required=False))
    contexts.delete("p1", created.id)

    assert updated.is_required is False


@responses.activate
def test_contexts_create_sends_write_only_ids(contexts: WorkItemPropertyContexts) -> None:
    import json

    responses.post(f"{WORKSPACE_BASE}/p1/contexts/", json={"id": "c1"}, status=201)

    contexts.create(
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

    page = workspace_options.list("p1")

    assert page.data[0].name == "Critical"


@responses.activate
def test_workspace_options_find_by_name(
    workspace_options: WorkspaceWorkItemPropertyOptions,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/p1/options/",
        json={"data": [{"id": "o1", "name": "Critical"}], "pagination": {"style": "offset"}},
        match=[
            matchers.query_param_matcher({"name": "Critical", "per_page": "2", "count": "False"})
        ],
    )

    assert workspace_options.find_by_name("p1", "Critical").id == "o1"


def test_workspace_options_list_rejects_unknown_order_by(
    workspace_options: WorkspaceWorkItemPropertyOptions,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        workspace_options.list("p1", order_by="bogus")


@responses.activate
def test_workspace_options_crud(workspace_options: WorkspaceWorkItemPropertyOptions) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/p1/options/",
        json={"id": "o1", "name": "Critical"},
        status=201,
    )
    responses.get(f"{WORKSPACE_BASE}/p1/options/o1/", json={"id": "o1", "name": "Critical"})
    responses.patch(f"{WORKSPACE_BASE}/p1/options/o1/", json={"id": "o1", "name": "Blocker"})
    responses.delete(f"{WORKSPACE_BASE}/p1/options/o1/", status=204)

    created = workspace_options.create("p1", CreateWorkItemPropertyOption(name="Critical"))
    fetched = workspace_options.retrieve("p1", created.id)
    updated = workspace_options.update(
        "p1", created.id, UpdateWorkItemPropertyOption(name="Blocker")
    )
    workspace_options.delete("p1", created.id)

    assert fetched.id == "o1"
    assert updated.name == "Blocker"


# -- Scope forwarding: `.options`/`.contexts` inherit their parent's own scope ----


def test_project_options_inherit_parent_scope(properties: WorkItemProperties) -> None:
    assert properties.options._scope == {"slug": "acme", "project_id": "ENG"}


def test_workspace_options_and_contexts_inherit_parent_scope(
    workspace_properties: WorkspaceWorkItemProperties,
) -> None:
    assert workspace_properties.options._scope == {"slug": "acme"}
    assert workspace_properties.contexts._scope == {"slug": "acme"}
