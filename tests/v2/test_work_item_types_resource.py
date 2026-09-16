"""Offline coverage for `WorkItemTypes`/`WorkspaceWorkItemTypes` and their
`.properties` children: CRUD, the four custom actions (`enable`, `import_types`,
`mark_default`, `schema`), and navigation from a fetched row. Asserts every
method's exact request URL. Project-scoped resources are depth 2 (`slug,
project`, plus their own `type` pk); workspace-scoped ones are depth 1 (`slug`,
plus their own `type` pk)."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_item_types import (
    WorkItemTypeProperties,
    WorkItemTypes,
    WorkspaceWorkItemTypeProperties,
    WorkspaceWorkItemTypes,
)
from plane.config import Configuration
from plane.models.v2.work_item_types import CreateWorkItemType, UpdateWorkItemType

BASE = "https://api.example.com/api/v2/workspaces/acme"
PROJECT_BASE = f"{BASE}/projects/ENG/work-item-types"
WORKSPACE_BASE = f"{BASE}/work-item-types"


@pytest.fixture
def work_item_types(config: Configuration) -> WorkItemTypes:
    return WorkItemTypes(V2Transport(config))


@pytest.fixture
def workspace_work_item_types(config: Configuration) -> WorkspaceWorkItemTypes:
    return WorkspaceWorkItemTypes(V2Transport(config))


@pytest.fixture
def properties(config: Configuration) -> WorkItemTypeProperties:
    return WorkItemTypeProperties(V2Transport(config))


@pytest.fixture
def workspace_properties(config: Configuration) -> WorkspaceWorkItemTypeProperties:
    return WorkspaceWorkItemTypeProperties(V2Transport(config))


def test_work_item_types_attaches_its_children(work_item_types: WorkItemTypes) -> None:
    assert isinstance(work_item_types.properties, WorkItemTypeProperties)


def test_workspace_work_item_types_attaches_its_children(
    workspace_work_item_types: WorkspaceWorkItemTypes,
) -> None:
    assert isinstance(workspace_work_item_types.properties, WorkspaceWorkItemTypeProperties)


# -- Project-scoped WorkItemTypes CRUD --------------------------------------------


@responses.activate
def test_list_project_scoped(work_item_types: WorkItemTypes) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "1", "name": "Bug", "is_default": True}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = work_item_types.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].is_default is True
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/"


@responses.activate
def test_list_passes_filters_and_pagination(work_item_types: WorkItemTypes) -> None:
    responses.get(f"{PROJECT_BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    work_item_types.list("acme", "ENG", name="Bug", per_page=25, offset=50)

    query = responses.calls[0].request.url
    assert "name=Bug" in query
    assert "per_page=25" in query
    assert "offset=50" in query


@responses.activate
def test_find_by_name(work_item_types: WorkItemTypes) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "1", "name": "Bug", "is_default": True}],
            "pagination": {"style": "offset"},
        },
    )

    row = work_item_types.find_by_name("acme", "ENG", "Bug")

    assert row.id == "1"
    query = responses.calls[0].request.url
    assert "name=Bug" in query
    assert "per_page=2" in query


@responses.activate
def test_workspace_find_by_name(workspace_work_item_types: WorkspaceWorkItemTypes) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={
            "data": [{"id": "9", "name": "Bug", "is_default": False}],
            "pagination": {"style": "offset"},
        },
    )

    assert workspace_work_item_types.find_by_name("acme", "Bug").id == "9"


@responses.activate
def test_sparse_response_leaves_absent_fields_unreadable(work_item_types: WorkItemTypes) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = work_item_types.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "1"
    with pytest.raises(Exception, match="not available"):
        _ = page.data[0].name


@responses.activate
def test_create_then_patch_then_delete(work_item_types: WorkItemTypes) -> None:
    responses.post(f"{PROJECT_BASE}/", json={"id": "1", "name": "Bug"}, status=201)
    responses.patch(f"{PROJECT_BASE}/1/", json={"id": "1", "name": "Defect"})
    responses.delete(f"{PROJECT_BASE}/1/", status=204)

    created = work_item_types.create("acme", "ENG", CreateWorkItemType(name="Bug"))
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/"

    updated = work_item_types.update("acme", "ENG", created.id, UpdateWorkItemType(name="Defect"))
    assert updated.name == "Defect"
    assert responses.calls[1].request.url == f"{PROJECT_BASE}/1/"

    assert work_item_types.delete("acme", "ENG", created.id) is None
    assert responses.calls[2].request.url == f"{PROJECT_BASE}/1/"


def test_unknown_field_is_rejected_before_the_request(work_item_types: WorkItemTypes) -> None:
    with pytest.raises(ValueError, match="nope"):
        work_item_types.list("acme", "ENG", fields=["nope"])


# -- Custom verb actions -----------------------------------------------------------


@responses.activate
def test_enable_posts_to_the_collection_level_action(work_item_types: WorkItemTypes) -> None:
    """`enable` has no `{pk}` -- it is a collection-level action, unlike
    `mark_default`/`schema` which are per-row. Routed through the kernel's
    `_custom_action`, not a hand-built URL."""
    responses.post(f"{PROJECT_BASE}/enable/", json={"id": "epic-type-id", "is_epic": True})

    result = work_item_types.enable("acme", "ENG")

    assert result.is_epic is True
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/enable/"


@responses.activate
def test_import_types_posts_the_ids_envelope(work_item_types: WorkItemTypes) -> None:
    """Also collection-level, and also routed through the kernel (`_custom_request`),
    not a hand-built URL."""
    responses.post(f"{PROJECT_BASE}/import/", json="", status=200)

    result = work_item_types.import_types("acme", "ENG", ["type-a", "type-b"])

    assert result is None
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/import/"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"work_item_types": ["type-a", "type-b"]}


@responses.activate
def test_mark_default_posts_to_the_hyphenated_detail_action(work_item_types: WorkItemTypes) -> None:
    """The URL segment is `mark-default` (hyphen), not `mark_default` -- the
    kernel's `_action` uses its `name` argument verbatim as the URL suffix."""
    responses.post(f"{PROJECT_BASE}/1/mark-default/", json={"id": "1", "is_default": True})

    result = work_item_types.mark_default("acme", "ENG", "1")

    assert result.is_default is True
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/1/mark-default/"


