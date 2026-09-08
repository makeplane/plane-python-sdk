"""Offline coverage for `Labels`, mirroring `test_states_resource.py`'s bound-scope signature
convention."""

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.labels import Labels
from plane.config import Configuration
from plane.models.v2.labels import CreateLabel, UpdateLabel


@pytest.fixture
def labels(config: Configuration) -> Labels:
    return Labels(V2Transport(config))


@responses.activate
def test_list_labels(labels: Labels) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={
            "data": [{"id": "1", "name": "bug", "color": "#f00"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = labels.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].color == "#f00"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(labels: Labels) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = labels.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_create_then_patch(labels: Labels) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={"id": "1", "name": "bug", "color": "#f00"},
        status=201,
    )
    responses.patch(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/1/",
        json={"id": "1", "name": "bugfix"},
    )

    created = labels.create("acme", "ENG", CreateLabel(name="bug", color="#f00"))
    updated = labels.update("acme", "ENG", created.id, UpdateLabel(name="bugfix"))

    assert updated.name == "bugfix"


@responses.activate
def test_delete_returns_none(labels: Labels) -> None:
    responses.delete(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/1/", status=204
    )

    assert labels.delete("acme", "ENG", "1") is None


@responses.activate
def test_upsert(labels: Labels) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/upsert/",
        json={"id": "1", "name": "bug"},
    )

    assert labels.upsert("acme", "ENG", CreateLabel(name="bug")).id == "1"


@responses.activate
def test_find_by_name(labels: Labels) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={"data": [{"id": "1", "name": "bug"}], "pagination": {"style": "offset"}},
    )

    assert labels.find_by_name("acme", "ENG", "bug").id == "1"


@responses.activate
def test_bulk_create_posts_items_envelope(labels: Labels) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = labels.bulk_create("acme", "ENG", [CreateLabel(name="bug")])

    assert result.succeeded == 1
