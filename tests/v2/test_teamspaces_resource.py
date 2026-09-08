import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.teamspaces import Teamspaces
from plane.config import Configuration
from plane.models.v2.teamspaces import CreateTeamspace, UpdateTeamspace

BASE = "https://api.example.com/api/v2/workspaces/acme/teamspaces"


@pytest.fixture
def teamspaces(config: Configuration) -> Teamspaces:
    return Teamspaces(V2Transport(config))


@responses.activate
def test_create_posts_to_the_workspace_collection(teamspaces: Teamspaces) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/teamspaces/",
        json={"id": "t1", "name": "Platform"},
    )

    created = teamspaces.create("acme", CreateTeamspace(name="Platform"))

    assert created.id == "t1"
    assert responses.calls[0].request.url.endswith("/workspaces/acme/teamspaces/")


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

    page = teamspaces.list("acme")

    assert page.total_count == 1
    assert page.data[0].member_ids == ["u1"]
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_list_passes_expand_and_filters(teamspaces: Teamspaces) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    teamspaces.list("acme", expand=["lead"], name="Platform")

    query = responses.calls[0].request.url
    assert query.startswith(f"{BASE}/")
    assert "expand=lead" in query
    assert "name=Platform" in query


def test_list_rejects_unknown_expand_before_the_request(teamspaces: Teamspaces) -> None:
    with pytest.raises(ValueError, match="Unknown expand"):
        teamspaces.list("acme", expand=["bogus"])


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(teamspaces: Teamspaces) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    teamspaces.list("acme", per_page=15, offset=30)

    request_url = responses.calls[0].request.url
    assert "per_page=15" in request_url
    assert "offset=30" in request_url


@responses.activate
def test_iterate_takes_the_workspace_slug(teamspaces: Teamspaces) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Platform"}], "pagination": {"style": "offset"}},
    )

    rows = list(teamspaces.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_retrieve(teamspaces: Teamspaces) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "name": "Platform"})

    teamspace = teamspaces.retrieve("acme", "1")

    assert teamspace.name == "Platform"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_create_then_patch(teamspaces: Teamspaces) -> None:
    responses.post(f"{BASE}/", json={"id": "1", "name": "Platform"}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "Platform (renamed)"})

    created = teamspaces.create("acme", CreateTeamspace(name="Platform"))
    assert responses.calls[0].request.url == f"{BASE}/"

    updated = teamspaces.update("acme", created.id, UpdateTeamspace(name="Platform (renamed)"))

    assert updated.name == "Platform (renamed)"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_delete(teamspaces: Teamspaces) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert teamspaces.delete("acme", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_find_by_name(teamspaces: Teamspaces) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Platform"}], "pagination": {"style": "offset"}},
    )

    found = teamspaces.find_by_name("acme", "Platform")

    assert found.id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")
