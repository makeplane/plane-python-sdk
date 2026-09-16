import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_item_relation_definitions import WorkItemRelationDefinitions
from plane.config import Configuration
from plane.models.v2.work_item_relation_definitions import (
    CreateWorkItemRelationDefinition,
    UpdateWorkItemRelationDefinition,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/work-item-relation-definitions"


@pytest.fixture
def relation_definitions(config: Configuration) -> WorkItemRelationDefinitions:
    return WorkItemRelationDefinitions(V2Transport(config))


@responses.activate
def test_list_relation_definitions(
    relation_definitions: WorkItemRelationDefinitions,
) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "blocks", "inward": "blocks", "outward": "blocked by"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = relation_definitions.list("acme")

    assert page.total_count == 1
    assert page.data[0].inward == "blocks"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_sparse_response_leaves_absent_fields_none(
    relation_definitions: WorkItemRelationDefinitions,
) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = relation_definitions.list("acme", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None
    assert "fields=id" in responses.calls[0].request.url


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(
    relation_definitions: WorkItemRelationDefinitions,
) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    relation_definitions.list("acme", per_page=5, offset=10)

    request_url = responses.calls[0].request.url
    assert "per_page=5" in request_url
    assert "offset=10" in request_url


@responses.activate
def test_iterate_takes_the_workspace_slug(
    relation_definitions: WorkItemRelationDefinitions,
) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "blocks"}], "pagination": {"style": "offset"}},
    )

    rows = list(relation_definitions.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_retrieve(relation_definitions: WorkItemRelationDefinitions) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "name": "blocks"})

    definition = relation_definitions.retrieve("acme", "1")

    assert definition.name == "blocks"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_create_then_patch(relation_definitions: WorkItemRelationDefinitions) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "name": "relates to", "inward": "relates to", "outward": "relates to"},
        status=201,
    )
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "relates to (renamed)"})

    created = relation_definitions.create(
        "acme",
        CreateWorkItemRelationDefinition(
            name="relates to", inward="relates to", outward="relates to"
        ),
    )
    assert responses.calls[0].request.url == f"{BASE}/"

    updated = relation_definitions.update(
        "acme", created.id, UpdateWorkItemRelationDefinition(name="relates to (renamed)")
    )

    assert updated.name == "relates to (renamed)"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_delete(relation_definitions: WorkItemRelationDefinitions) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert relation_definitions.delete("acme", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_find_by_name(relation_definitions: WorkItemRelationDefinitions) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "blocks"}], "pagination": {"style": "offset"}},
    )

    found = relation_definitions.find_by_name("acme", "blocks")

    assert found.id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")
