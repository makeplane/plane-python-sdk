"""Offline coverage for `Releases`: workspace-scoped, the `.work_items` and `.labels`
membership bridges (`add`/`remove`), and the `changelog` singleton sub-resource."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.releases import Releases
from plane.api.v2.releases.changelog import ReleaseChangelogResource
from plane.config import Configuration
from plane.models.v2.releases import (
    CreateRelease,
    CreateReleaseComment,
    CreateReleaseLabel,
    CreateReleaseLink,
    CreateReleaseTag,
    UpdateRelease,
    UpdateReleaseChangelog,
    UpdateReleaseComment,
    UpdateReleaseLabel,
    UpdateReleaseLink,
    UpdateReleaseTag,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/releases"


@pytest.fixture
def releases(config: Configuration) -> Releases:
    return Releases(V2Transport(config), slug="acme")


@pytest.fixture
def changelog(config: Configuration) -> ReleaseChangelogResource:
    return ReleaseChangelogResource(V2Transport(config), slug="acme")


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

    page = releases.list()

    assert page.total_count == 1
    assert page.data[0].status == "unreleased"
    # Workspace-scoped: no project segment anywhere in the URL.
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_list_passes_expand_and_filters(releases: Releases) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    releases.list(expand=["lead", "tag"], status="unreleased")

    query = responses.calls[0].request.url
    assert "expand=lead%2Ctag" in query
    assert "status=unreleased" in query


def test_list_rejects_unknown_expand_before_the_request(releases: Releases) -> None:
    with pytest.raises(ValueError, match="bogus"):
        releases.list(expand=["bogus"])


def test_list_rejects_unknown_fields_before_the_request(releases: Releases) -> None:
    with pytest.raises(ValueError, match="bogus"):
        releases.list(fields=["bogus"])


@responses.activate
def test_retrieve_release(releases: Releases) -> None:
    responses.get(f"{BASE}/rel-1/", json={"id": "rel-1", "name": "v1.0"})

    row = releases.retrieve("rel-1")

    assert row.id == "rel-1"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(releases: Releases) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = releases.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].name is None


@responses.activate
def test_create_then_patch(releases: Releases) -> None:
    responses.post(f"{BASE}/", json={"id": "1", "name": "v1.0"}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "v1.0-final"})

    created = releases.create(CreateRelease(name="v1.0"))
    updated = releases.update(created.id, UpdateRelease(name="v1.0-final"))

    assert updated.name == "v1.0-final"


@responses.activate
def test_delete_returns_none(releases: Releases) -> None:
    responses.delete(f"{BASE}/rel-1/", status=204)

    assert releases.delete("rel-1") is None


@responses.activate
def test_find_by_name(releases: Releases) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "v1.0"}], "pagination": {"style": "offset"}},
    )

    assert releases.find_by_name("v1.0").id == "1"


# -- Membership bridge: work_items ------------------------------------------------


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(releases: Releases) -> None:
    responses.post(
        f"{BASE}/rel-1/work-items/",
        json={"added": ["wi-1"], "removed": []},
    )

    result = releases.work_items.add("rel-1", ["wi-1"])

    assert result == ["wi-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(releases: Releases) -> None:
    responses.post(
        f"{BASE}/rel-1/work-items/",
        json={"added": [], "removed": ["wi-2"]},
    )

    result = releases.work_items.remove("rel-1", ["wi-2"])

    assert result == ["wi-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(releases: Releases) -> None:
    with pytest.raises(ValueError):
        releases.work_items.add("rel-1", [])
    with pytest.raises(ValueError):
        releases.work_items.add("rel-1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        releases.work_items.remove("rel-1", [])
    with pytest.raises(ValueError):
        releases.work_items.remove("rel-1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Membership bridge: labels (per-release association) -------------------------


@responses.activate
def test_labels_add_sends_add_body_and_returns_added(releases: Releases) -> None:
    responses.post(
        f"{BASE}/rel-1/labels/",
        json={"added": ["lbl-1"], "removed": []},
    )

    result = releases.labels.add("rel-1", ["lbl-1"])

    assert result == ["lbl-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["lbl-1"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/labels/"


@responses.activate
def test_labels_remove_sends_remove_body_and_returns_removed(releases: Releases) -> None:
    responses.post(
        f"{BASE}/rel-1/labels/",
        json={"added": [], "removed": ["lbl-2"]},
    )

    result = releases.labels.remove("rel-1", ["lbl-2"])

    assert result == ["lbl-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["lbl-2"]}
    assert responses.calls[0].request.url == f"{BASE}/rel-1/labels/"


@responses.activate
def test_labels_bridge_rejects_empty_or_oversized_ids(releases: Releases) -> None:
    with pytest.raises(ValueError):
        releases.labels.add("rel-1", [])
    with pytest.raises(ValueError):
        releases.labels.add("rel-1", [f"lbl-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        releases.labels.remove("rel-1", [])
    with pytest.raises(ValueError):
        releases.labels.remove("rel-1", [f"lbl-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Changelog (singleton) --------------------------------------------------------


@responses.activate
def test_retrieve_changelog(changelog: ReleaseChangelogResource) -> None:
    responses.get(
        f"{BASE}/rel-1/changelog/",
        json={"id": "chg-1", "release_id": "rel-1", "description_html": "<p>notes</p>"},
    )

    row = changelog.retrieve("rel-1")

    assert row.id == "chg-1"
    assert row.description_html == "<p>notes</p>"


@responses.activate
def test_changelog_update_uses_patch(changelog: ReleaseChangelogResource) -> None:
    responses.patch(
        f"{BASE}/rel-1/changelog/",
        json={"id": "chg-1", "description_html": "<p>updated</p>"},
    )

    row = changelog.update("rel-1", UpdateReleaseChangelog(description_html="<p>updated</p>"))

    body = json.loads(responses.calls[0].request.body)
    assert body == {"description_html": "<p>updated</p>"}
    assert row.description_html == "<p>updated</p>"


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

    page = releases.comments.list("rel-1")
    assert page.data[0].id == "c1"

    created = releases.comments.create("rel-1", CreateReleaseComment(comment_html="<p>hi</p>"))
    assert created.id == "c1"

    fetched = releases.comments.retrieve("rel-1", "c1")
    assert fetched.id == "c1"

    updated = releases.comments.update(
        "rel-1", "c1", UpdateReleaseComment(comment_html="<p>bye</p>")
    )
    assert updated.comment_html == "<p>bye</p>"

    assert releases.comments.delete("rel-1", "c1") is None


@responses.activate
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
    responses.patch(f"{BASE}/rel-1/links/l1/", json={"id": "l1", "url": "https://y.test"})
    responses.delete(f"{BASE}/rel-1/links/l1/", status=204)

    page = releases.links.list("rel-1")
    assert page.data[0].id == "l1"

    created = releases.links.create("rel-1", CreateReleaseLink(title="Docs", url="https://x.test"))
    assert created.id == "l1"

    updated = releases.links.update("rel-1", "l1", UpdateReleaseLink(url="https://y.test"))
    assert updated.url == "https://y.test"

    assert releases.links.delete("rel-1", "l1") is None


# -- Catalog: labels (workspace-level, not nested under a release) ---------------


@responses.activate
def test_labels_catalog_crud(releases: Releases) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/",
        json={"data": [{"id": "lbl-1", "name": "breaking"}], "pagination": {"style": "offset"}},
    )
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/",
        json={"id": "lbl-1", "name": "breaking"},
        status=201,
    )
    responses.patch(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/lbl-1/",
        json={"id": "lbl-1", "name": "breaking-change"},
    )
    responses.delete(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/lbl-1/", status=204
    )

    page = releases.labels.list()
    assert page.data[0].name == "breaking"

    created = releases.labels.create(CreateReleaseLabel(name="breaking"))
    assert created.id == "lbl-1"

    updated = releases.labels.update("lbl-1", UpdateReleaseLabel(name="breaking-change"))
    assert updated.name == "breaking-change"

    assert releases.labels.delete("lbl-1") is None
    # Catalog path has no release id segment.
    assert "rel-1" not in responses.calls[0].request.url


@responses.activate
def test_labels_catalog_find_by_name(releases: Releases) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/",
        json={"data": [{"id": "lbl-1", "name": "breaking"}], "pagination": {"style": "offset"}},
    )

    assert releases.labels.find_by_name("breaking").id == "lbl-1"


# -- Catalog: tags (workspace-level, version:-prefixed lookup) -------------------


@responses.activate
def test_tags_catalog_crud(releases: Releases) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/",
        json={"data": [{"id": "tag-1", "version": "1.0.0"}], "pagination": {"style": "offset"}},
    )
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/",
        json={"id": "tag-1", "version": "1.0.0"},
        status=201,
    )
    responses.patch(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/tag-1/",
        json={"id": "tag-1", "version": "1.0.1"},
    )
    responses.delete(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/tag-1/", status=204
    )

    page = releases.tags.list()
    assert page.data[0].version == "1.0.0"

    created = releases.tags.create(CreateReleaseTag(version="1.0.0"))
    assert created.id == "tag-1"

    updated = releases.tags.update("tag-1", UpdateReleaseTag(version="1.0.1"))
    assert updated.version == "1.0.1"

    assert releases.tags.delete("tag-1") is None


@responses.activate
def test_tags_catalog_retrieve_by_version_prefixed_pk(releases: Releases) -> None:
    """The golden documents the tag detail pk as UUID *or* `version:<value>` --
    the SDK does not special-case this, it just percent-encodes whatever string
    is passed, so the colon-prefixed form round-trips like any other pk."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/version%3A1.0.0/",
        json={"id": "tag-1", "version": "1.0.0"},
    )

    fetched = releases.tags.retrieve("version:1.0.0")

    assert fetched.id == "tag-1"


@responses.activate
def test_tags_catalog_find_by_version(releases: Releases) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/",
        json={"data": [{"id": "tag-1", "version": "1.0.0"}], "pagination": {"style": "offset"}},
    )

    assert releases.tags.find_by_version("1.0.0").id == "tag-1"
