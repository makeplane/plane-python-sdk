"""`Collections` against a real server, reached as
`client.v2.workspace(slug).wiki.collections`. Covers CRUD, `default()`, and the
`members`/`pages` sub-resources (a page belongs to only one collection, confirmed live)."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.collections import Collections
from plane.api.v2.members import WorkspaceMembers
from plane.api.v2.pages import WikiPages
from plane.client import PlaneClient
from plane.models.v2.collections import (
    CollectionMemberAdd,
    CreateCollection,
    UpdateCollection,
)
from plane.models.v2.pages import CreatePage, UpdatePage

from .helpers import unique_name


def _archive_workspace_page(workspace_pages: WikiPages, page_id: str) -> None:
    """Archives a page before deletion -- the server 400s otherwise; see `test_pages.py`."""
    workspace_pages.update(
        page_id, UpdatePage(archived_at=datetime.now(timezone.utc), is_locked=False)
    )


@pytest.fixture
def collections(client: PlaneClient, workspace_slug: str) -> Collections:
    return client.v2.workspace(workspace_slug).wiki.collections


@pytest.fixture
def workspace_pages(client: PlaneClient, workspace_slug: str) -> WikiPages:
    return client.v2.workspace(workspace_slug).wiki.pages


@pytest.fixture
def workspace_members(client: PlaneClient, workspace_slug: str) -> WorkspaceMembers:
    return client.v2.workspace(workspace_slug).members


class TestCRUD:
    def test_create_then_retrieve(self, collections: Collections) -> None:
        name = unique_name("collection")
        created = collections.create(CreateCollection(name=name))
        try:
            assert created.name == name

            fetched = collections.retrieve(created.id)
            assert fetched.id == created.id
        finally:
            collections.delete(created.id)

    def test_patch_updates_only_the_given_fields(self, collections: Collections) -> None:
        created = collections.create(CreateCollection(name=unique_name("coll")))
        try:
            new_name = unique_name("coll-renamed")
            updated = collections.update(created.id, UpdateCollection(name=new_name))
            assert updated.name == new_name
        finally:
            collections.delete(created.id)

    def test_delete_then_retrieve_404s(self, collections: Collections) -> None:
        created = collections.create(CreateCollection(name=unique_name("coll")))
        collections.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            collections.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_find_by_name(self, collections: Collections) -> None:
        name = unique_name("coll")
        created = collections.create(CreateCollection(name=name))
        try:
            assert collections.find_by_name(name).id == created.id
        finally:
            collections.delete(created.id)

    def test_default_resolves_the_workspaces_default_collection(
        self, collections: Collections
    ) -> None:
        """Every workspace has exactly one default (General) collection --
        confirmed live: a fresh page with no `collection_id` always lands in
        one (see the module docstring's API-quirk note)."""
        default = collections.default()
        assert default.is_default is True


class TestPagesSubResource:
    def test_pages_add_then_remove(
        self,
        collections: Collections,
        workspace_pages: WikiPages,
    ) -> None:
        collection = collections.create(CreateCollection(name=unique_name("coll")))
        # `collection_id` at create time, not `pages.add(...)` afterward -- see
        # the module docstring's API quirk note.
        page = workspace_pages.create(
            CreatePage(name=unique_name("coll-page"), collection_id=collection.id)
        )
        try:
            after_create = collections.retrieve(collection.id)
            assert page.id in (after_create.page_ids or [])

            removed = collections.pages.remove(collection.id, [page.id])
            assert page.id in removed

            after_remove = collections.retrieve(collection.id)
            assert page.id not in (after_remove.page_ids or [])

            # The page now has no active collection at all, so `add` genuinely
            # has somewhere to insert into (no unique-constraint conflict).
            added = collections.pages.add(collection.id, [page.id])
            assert page.id in added

            after_add = collections.retrieve(collection.id)
            assert page.id in (after_add.page_ids or [])
        finally:
            _archive_workspace_page(workspace_pages, page.id)
            workspace_pages.delete(page.id)
            collections.delete(collection.id)

    def test_pages_search_returns_a_plain_list(
        self,
        collections: Collections,
        workspace_pages: WikiPages,
    ) -> None:
        """`pages-search` returns a bare JSON array of pages NOT yet in the
        collection (confirmed live) and caps out at a fixed default limit rather
        than paginating; the collection's own name overlaps the search term too."""
        page_name = unique_name("coll-page")
        collection = collections.create(CreateCollection(name=f"coll-{page_name}"))
        page = workspace_pages.create(CreatePage(name=page_name))
        try:
            results = collections.pages.search(collection.id, search=page_name)
            assert isinstance(results, list)
            assert any(row.id == page.id for row in results)
        finally:
            _archive_workspace_page(workspace_pages, page.id)
            workspace_pages.delete(page.id)
            collections.delete(collection.id)


class TestMembersSubResource:
    def test_members_list_returns_a_plain_list(self, collections: Collections) -> None:
        """Pins the contract question flagged in the module docstring: this
        parses the payload as a bare JSON array, not an envelope."""
        created = collections.create(CreateCollection(name=unique_name("coll")))
        try:
            members = collections.members.list(created.id)
            assert isinstance(members, list)
        finally:
            collections.delete(created.id)

    def test_members_add_then_remove(
        self,
        collections: Collections,
        workspace_members: WorkspaceMembers,
    ) -> None:
        """Requires at least one workspace member besides the API principal --
        skips if the target workspace has none (a bare-minimum dev workspace
        might not)."""
        roster = workspace_members.list().data
        if not roster:
            pytest.skip("workspace has no members to grant collection access to")
        member_id = roster[0].member_id
        assert member_id is not None

        created = collections.create(CreateCollection(name=unique_name("coll")))
        try:
            added = collections.members.add(
                created.id, [CollectionMemberAdd(member_id=member_id, access=0)]
            )
            assert member_id in added

            removed = collections.members.remove(created.id, [member_id])
            assert member_id in removed
        finally:
            collections.delete(created.id)
