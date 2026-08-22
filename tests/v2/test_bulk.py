import json

import pytest
import responses
from pydantic import BaseModel, ConfigDict

from plane.api.v2 import PlaneAPIError
from plane.api.v2._kernel.resource import V2Resource
from plane.api.v2._kernel.transport import V2Transport
from plane.config import Configuration
from plane.models.v2.common import BulkRowFailure, BulkRowSuccess


class Row(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None


class WriteRow(BaseModel):
    name: str


class PatchRow(BaseModel):
    name: str | None = None


class Rows(V2Resource[Row, WriteRow, PatchRow]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = Row
    operations = {
        "list": "states_list",
        "retrieve": "states_retrieve",
        "create": "states_create",
        "update": "states_partial_update",
        "upsert": "states_upsert",
    }


@pytest.fixture
def rows(config: Configuration) -> Rows:
    return Rows(V2Transport(config))


@responses.activate
def test_upsert_returns_the_row(rows: Rows) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/upsert/",
        json={"id": "1", "name": "Todo"},
    )

    assert rows._upsert(WriteRow(name="Todo"), slug="acme", project_id="ENG").id == "1"


@responses.activate
def test_bulk_create_posts_items_envelope(rows: Rows) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = rows._bulk_create([WriteRow(name="Todo")], slug="acme", project_id="ENG")

    body = json.loads(responses.calls[0].request.body)
    assert body == {"items": [{"name": "Todo"}], "all_or_none": False}
    assert isinstance(result.results[0], BulkRowSuccess)
    assert result.succeeded == 1


@responses.activate
def test_bulk_update_posts_items_envelope(rows: Rows) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = rows._bulk_update(
        [{"id": "1", "name": "Done"}], slug="acme", project_id="ENG", all_or_none=True
    )

    body = json.loads(responses.calls[0].request.body)
    assert body == {"items": [{"id": "1", "name": "Done"}], "all_or_none": True}
    assert isinstance(result.results[0], BulkRowSuccess)
    assert result.succeeded == 1


@responses.activate
def test_bulk_delete_posts_ids_envelope(rows: Rows) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/bulk-delete/",
        json={
            "results": [{"index": 0, "result": "deleted", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    rows._bulk_delete(["1"], slug="acme", project_id="ENG", all_or_none=True)

    body = json.loads(responses.calls[0].request.body)
    assert body == {"ids": ["1"], "all_or_none": True}


@responses.activate
def test_failed_rows_parse_as_failures_and_can_raise(rows: Rows) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/bulk-create/",
        json={
            "results": [
                {"index": 0, "result": "created", "id": "1"},
                {
                    "index": 1,
                    "result": "failed",
                    "type": "invalid_request",
                    "code": "invalid_request",
                    "detail": "One or more fields failed validation.",
                    "errors": [{"field": "name", "message": "This field is required."}],
                },
            ],
            "succeeded": 1,
            "failed": 1,
        },
    )

    result = rows._bulk_create(
        [WriteRow(name="Todo"), WriteRow(name="x")], slug="acme", project_id="ENG"
    )

    assert isinstance(result.results[1], BulkRowFailure)
    assert result.results[1].errors[0].field == "name"
    with pytest.raises(PlaneAPIError, match="1 of 2 rows failed") as exc_info:
        result.raise_for_failures()
    assert exc_info.value.errors[0].field == "name"


def test_batch_cap_is_enforced_client_side(rows: Rows) -> None:
    with pytest.raises(ValueError, match="At most 50"):
        rows._bulk_delete([str(n) for n in range(51)], slug="acme", project_id="ENG")


def test_empty_batch_is_rejected_client_side_for_bulk_create(rows: Rows) -> None:
    """The API 400s on an empty `items` list; the client must reject it first,
    with wording that mirrors `BulkWriteMixin.perform_bulk_create`'s own detail."""
    with pytest.raises(ValueError, match="Provide a non-empty list of write bodies\\."):
        rows._bulk_create([], slug="acme", project_id="ENG")


def test_empty_batch_is_rejected_client_side_for_bulk_update(rows: Rows) -> None:
    with pytest.raises(
        ValueError, match="Provide a non-empty list of write bodies, each with an id\\."
    ):
        rows._bulk_update([], slug="acme", project_id="ENG")


def test_empty_batch_is_rejected_client_side_for_bulk_delete(rows: Rows) -> None:
    with pytest.raises(ValueError, match="Provide a non-empty list of ids\\."):
        rows._bulk_delete([], slug="acme", project_id="ENG")
