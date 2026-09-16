"""Offline coverage for `Releases`: workspace-scoped CRUD, the `.work_items` and
`.labels` membership bridges (`add`/`remove`), the `changelog` singleton, and the
nested `comments`/`links` children -- constructed standalone here (also reachable
as `Workspaces.releases` -- see `tests/v2/test_tree.py` for that wiring). Asserts
every method's exact request URL."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.releases import Releases
from plane.config import Configuration
from plane.models.v2.releases import (
    CreateRelease,
    CreateReleaseComment,
    CreateReleaseLabel,
    CreateReleaseLink,
    UpdateRelease,
    UpdateReleaseChangelog,
    UpdateReleaseComment,
    UpdateReleaseLabel,
    UpdateReleaseLink,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/releases"


@pytest.fixture
def releases(config: Configuration) -> Releases:
    return Releases(V2Transport(config))


# -- Workspace-scoped CRUD -------------------------------------------------------


@responses.activate
def test_list_releases(releases: Releases) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "v1.0", "status": "unreleased"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = releases.list("acme")

    assert page.total_count == 1
    assert page.data[0].status == "unreleased"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_list_passes_expand_filters_order_by_and_pagination(releases: Releases) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    releases.list(
        "acme",
        expand=["lead", "tag"],
        status="unreleased",
        order_by="-created_at",
        per_page=10,
        offset=20,
    )

    query = responses.calls[0].request.url
    assert "expand=lead%2Ctag" in query
    assert "status=unreleased" in query
    assert "order_by=-created_at" in query
    assert "per_page=10" in query
    assert "offset=20" in query


def test_list_rejects_unknown_expand_before_the_request(releases: Releases) -> None:
    with pytest.raises(ValueError, match="bogus"):
        releases.list("acme", expand=["bogus"])


def test_list_rejects_unknown_fields_before_the_request(releases: Releases) -> None:
    with pytest.raises(ValueError, match="bogus"):
        releases.list("acme", fields=["bogus"])


@responses.activate
def test_iterate_releases(releases: Releases) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "v1.0"}], "pagination": {"style": "offset"}},
    )

    rows = list(releases.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_retrieve_release(releases: Releases) -> None:
    responses.get(f"{BASE}/rel-1/", json={"id": "rel-1", "name": "v1.0"})

    row = releases.retrieve("acme", "rel-1")

    assert row.id == "rel-1"
    assert responses.calls[0].request.url == f"{BASE}/rel-1/"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(releases: Releases) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = releases.list("acme", fields=["id"])

    assert page.data[0].id == "1"


@responses.activate
def test_create_then_patch(releases: Releases) -> None:
    responses.post(f"{BASE}/", json={"id": "1", "name": "v1.0"}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "v1.0-final"})

    created = releases.create("acme", CreateRelease(name="v1.0"))
    updated = releases.update("acme", created.id, UpdateRelease(name="v1.0-final"))

    assert updated.name == "v1.0-final"
    assert responses.calls[0].request.url == f"{BASE}/"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_delete_returns_none(releases: Releases) -> None:
    responses.delete(f"{BASE}/rel-1/", status=204)

    assert releases.delete("acme", "rel-1") is None
    assert responses.calls[0].request.url == f"{BASE}/rel-1/"


@responses.activate
def test_find_by_name(releases: Releases) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "v1.0"}], "pagination": {"style": "offset"}},
    )

    assert releases.find_by_name("acme", "v1.0").id == "1"


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(releases: Releases) -> None:
    responses.post(f"{BASE}/rel-1/work-items/", json={"added": ["wi-1"], "removed": []})

    result = releases.work_items.add("acme", "rel-1", ["wi-1"])

    assert result == ["wi-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(releases: Releases) -> None:
    responses.post(f"{BASE}/rel-1/work-items/", json={"added": [], "removed": ["wi-2"]})

    result = releases.work_items.remove("acme", "rel-1", ["wi-2"])

    assert result == ["wi-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(releases: Releases) -> None:
    with pytest.raises(ValueError):
        releases.work_items.add("acme", "rel-1", [])
    with pytest.raises(ValueError):
        releases.work_items.add("acme", "rel-1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        releases.work_items.remove("acme", "rel-1", [])
    with pytest.raises(ValueError):
        releases.work_items.remove("acme", "rel-1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Membership bridge: labels (per-release association) -------------------------


@responses.activate
def test_labels_add_sends_add_body_and_returns_added(releases: Releases) -> None:
    responses.post(f"{BASE}/rel-1/labels/", json={"added": ["lbl-1"], "removed": []})

    result = releases.labels.add("acme", "rel-1", ["lbl-1"])

    assert result == ["lbl-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["lbl-1"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/labels/"


@responses.activate
def test_labels_remove_sends_remove_body_and_returns_removed(releases: Releases) -> None:
    responses.post(f"{BASE}/rel-1/labels/", json={"added": [], "removed": ["lbl-2"]})

    result = releases.labels.remove("acme", "rel-1", ["lbl-2"])

    assert result == ["lbl-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["lbl-2"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/labels/"


@responses.activate
def test_labels_bridge_rejects_empty_or_oversized_ids(releases: Releases) -> None:
    with pytest.raises(ValueError):
        releases.labels.add("acme", "rel-1", [])
    with pytest.raises(ValueError):
        releases.labels.add("acme", "rel-1", [f"lbl-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        releases.labels.remove("acme", "rel-1", [])
    with pytest.raises(ValueError):
        releases.labels.remove("acme", "rel-1", [f"lbl-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Changelog (singleton) --------------------------------------------------------


@responses.activate
def test_retrieve_changelog(releases: Releases) -> None:
    responses.get(
        f"{BASE}/rel-1/changelog/",
        json={"id": "chg-1", "release_id": "rel-1", "description_html": "<p>notes</p>"},
    )

    row = releases.changelog.retrieve("acme", "rel-1")

    assert row.id == "chg-1"
    assert row.description_html == "<p>notes</p>"
    assert responses.calls[0].request.url == f"{BASE}/rel-1/changelog/"


@responses.activate
def test_changelog_update_uses_patch(releases: Releases) -> None:
    responses.patch(
        f"{BASE}/rel-1/changelog/", json={"id": "chg-1", "description_html": "<p>updated</p>"}
    )

    row = releases.changelog.update(
        "acme", "rel-1", UpdateReleaseChangelog(description_html="<p>updated</p>")
    )

    body = json.loads(responses.calls[0].request.body)
    assert body == {"description_html": "<p>updated</p>"}
    assert row.description_html == "<p>updated</p>"
    assert responses.calls[0].request.url == f"{BASE}/rel-1/changelog/"


# -- Sub-resources: comments (nested under a release) ----------------------------


@responses.activate
def test_comments_crud(releases: Releases) -> None:
    responses.get(
        f"{BASE}/rel-1/comments/",
        json={
            "data": [{"id": "c1", "comment_html": "<p>hi</p>"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{BASE}/rel-1/comments/", json={"id": "c1", "comment_html": "<p>hi</p>"}, status=201
    )
    responses.get(f"{BASE}/rel-1/comments/c1/", json={"id": "c1", "comment_html": "<p>hi</p>"})
    responses.patch(f"{BASE}/rel-1/comments/c1/", json={"id": "c1", "comment_html": "<p>bye</p>"})
    responses.delete(f"{BASE}/rel-1/comments/c1/", status=204)

    page = releases.comments.list("acme", "rel-1")
    assert page.data[0].id == "c1"
    assert responses.calls[0].request.url == f"{BASE}/rel-1/comments/"

    created = releases.comments.create(
        "acme", "rel-1", CreateReleaseComment(comment_html="<p>hi</p>")
    )
    assert created.id == "c1"
    assert responses.calls[1].request.url == f"{BASE}/rel-1/comments/"

    fetched = releases.comments.retrieve("acme", "rel-1", "c1")
    assert fetched.id == "c1"
    assert responses.calls[2].request.url == f"{BASE}/rel-1/comments/c1/"

    updated = releases.comments.update(
        "acme", "rel-1", "c1", UpdateReleaseComment(comment_html="<p>bye</p>")
    )
    assert updated.comment_html == "<p>bye</p>"
    assert responses.calls[3].request.url == f"{BASE}/rel-1/comments/c1/"

    assert releases.comments.delete("acme", "rel-1", "c1") is None
    assert responses.calls[4].request.url == f"{BASE}/rel-1/comments/c1/"


@responses.activate
def test_comments_iterate(releases: Releases) -> None:
    responses.get(
        f"{BASE}/rel-1/comments/",
        json={"data": [{"id": "c1"}], "pagination": {"style": "offset"}},
    )

    rows = list(releases.comments.iterate("acme", "rel-1"))

    assert rows[0].id == "c1"
    assert responses.calls[0].request.url == f"{BASE}/rel-1/comments/"


def test_comments_has_no_upsert_or_bulk(releases: Releases) -> None:
    """Unlike work-item comments, the golden gives release comments only the
    plain CRUD five -- no upsert/bulk-* operationIds exist for this shard."""
    assert not hasattr(releases.comments, "upsert")
    assert not hasattr(releases.comments, "bulk_create")


# -- Sub-resources: links (nested under a release) -------------------------------


@responses.activate
def test_links_crud(releases: Releases) -> None:
    responses.get(
        f"{BASE}/rel-1/links/",
        json={"data": [{"id": "l1", "url": "https://x.test"}], "pagination": {"style": "offset"}},
    )
    responses.post(f"{BASE}/rel-1/links/", json={"id": "l1", "url": "https://x.test"}, status=201)
    responses.get(f"{BASE}/rel-1/links/l1/", json={"id": "l1", "url": "https://x.test"})
    responses.patch(f"{BASE}/rel-1/links/l1/", json={"id": "l1", "url": "https://y.test"})
    responses.delete(f"{BASE}/rel-1/links/l1/", status=204)

    page = releases.links.list("acme", "rel-1")
    assert page.data[0].id == "l1"
    assert responses.calls[0].request.url == f"{BASE}/rel-1/links/"

    created = releases.links.create(
        "acme", "rel-1", CreateReleaseLink(title="Docs", url="https://x.test")
    )
    assert created.id == "l1"
    assert responses.calls[1].request.url == f"{BASE}/rel-1/links/"

    fetched = releases.links.retrieve("acme", "rel-1", "l1")
    assert fetched.id == "l1"
    assert responses.calls[2].request.url == f"{BASE}/rel-1/links/l1/"

    updated = releases.links.update("acme", "rel-1", "l1", UpdateReleaseLink(url="https://y.test"))
    assert updated.url == "https://y.test"
    assert responses.calls[3].request.url == f"{BASE}/rel-1/links/l1/"

    assert releases.links.delete("acme", "rel-1", "l1") is None
    assert responses.calls[4].request.url == f"{BASE}/rel-1/links/l1/"


# -- Catalog: labels (workspace-level, not nested under a release) ---------------


@responses.activate
def test_labels_catalog_crud(releases: Releases) -> None:
    responses.get(
        f"{BASE}/labels/",
        json={"data": [{"id": "lbl-1", "name": "breaking"}], "pagination": {"style": "offset"}},
    )
    responses.post(f"{BASE}/labels/", json={"id": "lbl-1", "name": "breaking"}, status=201)
    responses.patch(f"{BASE}/labels/lbl-1/", json={"id": "lbl-1", "name": "breaking-change"})
    responses.delete(f"{BASE}/labels/lbl-1/", status=204)

    page = releases.labels.list("acme")
    assert page.data[0].name == "breaking"
    assert responses.calls[0].request.url == f"{BASE}/labels/"

    created = releases.labels.create("acme", CreateReleaseLabel(name="breaking"))
    assert created.id == "lbl-1"

    updated = releases.labels.update("acme", "lbl-1", UpdateReleaseLabel(name="breaking-change"))
    assert updated.name == "breaking-change"
    assert responses.calls[2].request.url == f"{BASE}/labels/lbl-1/"

    assert releases.labels.delete("acme", "lbl-1") is None
    # Catalog path has no release id segment.
    assert "rel-1" not in responses.calls[0].request.url


@responses.activate
def test_labels_catalog_find_by_name(releases: Releases) -> None:
    responses.get(
        f"{BASE}/labels/",
        json={"data": [{"id": "lbl-1", "name": "breaking"}], "pagination": {"style": "offset"}},
    )

    assert releases.labels.find_by_name("acme", "breaking").id == "lbl-1"
