"""Offline coverage for `Modules`; includes the `.work_items` membership bridge
(`add`/`remove`)."""

import json

import pytest
import responses

from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.modules import Modules
from plane.config import Configuration
from plane.models.v2.modules import CreateModule, UpdateModule

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/modules"


@pytest.fixture
def modules(config: Configuration) -> Modules:
    return Modules(V2Transport(config))


@responses.activate
def test_list_modules(modules: Modules) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Onboarding", "status": "planned"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = modules.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].status == "planned"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_sparse_response_raises_for_a_field_not_requested(modules: Modules) -> None:
    """`modules.list` returns navigable (`Loaded`) rows: a field neither requested
    nor returned raises `FieldNotRequested` instead of reading as a silent `None`
    -- see `tests/v2/test_loaded_families.py`."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = modules.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "1"
    with pytest.raises(FieldNotRequested, match="name"):
        _ = page.data[0].name


@responses.activate
def test_list_validates_expand_against_the_golden(modules: Modules) -> None:
    """`lead` and `members` are the only values `modules_list` expands to in the
    golden -- a typo must be rejected before the request is ever sent."""
    with pytest.raises(ValueError, match="Unknown expand"):
        modules.list("acme", "ENG", expand=["owner"])


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(modules: Modules) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    modules.list("acme", "ENG", per_page=10, offset=20)

    request_url = responses.calls[0].request.url
    assert "per_page=10" in request_url
    assert "offset=20" in request_url


@responses.activate
def test_create_then_patch(modules: Modules) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "name": "Onboarding", "status": "planned"},
        status=201,
    )
    responses.patch(
        f"{BASE}/1/",
        json={"id": "1", "name": "Onboarding", "status": "completed"},
    )

    created = modules.create("acme", "ENG", CreateModule(name="Onboarding"))
    updated = modules.update("acme", "ENG", created.id, UpdateModule(status="completed"))

    assert updated.status == "completed"
    assert responses.calls[0].request.url == f"{BASE}/"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_retrieve_targets_the_detail_url(modules: Modules) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "name": "Onboarding"})

    result = modules.retrieve("acme", "ENG", "1")

    assert result.id == "1"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_delete(modules: Modules) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert modules.delete("acme", "ENG", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_upsert_hits_the_upsert_url(modules: Modules) -> None:
    responses.post(
        f"{BASE}/upsert/",
        json={"id": "1", "name": "Onboarding"},
    )

    result = modules.upsert("acme", "ENG", CreateModule(name="Onboarding"))

    assert result.id == "1"
    assert responses.calls[0].request.url == f"{BASE}/upsert/"


@responses.activate
def test_bulk_create_hits_the_bulk_create_url(modules: Modules) -> None:
    responses.post(
        f"{BASE}/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = modules.bulk_create("acme", "ENG", [CreateModule(name="Onboarding")])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-create/"


@responses.activate
def test_bulk_update_hits_the_bulk_update_url(modules: Modules) -> None:
    responses.post(
        f"{BASE}/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = modules.bulk_update("acme", "ENG", [{"id": "1", "status": "completed"}])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-update/"


@responses.activate
def test_bulk_delete_hits_the_bulk_delete_url(modules: Modules) -> None:
    responses.post(
        f"{BASE}/bulk-delete/",
        json={
            "results": [{"index": 0, "result": "deleted", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = modules.bulk_delete("acme", "ENG", ["1"])

    assert result.succeeded == 1
    assert responses.calls[0].request.url == f"{BASE}/bulk-delete/"


@responses.activate
def test_find_by_name(modules: Modules) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Onboarding"}], "pagination": {"style": "offset"}},
    )

    assert modules.find_by_name("acme", "ENG", "Onboarding").id == "1"


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(modules: Modules) -> None:
    responses.post(
        f"{BASE}/mod-1/work-items/",
        json={"added": ["wi-1", "wi-2"], "removed": []},
    )

    result = modules.work_items.add("acme", "ENG", "mod-1", ["wi-1", "wi-2"])

    assert result == ["wi-1", "wi-2"]
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"add": ["wi-1", "wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/mod-1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(modules: Modules) -> None:
    responses.post(
        f"{BASE}/mod-1/work-items/",
        json={"added": [], "removed": ["wi-1"]},
    )

    result = modules.work_items.remove("acme", "ENG", "mod-1", ["wi-1"])

    assert result == ["wi-1"]
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"remove": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/mod-1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(modules: Modules) -> None:
    with pytest.raises(ValueError):
        modules.work_items.add("acme", "ENG", "mod-1", [])
    with pytest.raises(ValueError):
        modules.work_items.add("acme", "ENG", "mod-1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        modules.work_items.remove("acme", "ENG", "mod-1", [])
    with pytest.raises(ValueError):
        modules.work_items.remove("acme", "ENG", "mod-1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0