def test_mark_default_validates_fields_against_its_own_operation_id(
    work_item_types: WorkItemTypes,
) -> None:
    with pytest.raises(ValueError, match="nope"):
        work_item_types.mark_default("acme", "ENG", "1", fields=["nope"])


@responses.activate
def test_schema_gets_the_detail_action_and_parses_the_schema_model(
    work_item_types: WorkItemTypes,
) -> None:
    """`schema` is a GET (not a POST like every other custom action here) and
    returns a distinct `WorkItemTypeSchema`, not a `WorkItemType` row -- so it is
    not one of the methods routed through `_load`."""
    responses.get(
        f"{PROJECT_BASE}/1/schema/",
        json={
            "type_id": "1",
            "type_name": "Bug",
            "type_description": None,
            "type_logo_props": None,
            "fields": {"priority": {"options": ["low", "high"]}},
            "custom_fields": [],
        },
    )

    schema = work_item_types.schema("acme", "ENG", "1")

    assert schema.type_id == "1"
    assert schema.fields == {"priority": {"options": ["low", "high"]}}
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/1/schema/"


@responses.activate
def test_schema_passes_the_include_filter(work_item_types: WorkItemTypes) -> None:
    responses.get(f"{PROJECT_BASE}/1/schema/", json={"type_id": "1"})

    work_item_types.schema("acme", "ENG", "1", include="custom_fields")

    assert responses.calls[0].request.url == f"{PROJECT_BASE}/1/schema/?include=custom_fields"


# -- Workspace-scoped WorkItemTypes: different path template -----------------------


