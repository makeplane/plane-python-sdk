"""Offline coverage for `ReleaseTags`, constructed standalone here (also reachable
as `Releases.tags` -- see `tests/v2/test_tree.py` for that wiring). Asserts every
method's exact request URL, including the golden/server mismatch on `tag_id` that
`find_by_version` exists to work around."""

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.releases.tags import ReleaseTags
from plane.config import Configuration
from plane.models.v2.releases import CreateReleaseTag, UpdateReleaseTag

BASE = "https://api.example.com/api/v2/workspaces/acme/releases/tags"


@pytest.fixture
def release_tags(config: Configuration) -> ReleaseTags:
    return ReleaseTags(V2Transport(config))


@responses.activate
def test_list_takes_the_workspace_slug(release_tags: ReleaseTags) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "tag-1", "version": "1.0.0"}], "pagination": {"style": "offset"}},
    )

    page = release_tags.list("acme")

    assert page.data[0].version == "1.0.0"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(release_tags: ReleaseTags) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    release_tags.list("acme", per_page=10, offset=20)

    query = responses.calls[0].request.url
    assert "per_page=10" in query
    assert "offset=20" in query


@responses.activate
def test_iterate_takes_the_workspace_slug(release_tags: ReleaseTags) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "tag-1", "version": "1.0.0"}], "pagination": {"style": "offset"}},
    )

    rows = list(release_tags.iterate("acme"))

    assert rows[0].id == "tag-1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_retrieve_by_uuid(release_tags: ReleaseTags) -> None:
    responses.get(f"{BASE}/tag-1/", json={"id": "tag-1", "version": "1.0.0"})

    row = release_tags.retrieve("acme", "tag-1")

    assert row.id == "tag-1"
    assert responses.calls[0].request.url == f"{BASE}/tag-1/"


@responses.activate
def test_find_by_version_is_the_way_to_resolve_a_version_to_an_id(
    release_tags: ReleaseTags,
) -> None:
    """The golden implies `retrieve(slug, "version:<value>")` works; it 404s live
    -- `find_by_version` is the supported way to resolve a version string."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "tag-1", "version": "1.0.0"}], "pagination": {"style": "offset"}},
    )

    found = release_tags.find_by_version("acme", "1.0.0")

    assert found.id == "tag-1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")
    assert "version=1.0.0" in responses.calls[0].request.url


@responses.activate
def test_create(release_tags: ReleaseTags) -> None:
    responses.post(f"{BASE}/", json={"id": "tag-1", "version": "1.0.0"}, status=201)

    created = release_tags.create("acme", CreateReleaseTag(version="1.0.0"))

    assert created.id == "tag-1"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_update_uses_the_tag_uuid(release_tags: ReleaseTags) -> None:
    responses.patch(f"{BASE}/tag-1/", json={"id": "tag-1", "version": "1.0.1"})

    updated = release_tags.update("acme", "tag-1", UpdateReleaseTag(version="1.0.1"))

    assert updated.version == "1.0.1"
    assert responses.calls[0].request.url == f"{BASE}/tag-1/"


@responses.activate
def test_delete_returns_none(release_tags: ReleaseTags) -> None:
    responses.delete(f"{BASE}/tag-1/", status=204)

    assert release_tags.delete("acme", "tag-1") is None
    assert responses.calls[0].request.url == f"{BASE}/tag-1/"
