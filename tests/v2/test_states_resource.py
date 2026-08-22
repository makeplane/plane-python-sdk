import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.states import States
from plane.config import Configuration
from plane.models.v2.states import CreateState, UpdateState


@pytest.fixture
def states(config: Configuration) -> States:
    return States(V2Transport(config), slug="acme", project_id="ENG")


@responses.activate
def test_list_states(states: States) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={
            "data": [{"id": "1", "name": "Todo", "group": "unstarted"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = states.list()

    assert page.total_count == 1
    assert page.data[0].group == "unstarted"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(states: States) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = states.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_create_then_patch(states: States) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"id": "1", "name": "Todo", "color": "#fff"},
        status=201,
    )
    responses.patch(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/1/",
        json={"id": "1", "name": "Doing"},
    )

    created = states.create(CreateState(name="Todo", color="#fff"))
    updated = states.update(created.id, UpdateState(name="Doing"))

    assert updated.name == "Doing"


@responses.activate
def test_find_by_name(states: States) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [{"id": "1", "name": "Todo"}], "pagination": {"style": "offset"}},
    )

    assert states.find_by_name("Todo").id == "1"
