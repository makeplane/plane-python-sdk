"""Offline coverage for `Collections`; covers CRUD, `default()`, and the `members`/`pages` sub-
resources' list/manage verbs."""

import json

import pytest
import responses

from plane.api.v2._kernel.errors import NoMatchFound
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.collections import Collections
from plane.config import Configuration
from plane.models.v2.collections import (
    CollectionMemberAdd,
    CollectionMembersManage,
    CollectionPagesManage,
    CreateCollection,
    UpdateCollection,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/collections"


@pytest.fixture
def collections(config: Configuration) -> Collections:
    return Collections(V2Transport(config), slug="acme")


# -- CRUD --------------------------------------------------------------------------


@responses.activate
def test_list_collections(collections: Collections) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "c1", "name": "Runbooks"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = collections.list()

    assert page.total_count == 1
    assert page.data[0].name == "Runbooks"


@responses.activate
def test_retrieve_collection(collections: Collections) -> None:
    responses.get(f"{BASE}/c1/", json={"id": "c1", "name": "Runbooks"})

    row = collections.retrieve("c1")

    assert row.id == "c1"


@responses.activate
def test_find_by_name(collections: Collections) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "c1", "name": "Runbooks"}], "pagination": {"style": "offset"}},
    )

    assert collections.find_by_name("Runbooks").id == "c1"


@responses.activate
def test_default_uses_the_is_default_query_filter(collections: Collections) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "c1", "name": "General", "is_default": True}],
            "pagination": {"style": "offset"},
        },
    )

    default = collections.default()

    assert default.id == "c1"
    assert "is_default=True" in responses.calls[0].request.url


@responses.activate
def test_default_raises_when_none_found(collections: Collections) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    with pytest.raises(NoMatchFound):
        collections.default()


@responses.activate
def test_create_accepts_a_bare_body(collections: Collections) -> None:
    """`CollectionWriteRequest` names no required field in the golden."""
    responses.post(f"{BASE}/", json={"id": "c1"}, status=201)

    created = collections.create(CreateCollection())

    assert created.id == "c1"
    assert json.loads(responses.calls[0].request.body) == {}


@responses.activate
def test_update_uses_patch(collections: Collections) -> None:
    responses.patch(f"{BASE}/c1/", json={"id": "c1", "name": "Renamed"})

    updated = collections.update("c1", UpdateCollection(name="Renamed"))

    assert updated.name == "Renamed"


@responses.activate
def test_delete_returns_none(collections: Collections) -> None:
    responses.delete(f"{BASE}/c1/", status=204)

    assert collections.delete("c1") is None


# -- Members (collections.members) ----------------------------------------------


@responses.activate
def test_members_list_parses_a_plain_array(collections: Collections) -> None:
    """The golden documents a bare `CollectionMember` (not an array, not an
    envelope) for this operation, and it carries no pagination params -- the
    real shape is a plain JSON array of rows."""
    responses.get(
        f"{BASE}/c1/members/",
        json=[
            {"id": "m1", "member_id": "u1", "access": 2},
            {"id": "m2", "member_id": "u2", "access": 0},
        ],
    )

    members = collections.members.list("c1")

    assert [m.member_id for m in members] == ["u1", "u2"]
    assert members[0].access == 2


@responses.activate
def test_members_list_passes_expand(collections: Collections) -> None:
    responses.get(f"{BASE}/c1/members/", json=[])

    collections.members.list("c1", expand=["member"])

    assert "expand=member" in responses.calls[0].request.url


def test_members_list_rejects_unknown_expand(collections: Collections) -> None:
    with pytest.raises(ValueError, match="bogus"):
        collections.members.list("c1", expand=["bogus"])


@responses.activate
def test_members_manage_adds_and_removes(collections: Collections) -> None:
    responses.post(
        f"{BASE}/c1/members/",
        json={"added": ["u1"], "removed": ["u2"]},
    )

    result = collections.members.manage(
        "c1",
        CollectionMembersManage(add=[CollectionMemberAdd(member_id="u1", access=1)], remove=["u2"]),
    )

    assert result.added == ["u1"]
    assert result.removed == ["u2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": [{"member_id": "u1", "access": 1}], "remove": ["u2"]}


# -- Pages (collections.pages) ---------------------------------------------------


@responses.activate
def test_pages_manage_adds_and_removes(collections: Collections) -> None:
    responses.post(f"{BASE}/c1/pages/", json={"added": ["p1"], "removed": []})

    result = collections.pages.manage("c1", CollectionPagesManage(add=["p1"]))

    assert result.added == ["p1"]
    assert result.removed == []
    assert "/collections/c1/pages/" in responses.calls[0].request.url


@responses.activate
def test_pages_search_parses_a_plain_array(collections: Collections) -> None:
    """Same unpaginated-array shape as `members.list` -- see the module
    docstrings in `plane.api.v2.collections`."""
    responses.get(
        f"{BASE}/c1/pages-search/",
        json=[{"id": "p1", "name": "Runbook"}, {"id": "p2", "name": "Onboarding"}],
    )

    rows = collections.pages.search("c1")

    assert [r.name for r in rows] == ["Runbook", "Onboarding"]


@responses.activate
def test_pages_search_passes_fields(collections: Collections) -> None:
    responses.get(f"{BASE}/c1/pages-search/", json=[])

    collections.pages.search("c1", fields=["id", "name"])

    assert "fields=id%2Cname" in responses.calls[0].request.url