@responses.activate
def test_workspace_list_uses_a_workspace_only_path(
    workspace_work_item_types: WorkspaceWorkItemTypes,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={"data": [{"id": "1", "name": "Bug"}], "pagination": {"style": "offset"}},
    )

    page = workspace_work_item_types.list("acme")

    assert page.data[0].name == "Bug"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/"


@responses.activate
def test_workspace_create_and_mark_default(
    workspace_work_item_types: WorkspaceWorkItemTypes,
) -> None:
    responses.post(f"{WORKSPACE_BASE}/", json={"id": "1", "name": "Bug"}, status=201)
    responses.post(f"{WORKSPACE_BASE}/1/mark-default/", json={"id": "1", "is_default": True})

    created = workspace_work_item_types.create("acme", CreateWorkItemType(name="Bug"))
    marked = workspace_work_item_types.mark_default("acme", created.id)

    assert marked.is_default is True
    assert responses.calls[1].request.url == f"{WORKSPACE_BASE}/1/mark-default/"


@responses.activate
def test_workspace_delete_returns_none(workspace_work_item_types: WorkspaceWorkItemTypes) -> None:
    responses.delete(f"{WORKSPACE_BASE}/1/", status=204)

    assert workspace_work_item_types.delete("acme", "1") is None
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/1/"


# -- Project-scoped WorkItemTypeProperties ------------------------------------------


@responses.activate
def test_properties_list_and_retrieve(properties: WorkItemTypeProperties) -> None:
    responses.get(
        f"{PROJECT_BASE}/1/properties/",
        json={
            "data": [{"id": "p1", "name": "severity", "property_type": "OPTION"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.get(
        f"{PROJECT_BASE}/1/properties/p1/",
        json={"id": "p1", "name": "severity", "property_type": "OPTION"},
    )

    page = properties.list("acme", "ENG", "1")
    assert page.data[0].property_type == "OPTION"
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/1/properties/"

    fetched = properties.retrieve("acme", "ENG", "1", "p1")
    assert fetched.id == "p1"
    assert responses.calls[1].request.url == f"{PROJECT_BASE}/1/properties/p1/"


@responses.activate
def test_properties_link_posts_to_the_collection_url_with_ids_body(
    properties: WorkItemTypeProperties,
) -> None:
    responses.post(f"{PROJECT_BASE}/1/properties/", json={"properties": ["p1", "p2"]})

    result = properties.link("acme", "ENG", "1", ["p1", "p2"])

    assert result.properties == ["p1", "p2"]
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/1/properties/"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"properties": ["p1", "p2"]}


@responses.activate
def test_properties_unlink_deletes_by_property_id(properties: WorkItemTypeProperties) -> None:
    responses.delete(f"{PROJECT_BASE}/1/properties/p1/", status=204)

    assert properties.unlink("acme", "ENG", "1", "p1") is None
    assert responses.calls[0].request.url == f"{PROJECT_BASE}/1/properties/p1/"


# -- Workspace-scoped WorkItemTypeProperties: also a different path template -------


@responses.activate
def test_workspace_properties_list_uses_a_workspace_only_path(
    workspace_properties: WorkspaceWorkItemTypeProperties,
) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/1/properties/",
        json={"data": [{"id": "p1", "name": "severity"}], "pagination": {"style": "offset"}},
    )

    page = workspace_properties.list("acme", "1")

    assert page.data[0].id == "p1"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/1/properties/"


@responses.activate
def test_workspace_properties_link_and_unlink(
    workspace_properties: WorkspaceWorkItemTypeProperties,
) -> None:
    responses.post(f"{WORKSPACE_BASE}/1/properties/", json={"properties": ["p1"]})
    responses.delete(f"{WORKSPACE_BASE}/1/properties/p1/", status=204)

    linked = workspace_properties.link("acme", "1", ["p1"])
    assert linked.properties == ["p1"]
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/1/properties/"

    assert workspace_properties.unlink("acme", "1", "p1") is None
    assert responses.calls[1].request.url == f"{WORKSPACE_BASE}/1/properties/p1/"


# -- Navigation: a fetched work item type reaches its properties -- see
# tests/v2/test_loaded_work_item_types.py.
