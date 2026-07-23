"""Unit tests for Collections API resource (smoke tests with real HTTP requests).

Requires the target workspace to have the WORKSPACE_PAGES (and, for the
private-collection cases, PRIVATE_COLLECTIONS) feature flags enabled.
"""

import time

from plane.client import PlaneClient
from plane.models.collections import (
    AddCollectionPages,
    Collection,
    CreateCollection,
    PaginatedCollectionPageResponse,
    UpdateCollection,
    UpdateCollectionMember,
    UpdateCollectionPage,
)
from plane.models.pages import CreatePage
from plane.models.query_params import CollectionPageQueryParams


def _collection_name(prefix: str) -> str:
    return f"{prefix} {int(time.time() * 1000)}"


class TestCollectionsAPI:
    """Test Collections CRUD."""

    def test_collection_crud(self, client: PlaneClient, workspace_slug: str) -> None:
        created = client.collections.create(
            workspace_slug, CreateCollection(name=_collection_name("SDK Collection"))
        )
        assert created is not None
        assert created.id is not None

        try:
            collections = client.collections.list(workspace_slug)
            assert isinstance(collections, list)
            assert any(c.id == created.id for c in collections)

            retrieved = client.collections.retrieve(workspace_slug, created.id)
            assert isinstance(retrieved, Collection)
            assert retrieved.id == created.id

            updated = client.collections.update(
                workspace_slug,
                created.id,
                UpdateCollection(name=f"{created.name} (updated)", sort_order=25000),
            )
            assert updated.name == f"{created.name} (updated)"
        finally:
            client.collections.delete(workspace_slug, created.id, archive_pages=False)

        collections_after = client.collections.list(workspace_slug)
        assert not any(c.id == created.id for c in collections_after)


class TestCollectionPagesAPI:
    """Test page-in-collection operations: add, list, search, move, remove."""

    def test_add_list_search_move_and_remove_pages(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        source = client.collections.create(
            workspace_slug, CreateCollection(name=_collection_name("Source Collection"))
        )
        target = client.collections.create(
            workspace_slug, CreateCollection(name=_collection_name("Target Collection"))
        )
        page = client.pages.create_workspace_page(
            workspace_slug,
            CreatePage(
                name=_collection_name("Collection Page"),
                description_html="<p>collection sdk test</p>",
            ),
        )

        try:
            search_results = client.collections.pages.search(
                workspace_slug, source.id, search=page.name
            )
            assert any(r.id == page.id for r in search_results)

            added = client.collections.pages.add(
                workspace_slug, source.id, AddCollectionPages(page_ids=[page.id])
            )
            assert any(pc.page == page.id for pc in added)

            listed = client.collections.pages.list(workspace_slug, source.id)
            assert isinstance(listed, PaginatedCollectionPageResponse)
            matching = [row for row in listed.results if row.page and row.page.get("id") == page.id]
            assert len(matching) == 1
            page_collection_id = matching[0].page_collection_id
            assert page_collection_id is not None

            moved = client.collections.pages.update(
                workspace_slug,
                source.id,
                page_collection_id,
                UpdateCollectionPage(collection=target.id),
            )
            assert moved.collection == target.id

            client.collections.pages.remove(workspace_slug, target.id, page_collection_id)
            listed_after = client.collections.pages.list(workspace_slug, target.id)
            assert not any(
                row.page and row.page.get("id") == page.id for row in listed_after.results
            )
        finally:
            try:
                client.pages.delete_workspace_page(workspace_slug, page.id)
            except Exception:
                pass
            for collection in (source, target):
                try:
                    client.collections.delete(workspace_slug, collection.id, archive_pages=False)
                except Exception:
                    pass

    def test_create_page_in_collection_and_sub_page(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Create page directly via CreatePage(collection_id=...), plus a sub-page."""
        collection = client.collections.create(
            workspace_slug, CreateCollection(name=_collection_name("Parent Collection"))
        )
        parent_page = None
        child_page = None
        try:
            parent_page = client.pages.create_workspace_page(
                workspace_slug,
                CreatePage(
                    name=_collection_name("Parent Page"),
                    description_html="<p>parent</p>",
                    collection_id=collection.id,
                ),
            )
            assert parent_page is not None

            child_page = client.pages.create_workspace_page(
                workspace_slug,
                CreatePage(
                    name=_collection_name("Child Page"),
                    description_html="<p>child</p>",
                    parent_id=parent_page.id,
                ),
            )
            assert child_page is not None

            # The unfiltered listing returns only root-branch pages; sub-pages are
            # listed under their parent via the parent_id filter.
            listed = client.collections.pages.list(workspace_slug, collection.id)
            root_page_ids = {row.page.get("id") for row in listed.results if row.page}
            assert parent_page.id in root_page_ids
            assert child_page.id not in root_page_ids

            children = client.collections.pages.list(
                workspace_slug,
                collection.id,
                params=CollectionPageQueryParams(parent_id=parent_page.id),
            )
            child_page_ids = {row.page.get("id") for row in children.results if row.page}
            assert child_page.id in child_page_ids
        finally:
            for created_page in (child_page, parent_page):
                if created_page is not None:
                    try:
                        client.pages.delete_workspace_page(workspace_slug, created_page.id)
                    except Exception:
                        pass
            try:
                client.collections.delete(workspace_slug, collection.id, archive_pages=False)
            except Exception:
                pass


class TestCollectionMembersAPI:
    """Test collection membership CRUD (private collections).

    Creating a private collection auto-adds its creator as an EDIT member
    (server-side), so this test exercises list/update against that
    auto-created row rather than adding a second membership for the same
    user (which the API rejects as a duplicate).
    """

    def test_collection_member_crud(self, client: PlaneClient, workspace_slug: str) -> None:
        collection = client.collections.create(
            workspace_slug,
            CreateCollection(name=_collection_name("Private Collection"), access=1),
        )
        try:
            members = client.collections.members.list(workspace_slug, collection.id)
            assert isinstance(members, list)
            assert len(members) == 1
            owner_member = members[0]
            assert owner_member.access == 2  # EDIT, auto-assigned to the creator

            updated_member = client.collections.members.update(
                workspace_slug,
                collection.id,
                owner_member.id,
                UpdateCollectionMember(access=0),
            )
            assert updated_member.access == 0
        finally:
            try:
                client.collections.delete(workspace_slug, collection.id, archive_pages=False)
            except Exception:
                pass
