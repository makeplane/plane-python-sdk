import pytest
import responses
from pydantic import BaseModel, ConfigDict
from responses import matchers

from plane.api.v2 import MultipleMatchesFound, NoMatchFound
from plane.api.v2._kernel.resource import V2Resource
from plane.api.v2._kernel.transport import V2Transport
from plane.config import Configuration


class Row(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None


class WriteRow(BaseModel):
    name: str


class PatchRow(BaseModel):
    name: str | None = None


class Rows(V2Resource[Row, WriteRow, PatchRow]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = Row
    operations = {
        "list": "states_list",
        "retrieve": "states_retrieve",
        "create": "states_create",
        "update": "states_partial_update",
        "upsert": "states_upsert",
    }


@pytest.fixture
def rows(config: Configuration) -> Rows:
    return Rows(V2Transport(config))


@responses.activate
def test_find_one_returns_the_single_match(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [{"id": "1", "name": "Todo"}], "pagination": {"style": "offset"}},
        match=[matchers.query_param_matcher({"name": "Todo", "per_page": "2", "count": "False"})],
    )

    assert rows._find_one(filters={"name": "Todo"}, slug="acme", project_id="ENG").id == "1"


@responses.activate
def test_find_one_raises_when_nothing_matches(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}},
        match=[matchers.query_param_matcher({"name": "Nope", "per_page": "2", "count": "False"})],
    )

    with pytest.raises(NoMatchFound, match="name='Nope'"):
        rows._find_one(filters={"name": "Nope"}, slug="acme", project_id="ENG")


@responses.activate
def test_find_one_raises_when_several_match(rows: Rows) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={
            "data": [{"id": "1", "name": "Todo"}, {"id": "2", "name": "todo"}],
            "pagination": {"style": "offset"},
        },
        match=[matchers.query_param_matcher({"name": "Todo", "per_page": "2", "count": "False"})],
    )

    with pytest.raises(MultipleMatchesFound, match="Multiple rows matched"):
        rows._find_one(filters={"name": "Todo"}, slug="acme", project_id="ENG")
