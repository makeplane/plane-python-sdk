import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.teamspaces import Teamspaces
from plane.config import Configuration
from plane.models.v2.teamspaces import CreateTeamspace, UpdateTeamspace

BASE = "https://api.example.com/api/v2/workspaces/acme/teamspaces"


@pytest.fixture
def teamspaces(config: Configuration) -> Teamspaces:
    return Teamspaces(V2Transport(config), slug="acme")


@responses.activate
def test_list_teamspaces(teamspaces: Teamspaces) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Platform", "member_ids": ["u1"]}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = teamspaces.list()

    assert page.total_count == 1
    assert page.data[0].member_ids == ["u1"]


@responses.activate
def test_list_passes_expand_and_filters(teamspaces: Teamspaces) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    teamspaces.list(expand=["lead"], name="Platform")

    query = responses.calls[0].request.url
    assert "expand=lead" in query
    assert "name=Platform" in query


def test_list_rejects_unknown_expand_before_the_request(teamspaces: Teamspaces) -> None:
    with pytest.raises(ValueError, match="Unknown expand"):
        teamspaces.list(expand=["bogus"])


@responses.activate
def test_create_then_patch(teamspaces: Teamspaces) -> None:
    responses.post(f"{BASE}/", json={"id": "1", "name": "Platform"}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "Platform (renamed)"})

    created = teamspaces.create(CreateTeamspace(name="Platform"))
    updated = teamspaces.update(created.id, UpdateTeamspace(name="Platform (renamed)"))

    assert updated.name == "Platform (renamed)"


@responses.activate
def test_delete(teamspaces: Teamspaces) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert teamspaces.delete("1") is None


@responses.activate
def test_find_by_name(teamspaces: Teamspaces) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Platform"}], "pagination": {"style": "offset"}},
    )

    assert teamspaces.find_by_name("Platform").id == "1"
