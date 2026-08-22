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
    return WorkItemRelationDefinitions(V2Transport(config), slug="acme")


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

    page = relation_definitions.list()

    assert page.total_count == 1
    assert page.data[0].inward == "blocks"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(
    relation_definitions: WorkItemRelationDefinitions,
) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = relation_definitions.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_create_then_patch(relation_definitions: WorkItemRelationDefinitions) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "name": "relates to", "inward": "relates to", "outward": "relates to"},
        status=201,
    )
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "relates to (renamed)"})

    created = relation_definitions.create(
        CreateWorkItemRelationDefinition(
            name="relates to", inward="relates to", outward="relates to"
        )
    )
    updated = relation_definitions.update(
        created.id, UpdateWorkItemRelationDefinition(name="relates to (renamed)")
    )

    assert updated.name == "relates to (renamed)"


@responses.activate
def test_delete(relation_definitions: WorkItemRelationDefinitions) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert relation_definitions.delete("1") is None


@responses.activate
def test_find_by_name(relation_definitions: WorkItemRelationDefinitions) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "blocks"}], "pagination": {"style": "offset"}},
    )

    assert relation_definitions.find_by_name("blocks").id == "1"
