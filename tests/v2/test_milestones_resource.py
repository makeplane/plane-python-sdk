"""Offline coverage for `Milestones`; includes the `.work_items` membership bridge
(`add`/`remove`)."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.milestones import Milestones
from plane.config import Configuration
from plane.models.v2.milestones import CreateMilestone, UpdateMilestone

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/milestones"


@pytest.fixture
def milestones(config: Configuration) -> Milestones:
    return Milestones(V2Transport(config))


@responses.activate
def test_list_milestones(milestones: Milestones) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "title": "Beta launch"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = milestones.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].title == "Beta launch"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(milestones: Milestones) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = milestones.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].title is None


@responses.activate
def test_list_validates_fields_against_the_golden(milestones: Milestones) -> None:
    """`title` is a real field on `milestones_list` in the golden; `name` is not --
    milestones use `title`, not `name`, for the write/read field itself. A bad field
    name must be rejected client-side before the request is ever sent."""
    with pytest.raises(ValueError, match="Unknown field"):
        milestones.list("acme", "ENG", fields=["name"])


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(milestones: Milestones) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    milestones.list("acme", "ENG", per_page=25, offset=50)

    request_url = responses.calls[0].request.url
    assert "per_page=25" in request_url
    assert "offset=50" in request_url


@responses.activate
def test_create_then_patch(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "title": "Beta launch"},
        status=201,
    )
    responses.patch(
        f"{BASE}/1/",
        json={"id": "1", "title": "GA launch"},
    )

    created = milestones.create("acme", "ENG", CreateMilestone(title="Beta launch"))
    updated = milestones.update("acme", "ENG", created.id, UpdateMilestone(title="GA launch"))

    assert updated.title == "GA launch"
    assert responses.calls[0].request.url == f"{BASE}/"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_retrieve_targets_the_detail_url(milestones: Milestones) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "title": "Beta launch"})

    result = milestones.retrieve("acme", "ENG", "1")

    assert result.id == "1"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_delete(milestones: Milestones) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert milestones.delete("acme", "ENG", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_upsert_hits_the_upsert_url(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/upsert/",
        json={"id": "1", "title": "Beta launch"},
    )

    result = milestones.upsert("acme", "ENG", CreateMilestone(title="Beta launch"))

    assert result.id == "1"
    assert responses.calls[0].request.url == f"{BASE}/upsert/"


@responses.activate
def test_bulk_create_hits_the_bulk_create_url(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = milestones.bulk_create("acme", "ENG", [CreateMilestone(title="Beta launch")])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-create/"


@responses.activate
def test_bulk_update_hits_the_bulk_update_url(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = milestones.bulk_update("acme", "ENG", [{"id": "1", "title": "GA launch"}])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-update/"


@responses.activate
def test_bulk_delete_hits_the_bulk_delete_url(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/bulk-delete/",
        json={
            "results": [{"index": 0, "result": "deleted", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = milestones.bulk_delete("acme", "ENG", ["1"])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-delete/"


@responses.activate
def test_find_by_name_filters_on_the_name_query_param(milestones: Milestones) -> None:
    """The golden aliases the `?name=` filter to the `title` column server-side, so
    `find_by_name` keeps the same `name` parameter every other resource uses even
    though the underlying field is `title`."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "title": "Beta launch"}], "pagination": {"style": "offset"}},
    )

    assert milestones.find_by_name("acme", "ENG", "Beta launch").id == "1"

    request = responses.calls[0].request
    assert "name=Beta" in (request.url or "")


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/m1/work-items/",
        json={"added": ["wi-1"], "removed": []},
    )

    result = milestones.work_items.add("acme", "ENG", "m1", ["wi-1"])

    assert result == ["wi-1"]
    sent_body = json.loads(responses.calls[0].request.body)
    assert sent_body == {"add": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/m1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/m1/work-items/",
        json={"added": [], "removed": ["wi-2"]},
    )

    result = milestones.work_items.remove("acme", "ENG", "m1", ["wi-2"])

    assert result == ["wi-2"]
    sent_body = json.loads(responses.calls[0].request.body)
    assert sent_body == {"remove": ["wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/m1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(milestones: Milestones) -> None:
    with pytest.raises(ValueError):
        milestones.work_items.add("acme", "ENG", "m1", [])
    with pytest.raises(ValueError):
        milestones.work_items.add("acme", "ENG", "m1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        milestones.work_items.remove("acme", "ENG", "m1", [])
    with pytest.raises(ValueError):
        milestones.work_items.remove("acme", "ENG", "m1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0
