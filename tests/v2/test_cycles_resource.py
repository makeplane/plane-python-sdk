"""Offline coverage for `Cycles`; includes `transfer` and the `.work_items` membership
bridge (`add`/`remove`)."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.cycles import Cycles
from plane.config import Configuration
from plane.models.v2.cycles import CreateCycle, UpdateCycle

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/cycles"


@pytest.fixture
def cycles(config: Configuration) -> Cycles:
    return Cycles(V2Transport(config), slug="acme", project_id="ENG")


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

    page = cycles.list()

    assert page.total_count == 1
    assert page.data[0].timezone == "UTC"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(cycles: Cycles) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = cycles.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_list_validates_expand_against_the_golden(cycles: Cycles) -> None:
    """`owned_by` is the only value `cycles_list` expands to in the golden -- a typo
    must be rejected before the request is ever sent, not silently ignored."""
    with pytest.raises(ValueError, match="Unknown expand"):
        cycles.list(expand=["ownedby"])


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

    created = cycles.create(CreateCycle(name="Sprint 1"))
    updated = cycles.update(created.id, UpdateCycle(name="Sprint 1 (renamed)"))

    assert updated.name == "Sprint 1 (renamed)"


@responses.activate
def test_delete(cycles: Cycles) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert cycles.delete("1") is None


@responses.activate
def test_upsert_hits_the_upsert_url(cycles: Cycles) -> None:
    responses.post(
        f"{BASE}/upsert/",
        json={"id": "1", "name": "Sprint 1"},
    )

    result = cycles.upsert(CreateCycle(name="Sprint 1"))

    assert result.id == "1"


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

    result = cycles.bulk_create([CreateCycle(name="Sprint 1")])

    assert result.succeeded == 1


@responses.activate
def test_find_by_name(cycles: Cycles) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Sprint 1"}], "pagination": {"style": "offset"}},
    )

    assert cycles.find_by_name("Sprint 1").id == "1"


# -- Custom action: transfer -----------------------------------------------------


@responses.activate
def test_transfer_sends_new_cycle_id_and_returns_it(cycles: Cycles) -> None:
    responses.post(f"{BASE}/1/transfer/", json={"new_cycle_id": "2"})

    result = cycles.transfer("1", "2")

    assert result.new_cycle_id == "2"
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"new_cycle_id": "2"}


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(cycles: Cycles) -> None:
    responses.post(f"{BASE}/1/work-items/", json={"added": ["wi-1"], "removed": []})

    result = cycles.work_items.add("1", ["wi-1"])

    assert result == ["wi-1"]
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"add": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(cycles: Cycles) -> None:
    responses.post(f"{BASE}/1/work-items/", json={"added": [], "removed": ["wi-2"]})

    result = cycles.work_items.remove("1", ["wi-2"])

    assert result == ["wi-2"]
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"remove": ["wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(cycles: Cycles) -> None:
    with pytest.raises(ValueError):
        cycles.work_items.add("1", [])
    with pytest.raises(ValueError):
        cycles.work_items.add("1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        cycles.work_items.remove("1", [])
    with pytest.raises(ValueError):
        cycles.work_items.remove("1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0
