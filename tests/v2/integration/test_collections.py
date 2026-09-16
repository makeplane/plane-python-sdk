"""`Collections` against a real server, reached as `client.v2.workspaces.wiki.collections`.
Covers CRUD, `default()`, and the `members`/`pages` sub-resources (a page belongs to
only one collection, confirmed live).

Both ways in, and the seam is `wiki`: it is a grouping node holding no `V2Resource`
base of its own, so it consumes no path id and a loaded workspace deliberately does
not reach it -- the collection and wiki-page CRUD below is flat, with the slug passed.
Once a collection *row* exists, its members and pages hang off it
(`collection.pages.add([...])`), which is where the collection id comes from."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from plane.api.v2 import LoadedWorkspace, PlaneAPIError
from plane.api.v2.collections import Collections
from plane.api.v2.pages import WikiPages
from plane.client import PlaneClient
from plane.models.v2.collections import (
    CollectionMemberAdd,
    CreateCollection,
    UpdateCollection,
)
from plane.models.v2.pages import CreatePage, UpdatePage

from ._guard import skip_absent_capability
from .helpers import unique_name


def _archive_workspace_page(workspace_pages: WikiPages, workspace_slug: str, page_id: str) -> None:
    """Archives a page before deletion -- the server 400s otherwise; see `test_pages.py`."""
    workspace_pages.update(
        workspace_slug,
        page_id,
        UpdatePage(archived_at=datetime.now(timezone.utc), is_locked=False),
    )


@pytest.fixture
def collections(client: PlaneClient) -> Collections:
    return client.v2.workspaces.wiki.collections


@pytest.fixture
def workspace_pages(client: PlaneClient) -> WikiPages:
    return client.v2.workspaces.wiki.pages


class TestCRUD:
    def test_create_then_retrieve(self, collections: Collections, workspace_slug: str) -> None:
        name = unique_name("collection")
        created = collections.create(workspace_slug, CreateCollection(name=name))
        try:
            assert created.name == name

            fetched = collections.retrieve(workspace_slug, created.id)
            assert fetched.id == created.id
        finally:
            collections.delete(workspace_slug, created.id)

    def test_patch_updates_only_the_given_fields(
        self, collections: Collections, workspace_slug: str
    ) -> None:
        created = collections.create(workspace_slug, CreateCollection(name=unique_name("coll")))
        try:
            new_name = unique_name("coll-renamed")
            updated = collections.update(
                workspace_slug, created.id, UpdateCollection(name=new_name)
            )
            assert updated.name == new_name
        finally:
            collections.delete(workspace_slug, created.id)

    def test_delete_then_retrieve_404s(self, collections: Collections, workspace_slug: str) -> None:
        created = collections.create(workspace_slug, CreateCollection(name=unique_name("coll")))
        collections.delete(workspace_slug, created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            collections.retrieve(workspace_slug, created.id)
        assert exc_info.value.status == 404

    def test_find_by_name(self, collections: Collections, workspace_slug: str) -> None:
        name = unique_name("coll")
        created = collections.create(workspace_slug, CreateCollection(name=name))
        try:
            assert collections.find_by_name(workspace_slug, name).id == created.id
        finally:
            collections.delete(workspace_slug, created.id)

    def test_default_resolves_the_workspaces_default_collection(
        self, collections: Collections, workspace_slug: str
    ) -> None:
        """Every workspace has exactly one default (General) collection --
        confirmed live: a fresh page with no `collection_id` always lands in
        one (see the module docstring's API-quirk note)."""
        default = collections.default(workspace_slug)
        assert default.is_default is True


class TestPagesSubResource:
    def test_pages_add_then_remove(
        self,
        collections: Collections,
        workspace_pages: WikiPages,
        workspace_slug: str,
    ) -> None:
        collection = collections.create(workspace_slug, CreateCollection(name=unique_name("coll")))
        # `collection_id` at create time, not `pages.add(...)` afterward -- see
        # the module docstring's API quirk note.
        page = workspace_pages.create(
            workspace_slug, CreatePage(name=unique_name("coll-page"), collection_id=collection.id)
        )
        try:
            after_create = collections.retrieve(workspace_slug, collection.id)
            assert page.id in (after_create.page_ids or [])

            removed = collection.pages.remove([page.id])
            assert page.id in removed

            after_remove = collections.retrieve(workspace_slug, collection.id)
            assert page.id not in (after_remove.page_ids or [])

            # The page now has no active collection at all, so `add` genuinely
            # has somewhere to insert into (no unique-constraint conflict).
            added = collection.pages.add([page.id])
            assert page.id in added

            after_add = collections.retrieve(workspace_slug, collection.id)
            assert page.id in (after_add.page_ids or [])
        finally:
            _archive_workspace_page(workspace_pages, workspace_slug, page.id)
            workspace_pages.delete(workspace_slug, page.id)
            collections.delete(workspace_slug, collection.id)

    def test_pages_search_returns_a_plain_list(
        self,
        collections: Collections,
        workspace_pages: WikiPages,
        workspace_slug: str,
    ) -> None:
        """`pages-search` returns a bare JSON array of pages NOT yet in the
        collection (confirmed live) and caps out at a fixed default limit rather
        than paginating; the collection's own name overlaps the search term too."""
        page_name = unique_name("coll-page")
        collection = collections.create(workspace_slug, CreateCollection(name=f"coll-{page_name}"))
        page = workspace_pages.create(workspace_slug, CreatePage(name=page_name))
        try:
            results = collection.pages.search(search=page_name)
            assert isinstance(results, list)
            assert any(row.id == page.id for row in results)
        finally:
            _archive_workspace_page(workspace_pages, workspace_slug, page.id)
            workspace_pages.delete(workspace_slug, page.id)
            collections.delete(workspace_slug, collection.id)


class TestMembersSubResource:
    def test_members_list_returns_a_plain_list(
        self, collections: Collections, workspace_slug: str
    ) -> None:
        """Pins the contract question flagged in the module docstring: this
        parses the payload as a bare JSON array, not an envelope."""
        created = collections.create(workspace_slug, CreateCollection(name=unique_name("coll")))
        try:
            members = created.members.list()
            assert isinstance(members, list)
        finally:
            collections.delete(workspace_slug, created.id)

    def test_members_add_then_remove(
        self,
        collections: Collections,
        workspace: LoadedWorkspace,
        workspace_slug: str,
    ) -> None:
        """Requires at least one workspace member besides the API principal --
        skips if the target workspace has none (a bare-minimum dev workspace
        might not)."""
        roster = workspace.members.list().data
        if not roster:
            skip_absent_capability("workspace has no members to grant collection access to")
        member_id = roster[0].member_id
        assert member_id is not None

        created = collections.create(workspace_slug, CreateCollection(name=unique_name("coll")))
        try:
            added = created.members.add([CollectionMemberAdd(member_id=member_id, access=0)])
            assert member_id in added

            removed = created.members.remove([member_id])
            assert member_id in removed
        finally:
            collections.delete(workspace_slug, created.id)
