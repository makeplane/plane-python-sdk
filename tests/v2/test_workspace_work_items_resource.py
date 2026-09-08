"""Offline coverage for `WorkspaceWorkItems`; carries `retrieve_by_identifier`, fetching a work
item by its human-readable key with no project id."""

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_items.workspace import WorkspaceWorkItems
from plane.config import Configuration

BASE = "https://api.example.com/api/v2/workspaces/acme/work-items"


@pytest.fixture
def workspace_work_items(config: Configuration) -> WorkspaceWorkItems:
    return WorkspaceWorkItems(V2Transport(config))


@responses.activate
def test_list_hits_the_workspace_level_path_not_the_project_one(
    workspace_work_items: WorkspaceWorkItems,
) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = workspace_work_items.list("acme")

    assert page.data[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_list_passes_expand_and_filters(workspace_work_items: WorkspaceWorkItems) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    workspace_work_items.list("acme", expand=["state"], project_id="proj-1")

    query = responses.calls[0].request.url
    assert "expand=state" in query
    assert "project_id=proj-1" in query


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(
    workspace_work_items: WorkspaceWorkItems,
) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    workspace_work_items.list("acme", per_page=25, offset=50)

    query = responses.calls[0].request.url
    assert "per_page=25" in query
    assert "offset=50" in query


def test_list_rejects_unknown_expand_before_the_request(
    workspace_work_items: WorkspaceWorkItems,
) -> None:
    with pytest.raises(ValueError, match="bogus"):
        workspace_work_items.list("acme", expand=["bogus"])


@responses.activate
def test_iterate_follows_pages(workspace_work_items: WorkspaceWorkItems) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}, "next": 1},
    )
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "2"}], "pagination": {"style": "offset"}, "next": None},
    )

    rows = list(workspace_work_items.iterate("acme"))

    assert [row.id for row in rows] == ["1", "2"]
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_retrieve_by_identifier_is_the_readable_key_lookup(
    workspace_work_items: WorkspaceWorkItems,
) -> None:
    responses.get(
        f"{BASE}/ENG-12/",
        json={"id": "wi-1", "identifier": "ENG-12"},
    )

    row = workspace_work_items.retrieve_by_identifier("acme", "ENG-12")

    assert row.identifier == "ENG-12"
    assert responses.calls[0].request.url == f"{BASE}/ENG-12/"
    # No project id anywhere in the URL -- the whole point of this lookup.
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_retrieve_by_identifier_uses_the_readable_key_route(
    workspace_work_items: WorkspaceWorkItems,
) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/work-items/ENG-12/",
        json={"id": "w1", "sequence_id": 12},
    )

    row = workspace_work_items.retrieve_by_identifier("acme", "ENG-12")

    assert row.id == "w1"
    assert responses.calls[0].request.url.endswith("/work-items/ENG-12/")
