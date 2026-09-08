import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.intakes import Intakes
from plane.config import Configuration
from plane.models.v2.intakes import CreateIntakeWorkItem, UpdateIntakeWorkItem

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/intake-issues"


@pytest.fixture
def intakes(config: Configuration) -> Intakes:
    return Intakes(V2Transport(config))


@responses.activate
def test_list_takes_slug_and_project(intakes: Intakes) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Bug report", "status": -2}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = intakes.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].status == -2
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_list_passes_filters(intakes: Intakes) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    intakes.list("acme", "ENG", status=1)

    assert "status=1" in responses.calls[0].request.url


@responses.activate
def test_sparse_response_leaves_absent_fields_none(intakes: Intakes) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = intakes.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_create_then_patch_status(intakes: Intakes) -> None:
    """PATCH folds the triage status transition into the same call as any other
    field -- no separate status endpoint in v2."""
    responses.post(f"{BASE}/", json={"id": "1", "name": "Bug report", "status": -2}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "Bug report", "status": 1})

    created = intakes.create("acme", "ENG", CreateIntakeWorkItem(name="Bug report"))
    updated = intakes.update("acme", "ENG", created.id, UpdateIntakeWorkItem(status=1))

    assert updated.status == 1
    assert responses.calls[0].request.url == f"{BASE}/"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_delete(intakes: Intakes) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert intakes.delete("acme", "ENG", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"
