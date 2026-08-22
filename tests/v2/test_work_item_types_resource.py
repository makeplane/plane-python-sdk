"""Offline coverage for project- and workspace-scoped `WorkItemTypes`/`WorkItemTypeProperties`."""

from __future__ import annotations

import json

import pytest
import responses
from responses import matchers

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


@pytest.fixture
def work_item_types(config: Configuration) -> WorkItemTypes:
    return WorkItemTypes(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_work_item_types(config: Configuration) -> WorkspaceWorkItemTypes:
    return WorkspaceWorkItemTypes(V2Transport(config), slug="acme")


@pytest.fixture
def properties(config: Configuration) -> WorkItemTypeProperties:
    return WorkItemTypeProperties(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_properties(config: Configuration) -> WorkspaceWorkItemTypeProperties:
    return WorkspaceWorkItemTypeProperties(V2Transport(config), slug="acme")


# -- Project-scoped WorkItemTypes CRUD --------------------------------------------


@responses.activate
def test_list_project_scoped(work_item_types: WorkItemTypes) -> None:
    responses.get(
        f"{BASE}/projects/ENG/work-item-types/",
        json={
            "data": [{"id": "1", "name": "Bug", "is_default": True}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = work_item_types.list()

    assert page.total_count == 1
    assert page.data[0].is_default is True


@responses.activate
def test_find_by_name(work_item_types: WorkItemTypes) -> None:
    responses.get(
        f"{BASE}/projects/ENG/work-item-types/",
        json={
            "data": [{"id": "1", "name": "Bug", "is_default": True}],
            "pagination": {"style": "offset"},
        },
        match=[matchers.query_param_matcher({"name": "Bug", "per_page": "2", "count": "False"})],
    )

    assert work_item_types.find_by_name("Bug").id == "1"


@responses.activate
def test_workspace_find_by_name(workspace_work_item_types: WorkspaceWorkItemTypes) -> None:
    responses.get(
        f"{BASE}/work-item-types/",
        json={
            "data": [{"id": "9", "name": "Bug", "is_default": False}],
            "pagination": {"style": "offset"},
        },
        match=[matchers.query_param_matcher({"name": "Bug", "per_page": "2", "count": "False"})],
    )

    assert workspace_work_item_types.find_by_name("Bug").id == "9"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(work_item_types: WorkItemTypes) -> None:
    responses.get(
        f"{BASE}/projects/ENG/work-item-types/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = work_item_types.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None
    assert page.data[0].level is None


@responses.activate
def test_create_then_patch_then_delete(work_item_types: WorkItemTypes) -> None:
    responses.post(
        f"{BASE}/projects/ENG/work-item-types/",
        json={"id": "1", "name": "Bug"},
        status=201,
    )
    responses.patch(
        f"{BASE}/projects/ENG/work-item-types/1/",
        json={"id": "1", "name": "Defect"},
    )
    responses.delete(f"{BASE}/projects/ENG/work-item-types/1/", status=204)

    created = work_item_types.create(CreateWorkItemType(name="Bug"))
    updated = work_item_types.update(created.id, UpdateWorkItemType(name="Defect"))
    assert updated.name == "Defect"

    assert work_item_types.delete(created.id) is None


def test_unknown_field_is_rejected_before_the_request(work_item_types: WorkItemTypes) -> None:
    with pytest.raises(ValueError, match="nope"):
        work_item_types.list(fields=["nope"])


# -- Custom verb actions -----------------------------------------------------------


@responses.activate
def test_enable_posts_to_the_collection_level_action(work_item_types: WorkItemTypes) -> None:
    """`enable` has no `{pk}` -- it is a collection-level action, unlike
    `mark_default`/`schema` which are per-row."""
    responses.post(
        f"{BASE}/projects/ENG/work-item-types/enable/",
        json={"id": "epic-type-id", "is_epic": True},
    )

    result = work_item_types.enable()

    assert result.is_epic is True
    assert responses.calls[0].request.url.endswith("/work-item-types/enable/")


@responses.activate
def test_import_types_posts_the_ids_envelope(work_item_types: WorkItemTypes) -> None:
    responses.post(f"{BASE}/projects/ENG/work-item-types/import/", json="", status=200)

    result = work_item_types.import_types(["type-a", "type-b"])

    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body == {"work_item_types": ["type-a", "type-b"]}


@responses.activate
def test_mark_default_posts_to_the_hyphenated_detail_action(
    work_item_types: WorkItemTypes,
) -> None:
    """The URL segment is `mark-default` (hyphen), not `mark_default` -- the
    kernel's `_action` uses its `name` argument verbatim as the URL suffix."""
    responses.post(
        f"{BASE}/projects/ENG/work-item-types/1/mark-default/",
        json={"id": "1", "is_default": True},
    )

    result = work_item_types.mark_default("1")

    assert result.is_default is True


def test_mark_default_validates_fields_against_its_own_operation_id(
    work_item_types: WorkItemTypes,
) -> None:
    with pytest.raises(ValueError, match="nope"):
        work_item_types.mark_default("1", fields=["nope"])


@responses.activate
def test_schema_gets_the_detail_action_and_parses_the_schema_model(
    work_item_types: WorkItemTypes,
) -> None:
    """`schema` is a GET (not a POST like every other custom action here) and
    returns a distinct `WorkItemTypeSchema`, not a `WorkItemType` row."""
    responses.get(
        f"{BASE}/projects/ENG/work-item-types/1/schema/",
        json={
            "type_id": "1",
            "type_name": "Bug",
            "type_description": None,
            "type_logo_props": None,
            "fields": {"priority": {"options": ["low", "high"]}},
            "custom_fields": [],
        },
    )

    schema = work_item_types.schema("1")

    assert schema.type_id == "1"
    assert schema.fields == {"priority": {"options": ["low", "high"]}}


# -- Workspace-scoped WorkItemTypes: different path template -----------------------


@responses.activate
def test_workspace_list_uses_a_workspace_only_path(
    workspace_work_item_types: WorkspaceWorkItemTypes,
) -> None:
    responses.get(
        f"{BASE}/work-item-types/",
        json={"data": [{"id": "1", "name": "Bug"}], "pagination": {"style": "offset"}},
    )

    page = workspace_work_item_types.list()

    assert page.data[0].name == "Bug"
    # Negative assertion: the workspace-scoped path never mentions a project.
    assert "/projects/" not in responses.calls[0].request.url


@responses.activate
def test_workspace_create_and_mark_default(
    workspace_work_item_types: WorkspaceWorkItemTypes,
) -> None:
    responses.post(f"{BASE}/work-item-types/", json={"id": "1", "name": "Bug"}, status=201)
    responses.post(f"{BASE}/work-item-types/1/mark-default/", json={"id": "1", "is_default": True})

    created = workspace_work_item_types.create(CreateWorkItemType(name="Bug"))
    marked = workspace_work_item_types.mark_default(created.id)

    assert marked.is_default is True


@responses.activate
def test_workspace_delete_returns_none(
    workspace_work_item_types: WorkspaceWorkItemTypes,
) -> None:
    responses.delete(f"{BASE}/work-item-types/1/", status=204)

    assert workspace_work_item_types.delete("1") is None


# -- Project-scoped WorkItemTypeProperties ------------------------------------------


@responses.activate
def test_properties_list_and_retrieve(properties: WorkItemTypeProperties) -> None:
    responses.get(
        f"{BASE}/projects/ENG/work-item-types/1/properties/",
        json={
            "data": [{"id": "p1", "name": "severity", "property_type": "OPTION"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.get(
        f"{BASE}/projects/ENG/work-item-types/1/properties/p1/",
        json={"id": "p1", "name": "severity", "property_type": "OPTION"},
    )

    page = properties.list("1")
    assert page.data[0].property_type == "OPTION"

    fetched = properties.retrieve("1", "p1")
    assert fetched.id == "p1"


@responses.activate
def test_properties_attach_posts_to_the_collection_url_with_ids_body(
    properties: WorkItemTypeProperties,
) -> None:
    responses.post(
        f"{BASE}/projects/ENG/work-item-types/1/properties/",
        json={"properties": ["p1", "p2"]},
    )

    result = properties.attach("1", ["p1", "p2"])

    assert result.properties == ["p1", "p2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"properties": ["p1", "p2"]}


@responses.activate
def test_properties_detach_deletes_by_property_id(properties: WorkItemTypeProperties) -> None:
    responses.delete(f"{BASE}/projects/ENG/work-item-types/1/properties/p1/", status=204)

    assert properties.detach("1", "p1") is None


# -- Workspace-scoped WorkItemTypeProperties: also a different path template -------


@responses.activate
def test_workspace_properties_list_uses_a_workspace_only_path(
    workspace_properties: WorkspaceWorkItemTypeProperties,
) -> None:
    responses.get(
        f"{BASE}/work-item-types/1/properties/",
        json={"data": [{"id": "p1", "name": "severity"}], "pagination": {"style": "offset"}},
    )

    page = workspace_properties.list("1")

    assert page.data[0].id == "p1"
    assert "/projects/" not in responses.calls[0].request.url


@responses.activate
def test_workspace_properties_attach_and_detach(
    workspace_properties: WorkspaceWorkItemTypeProperties,
) -> None:
    responses.post(f"{BASE}/work-item-types/1/properties/", json={"properties": ["p1"]})
    responses.delete(f"{BASE}/work-item-types/1/properties/p1/", status=204)

    attached = workspace_properties.attach("1", ["p1"])
    assert attached.properties == ["p1"]

    assert workspace_properties.detach("1", "p1") is None


# -- Scope forwarding: `.properties` inherits its parent's own scope ---------------


def test_project_properties_inherit_parent_scope(work_item_types: WorkItemTypes) -> None:
    assert work_item_types.properties._scope == {"slug": "acme", "project_id": "ENG"}


def test_workspace_properties_inherit_parent_scope(
    workspace_work_item_types: WorkspaceWorkItemTypes,
) -> None:
    assert workspace_work_item_types.properties._scope == {"slug": "acme"}
