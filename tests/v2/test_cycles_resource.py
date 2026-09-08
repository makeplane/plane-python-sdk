"""Offline coverage for `Cycles`; includes `transfer` and the `.work_items` membership
bridge (`add`/`remove`)."""

import json

import pytest
import responses

from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.cycles import Cycles
from plane.config import Configuration
from plane.models.v2.cycles import CreateCycle, UpdateCycle

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/cycles"


@pytest.fixture
def cycles(config: Configuration) -> Cycles:
    return Cycles(V2Transport(config))


@responses.activate
def test_list_cycles(cycles: Cycles) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Sprint 1", "timezone": "UTC"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = cycles.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].timezone == "UTC"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_sparse_response_raises_for_a_field_not_requested(cycles: Cycles) -> None:
    """`cycles.list` returns navigable (`Loaded`) rows: a field neither requested
    nor returned raises `FieldNotRequested` instead of reading as a silent `None`
    -- see `tests/v2/test_loaded_families.py`."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = cycles.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "1"
    with pytest.raises(FieldNotRequested, match="name"):
        _ = page.data[0].name


@responses.activate
def test_list_validates_expand_against_the_golden(cycles: Cycles) -> None:
    """`owned_by` is the only value `cycles_list` expands to in the golden -- a typo
    must be rejected before the request is ever sent, not silently ignored."""
    with pytest.raises(ValueError, match="Unknown expand"):
        cycles.list("acme", "ENG", expand=["ownedby"])


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(cycles: Cycles) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    cycles.list("acme", "ENG", per_page=50, offset=100)

    request_url = responses.calls[0].request.url
    assert "per_page=50" in request_url
    assert "offset=100" in request_url


@responses.activate
def test_create_then_patch(cycles: Cycles) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "name": "Sprint 1"},
        status=201,
    )
    responses.patch(
        f"{BASE}/1/",
        json={"id": "1", "name": "Sprint 1 (renamed)"},
    )

    created = cycles.create("acme", "ENG", CreateCycle(name="Sprint 1"))
    updated = cycles.update("acme", "ENG", created.id, UpdateCycle(name="Sprint 1 (renamed)"))

    assert updated.name == "Sprint 1 (renamed)"
    assert responses.calls[0].request.url == f"{BASE}/"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_retrieve_targets_the_detail_url(cycles: Cycles) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "name": "Sprint 1"})

    result = cycles.retrieve("acme", "ENG", "1")

    assert result.id == "1"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_delete(cycles: Cycles) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert cycles.delete("acme", "ENG", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_upsert_hits_the_upsert_url(cycles: Cycles) -> None:
    responses.post(
        f"{BASE}/upsert/",
        json={"id": "1", "name": "Sprint 1"},
    )

    result = cycles.upsert("acme", "ENG", CreateCycle(name="Sprint 1"))

    assert result.id == "1"
    assert responses.calls[0].request.url == f"{BASE}/upsert/"


@responses.activate
def test_bulk_create_hits_the_bulk_create_url(cycles: Cycles) -> None:
    responses.post(
        f"{BASE}/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = cycles.bulk_create("acme", "ENG", [CreateCycle(name="Sprint 1")])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-create/"


@responses.activate
def test_bulk_update_hits_the_bulk_update_url(cycles: Cycles) -> None:
    responses.post(
        f"{BASE}/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = cycles.bulk_update("acme", "ENG", [{"id": "1", "name": "Sprint 1b"}])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-update/"


@responses.activate
def test_bulk_delete_hits_the_bulk_delete_url(cycles: Cycles) -> None:
    responses.post(
        f"{BASE}/bulk-delete/",
        json={
            "results": [{"index": 0, "result": "deleted", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = cycles.bulk_delete("acme", "ENG", ["1"])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-delete/"


@responses.activate
def test_find_by_name(cycles: Cycles) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Sprint 1"}], "pagination": {"style": "offset"}},
    )

    assert cycles.find_by_name("acme", "ENG", "Sprint 1").id == "1"


# -- Custom action: transfer -----------------------------------------------------


@responses.activate
def test_transfer_sends_new_cycle_id_and_returns_it(cycles: Cycles) -> None:
    responses.post(f"{BASE}/1/transfer/", json={"new_cycle_id": "2"})

    result = cycles.transfer("acme", "ENG", "1", "2")

    assert result.new_cycle_id == "2"
    assert responses.calls[0].request.url == f"{BASE}/1/transfer/"
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"new_cycle_id": "2"}


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_cycle_work_items_bridge_takes_three_ids(cycles: Cycles) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/cycles/c1/work-items/",
        json={"added": ["w1"]},
    )

    added = cycles.work_items.add("acme", "ENG", "c1", ["w1"])

    assert added == ["w1"]
    assert responses.calls[0].request.url.endswith("/cycles/c1/work-items/")


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(cycles: Cycles) -> None:
    responses.post(f"{BASE}/1/work-items/", json={"added": ["wi-1"], "removed": []})

    result = cycles.work_items.add("acme", "ENG", "1", ["wi-1"])

    assert result == ["wi-1"]
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"add": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(cycles: Cycles) -> None:
    responses.post(f"{BASE}/1/work-items/", json={"added": [], "removed": ["wi-2"]})

    result = cycles.work_items.remove("acme", "ENG", "1", ["wi-2"])

    assert result == ["wi-2"]
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"remove": ["wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(cycles: Cycles) -> None:
    with pytest.raises(ValueError):
        cycles.work_items.add("acme", "ENG", "1", [])
    with pytest.raises(ValueError):
        cycles.work_items.add("acme", "ENG", "1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        cycles.work_items.remove("acme", "ENG", "1", [])
    with pytest.raises(ValueError):
        cycles.work_items.remove("acme", "ENG", "1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0
