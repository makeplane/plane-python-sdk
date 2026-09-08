"""Offline coverage for `Collections`; covers CRUD, `default()`, and the `members`/`pages`
sub-resources' list/membership-bridge (`add`/`remove`) verbs."""

import json

import pytest
import responses

from plane.api.v2._kernel.errors import NoMatchFound
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.collections import Collections
from plane.config import Configuration
from plane.models.v2.collections import CollectionMemberAdd, CreateCollection, UpdateCollection

BASE = "https://api.example.com/api/v2/workspaces/acme/collections"


@pytest.fixture
def collections(config: Configuration) -> Collections:
    return Collections(V2Transport(config))


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

    page = collections.list("acme")

    assert page.total_count == 1
    assert page.data[0].name == "Runbooks"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_list_passes_expand(collections: Collections) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    collections.list("acme", expand=["owned_by"])

    assert responses.calls[0].request.url == f"{BASE}/?expand=owned_by"


@responses.activate
def test_retrieve_collection(collections: Collections) -> None:
    responses.get(f"{BASE}/c1/", json={"id": "c1", "name": "Runbooks"})

    row = collections.retrieve("acme", "c1")

    assert row.id == "c1"
    assert responses.calls[0].request.url == f"{BASE}/c1/"


@responses.activate
def test_find_by_name(collections: Collections) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "c1", "name": "Runbooks"}], "pagination": {"style": "offset"}},
    )

    assert collections.find_by_name("acme", "Runbooks").id == "c1"


@responses.activate
def test_default_uses_the_is_default_query_filter(collections: Collections) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "c1", "name": "General", "is_default": True}],
            "pagination": {"style": "offset"},
        },
    )

    default = collections.default("acme")

    assert default.id == "c1"
    assert "is_default=True" in responses.calls[0].request.url


@responses.activate
def test_default_raises_when_none_found(collections: Collections) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    with pytest.raises(NoMatchFound):
        collections.default("acme")


@responses.activate
def test_create_accepts_a_bare_body(collections: Collections) -> None:
    """`CollectionWriteRequest` names no required field in the golden."""
    responses.post(f"{BASE}/", json={"id": "c1"}, status=201)

    created = collections.create("acme", CreateCollection())

    assert created.id == "c1"
    assert json.loads(responses.calls[0].request.body) == {}
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_update_uses_patch(collections: Collections) -> None:
    responses.patch(f"{BASE}/c1/", json={"id": "c1", "name": "Renamed"})

    updated = collections.update("acme", "c1", UpdateCollection(name="Renamed"))

    assert updated.name == "Renamed"
    assert responses.calls[0].request.url == f"{BASE}/c1/"


@responses.activate
def test_delete_returns_none(collections: Collections) -> None:
    responses.delete(f"{BASE}/c1/", status=204)

    assert collections.delete("acme", "c1") is None
    assert responses.calls[0].request.url == f"{BASE}/c1/"


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

    members = collections.members.list("acme", "c1")

    assert [m.member_id for m in members] == ["u1", "u2"]
    assert members[0].access == 2
    assert responses.calls[0].request.url == f"{BASE}/c1/members/"


@responses.activate
def test_members_list_passes_expand(collections: Collections) -> None:
    responses.get(f"{BASE}/c1/members/", json=[])

    collections.members.list("acme", "c1", expand=["member"])

    assert responses.calls[0].request.url == f"{BASE}/c1/members/?expand=member"


def test_members_list_rejects_unknown_expand(collections: Collections) -> None:
    with pytest.raises(ValueError, match="bogus"):
        collections.members.list("acme", "c1", expand=["bogus"])


@responses.activate
def test_members_add_sends_add_body_and_returns_added(collections: Collections) -> None:
    responses.post(f"{BASE}/c1/members/", json={"added": ["u1"], "removed": []})

    result = collections.members.add("acme", "c1", [CollectionMemberAdd(member_id="u1", access=1)])

    assert result == ["u1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": [{"member_id": "u1", "access": 1}]}
    assert responses.calls[0].request.url == f"{BASE}/c1/members/"


@responses.activate
def test_members_remove_sends_remove_body_and_returns_removed(collections: Collections) -> None:
    responses.post(f"{BASE}/c1/members/", json={"added": [], "removed": ["u2"]})

    result = collections.members.remove("acme", "c1", ["u2"])

    assert result == ["u2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["u2"]}
    assert responses.calls[0].request.url == f"{BASE}/c1/members/"


@responses.activate
def test_members_bridge_rejects_empty_or_oversized_ids(collections: Collections) -> None:
    with pytest.raises(ValueError):
        collections.members.add("acme", "c1", [])
    with pytest.raises(ValueError):
        collections.members.add(
            "acme", "c1", [CollectionMemberAdd(member_id=f"u-{i}") for i in range(101)]
        )
    with pytest.raises(ValueError):
        collections.members.remove("acme", "c1", [])
    with pytest.raises(ValueError):
        collections.members.remove("acme", "c1", [f"u-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Pages (collections.pages) ---------------------------------------------------


@responses.activate
def test_pages_add_sends_add_body_and_returns_added(collections: Collections) -> None:
    responses.post(f"{BASE}/c1/pages/", json={"added": ["p1"], "removed": []})

    result = collections.pages.add("acme", "c1", ["p1"])

    assert result == ["p1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["p1"]}
    assert responses.calls[0].request.url == f"{BASE}/c1/pages/"


@responses.activate
def test_pages_remove_sends_remove_body_and_returns_removed(collections: Collections) -> None:
    responses.post(f"{BASE}/c1/pages/", json={"added": [], "removed": ["p2"]})

    result = collections.pages.remove("acme", "c1", ["p2"])

    assert result == ["p2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["p2"]}
    assert responses.calls[0].request.url == f"{BASE}/c1/pages/"


@responses.activate
def test_pages_bridge_rejects_empty_or_oversized_ids(collections: Collections) -> None:
    with pytest.raises(ValueError):
        collections.pages.add("acme", "c1", [])
    with pytest.raises(ValueError):
        collections.pages.add("acme", "c1", [f"p-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        collections.pages.remove("acme", "c1", [])
    with pytest.raises(ValueError):
        collections.pages.remove("acme", "c1", [f"p-{i}" for i in range(101)])

    assert len(responses.calls) == 0


@responses.activate
def test_pages_search_parses_a_plain_array(collections: Collections) -> None:
    """Same unpaginated-array shape as `members.list` -- see the module
    docstrings in `plane.api.v2.collections`."""
    responses.get(
        f"{BASE}/c1/pages-search/",
        json=[{"id": "p1", "name": "Runbook"}, {"id": "p2", "name": "Onboarding"}],
    )

    rows = collections.pages.search("acme", "c1")

    assert [r.name for r in rows] == ["Runbook", "Onboarding"]
    assert responses.calls[0].request.url == f"{BASE}/c1/pages-search/"


@responses.activate
def test_pages_search_passes_fields(collections: Collections) -> None:
    responses.get(f"{BASE}/c1/pages-search/", json=[])

    collections.pages.search("acme", "c1", fields=["id", "name"])

    assert responses.calls[0].request.url == f"{BASE}/c1/pages-search/?fields=id%2Cname"
