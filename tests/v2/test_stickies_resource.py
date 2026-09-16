import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.stickies import Stickies
from plane.config import Configuration
from plane.models.v2.stickies import CreateSticky, UpdateSticky

BASE = "https://api.example.com/api/v2/workspaces/acme/stickies"


@pytest.fixture
def stickies(config: Configuration) -> Stickies:
    return Stickies(V2Transport(config))


@responses.activate
def test_list_stickies(stickies: Stickies) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Reminder", "color": "#f00"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = stickies.list("acme")

    assert page.total_count == 1
    assert page.data[0].color == "#f00"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_sparse_response_leaves_absent_fields_none(stickies: Stickies) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = stickies.list("acme", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None
    assert "fields=id" in responses.calls[0].request.url


def test_list_rejects_unknown_field_before_the_request(stickies: Stickies) -> None:
    with pytest.raises(ValueError, match="Unknown field"):
        stickies.list("acme", fields=["bogus"])  # type: ignore[list-item]


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(stickies: Stickies) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    stickies.list("acme", per_page=10, offset=5)

    request_url = responses.calls[0].request.url
    assert "per_page=10" in request_url
    assert "offset=5" in request_url


@responses.activate
def test_iterate_takes_the_workspace_slug(stickies: Stickies) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Reminder"}], "pagination": {"style": "offset"}},
    )

    rows = list(stickies.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_retrieve(stickies: Stickies) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "name": "Reminder"})

    sticky = stickies.retrieve("acme", "1")

    assert sticky.name == "Reminder"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_create_with_empty_body_then_patch(stickies: Stickies) -> None:
    """Every field on `CreateSticky` is optional in the golden -- an empty body is
    a valid create."""
    responses.post(f"{BASE}/", json={"id": "1"}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "Todo"})

    created = stickies.create("acme", CreateSticky())
    assert responses.calls[0].request.url == f"{BASE}/"

    updated = stickies.update("acme", created.id, UpdateSticky(name="Todo"))

    assert updated.name == "Todo"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_create_accepts_fields_and_reaches_the_query_string(stickies: Stickies) -> None:
    responses.post(f"{BASE}/", json={"id": "1", "name": "Reminder"}, status=201)

    stickies.create("acme", CreateSticky(name="Reminder"), fields=["id", "name"])

    assert "fields=id%2Cname" in responses.calls[0].request.url


@responses.activate
def test_delete(stickies: Stickies) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert stickies.delete("acme", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"
