"""Offline coverage for `Modules`; includes the `.work_items` membership bridge
(`add`/`remove`)."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.modules import Modules
from plane.config import Configuration
from plane.models.v2.modules import CreateModule, UpdateModule

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/modules"


@pytest.fixture
def modules(config: Configuration) -> Modules:
    return Modules(V2Transport(config), slug="acme", project_id="ENG")


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

    page = modules.list()

    assert page.total_count == 1
    assert page.data[0].status == "planned"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(modules: Modules) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = modules.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_list_validates_expand_against_the_golden(modules: Modules) -> None:
    """`lead` and `members` are the only values `modules_list` expands to in the
    golden -- a typo must be rejected before the request is ever sent."""
    with pytest.raises(ValueError, match="Unknown expand"):
        modules.list(expand=["owner"])


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

    created = modules.create(CreateModule(name="Onboarding"))
    updated = modules.update(created.id, UpdateModule(status="completed"))

    assert updated.status == "completed"


@responses.activate
def test_delete(modules: Modules) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert modules.delete("1") is None


@responses.activate
def test_upsert_hits_the_upsert_url(modules: Modules) -> None:
    responses.post(
        f"{BASE}/upsert/",
        json={"id": "1", "name": "Onboarding"},
    )

    result = modules.upsert(CreateModule(name="Onboarding"))

    assert result.id == "1"


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

    result = modules.bulk_create([CreateModule(name="Onboarding")])

    assert result.succeeded == 1


@responses.activate
def test_find_by_name(modules: Modules) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Onboarding"}], "pagination": {"style": "offset"}},
    )

    assert modules.find_by_name("Onboarding").id == "1"


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(modules: Modules) -> None:
    responses.post(
        f"{BASE}/mod-1/work-items/",
        json={"added": ["wi-1", "wi-2"], "removed": []},
    )

    result = modules.work_items.add("mod-1", ["wi-1", "wi-2"])

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

    result = modules.work_items.remove("mod-1", ["wi-1"])

    assert result == ["wi-1"]
    sent = json.loads(responses.calls[0].request.body)
    assert sent == {"remove": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/mod-1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(modules: Modules) -> None:
    with pytest.raises(ValueError):
        modules.work_items.add("mod-1", [])
    with pytest.raises(ValueError):
        modules.work_items.add("mod-1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        modules.work_items.remove("mod-1", [])
    with pytest.raises(ValueError):
        modules.work_items.remove("mod-1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0
