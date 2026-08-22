import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.stickies import Stickies
from plane.config import Configuration
from plane.models.v2.stickies import CreateSticky, UpdateSticky

BASE = "https://api.example.com/api/v2/workspaces/acme/stickies"


@pytest.fixture
def stickies(config: Configuration) -> Stickies:
    return Stickies(V2Transport(config), slug="acme")


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

    page = stickies.list()

    assert page.total_count == 1
    assert page.data[0].color == "#f00"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(stickies: Stickies) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = stickies.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


def test_list_rejects_unknown_field_before_the_request(stickies: Stickies) -> None:
    with pytest.raises(ValueError, match="Unknown field"):
        stickies.list(fields=["bogus"])


@responses.activate
def test_create_with_empty_body_then_patch(stickies: Stickies) -> None:
    """Every field on `CreateSticky` is optional in the golden -- an empty body is
    a valid create."""
    responses.post(f"{BASE}/", json={"id": "1"}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "Todo"})

    created = stickies.create(CreateSticky())
    updated = stickies.update(created.id, UpdateSticky(name="Todo"))

    assert updated.name == "Todo"


@responses.activate
def test_delete(stickies: Stickies) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert stickies.delete("1") is None
