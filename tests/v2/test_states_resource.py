import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.states import States
from plane.config import Configuration
from plane.models.v2.states import CreateState


@pytest.fixture
def states(config: Configuration) -> States:
    return States(V2Transport(config))


@responses.activate
def test_list_takes_path_ids_positionally(states: States) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={
            "data": [{"id": "1", "name": "Todo"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = states.list("acme", "ENG")

    assert page.data[0].name == "Todo"


@responses.activate
def test_path_ids_may_be_passed_by_keyword(states: States) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    states.list(slug="acme", project="ENG")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/"
    )


@responses.activate
def test_filters_reach_the_query_string(states: States) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    states.list("acme", "ENG", fields=["id", "name"], group="unstarted")

    request_url = responses.calls[0].request.url
    assert "fields=id%2Cname" in request_url
    assert "group=unstarted" in request_url


@responses.activate
def test_create_posts_to_the_collection(states: States) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"id": "2", "name": "Doing"},
    )

    created = states.create("acme", "ENG", CreateState(name="Doing", color="#fff", group="started"))

    assert created.id == "2"


@responses.activate
def test_delete_targets_the_detail_url(states: States) -> None:
    responses.delete(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/2/", status=204
    )

    assert states.delete("acme", "ENG", "2") is None
