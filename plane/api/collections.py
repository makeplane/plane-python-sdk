from typing import Any

from ..models.collections import (
    AddCollectionPages,
    Collection,
    CollectionMember,
    CollectionPage,
    CollectionPageSearchResult,
    CreateCollection,
    CreateCollectionMember,
    PaginatedCollectionPageResponse,
    UpdateCollection,
    UpdateCollectionMember,
    UpdateCollectionPage,
)
from ..models.query_params import CollectionPageQueryParams
from .base_resource import BaseResource


class Collections(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    # Collections

    def list_collections(self, workspace_slug: str) -> list[Collection]:
        """List all collections in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/collections")
        return [Collection.model_validate(item) for item in response]

    def create_collection(self, workspace_slug: str, data: CreateCollection) -> Collection:
        """Create a new collection in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Collection data
        """
        response = self._post(f"{workspace_slug}/collections", data.model_dump(exclude_none=True))
        return Collection.model_validate(response)

    def retrieve_collection(self, workspace_slug: str, collection_id: str) -> Collection:
        """Retrieve a collection by ID.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
        """
        response = self._get(f"{workspace_slug}/collections/{collection_id}")
        return Collection.model_validate(response)

    def update_collection(
        self, workspace_slug: str, collection_id: str, data: UpdateCollection
    ) -> Collection:
        """Update a collection's name, logo, or sort order.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            data: Fields to update (access cannot be changed after creation)
        """
        response = self._patch(
            f"{workspace_slug}/collections/{collection_id}",
            data.model_dump(exclude_none=True),
        )
        return Collection.model_validate(response)

    def delete_collection(
        self,
        workspace_slug: str,
        collection_id: str,
        archive_pages: bool | None = None,
    ) -> None:
        """Delete a collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            archive_pages: Whether to archive the collection's pages instead of
                leaving them unfiled. Omit to use the server's default (True).
                Private collections always archive their pages regardless.
        """
        params = None
        if archive_pages is not None:
            params = {"archive_pages": "true" if archive_pages else "false"}
        return self._delete(f"{workspace_slug}/collections/{collection_id}", params=params)

    # Pages within a collection

    def list_collection_pages(
        self,
        workspace_slug: str,
        collection_id: str,
        params: CollectionPageQueryParams | None = None,
    ) -> PaginatedCollectionPageResponse:
        """List pages that belong to a collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            params: Optional search/parent_id/pagination filters
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/collections/{collection_id}/pages", params=query_params
        )
        return PaginatedCollectionPageResponse.model_validate(response)

    def add_collection_pages(
        self, workspace_slug: str, collection_id: str, data: AddCollectionPages
    ) -> list[CollectionPage]:
        """Add existing page(s) to a collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            data: Page IDs to add, with optional sort_orders/placement
        """
        response = self._post(
            f"{workspace_slug}/collections/{collection_id}/pages",
            data.model_dump(exclude_none=True),
        )
        return [CollectionPage.model_validate(item) for item in response]

    def search_addable_collection_pages(
        self, workspace_slug: str, collection_id: str, search: str | None = None
    ) -> list[CollectionPageSearchResult]:
        """Search pages that are not yet in a collection, to add them.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            search: Optional case-insensitive substring filter on page name
        """
        query_params = {"search": search} if search else None
        response = self._get(
            f"{workspace_slug}/collections/{collection_id}/pages-search",
            params=query_params,
        )
        return [CollectionPageSearchResult.model_validate(item) for item in response]

    def update_collection_page(
        self,
        workspace_slug: str,
        collection_id: str,
        page_collection_id: str,
        data: UpdateCollectionPage,
    ) -> CollectionPage:
        """Move a page to a different collection, or reorder it within the current one.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the page's current collection
            page_collection_id: UUID of the page-collection membership row
            data: `collection` to move (omit/leave unset to just reorder),
                and/or `sort_order`/`placement` to reorder
        """
        response = self._patch(
            f"{workspace_slug}/collections/{collection_id}/pages/{page_collection_id}",
            data.model_dump(exclude_none=True),
        )
        return CollectionPage.model_validate(response)

    def remove_collection_page(
        self, workspace_slug: str, collection_id: str, page_collection_id: str
    ) -> None:
        """Remove a page from a collection (does not delete the page itself).

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            page_collection_id: UUID of the page-collection membership row
        """
        return self._delete(
            f"{workspace_slug}/collections/{collection_id}/pages/{page_collection_id}"
        )

    # Collection members

    def list_collection_members(
        self, workspace_slug: str, collection_id: str
    ) -> list[CollectionMember]:
        """List members of a (typically private) collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
        """
        response = self._get(f"{workspace_slug}/collections/{collection_id}/members")
        return [CollectionMember.model_validate(item) for item in response]

    def add_collection_member(
        self, workspace_slug: str, collection_id: str, data: CreateCollectionMember
    ) -> CollectionMember:
        """Add a member to a collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            data: Member user id and access level
        """
        response = self._post(
            f"{workspace_slug}/collections/{collection_id}/members",
            data.model_dump(exclude_none=True),
        )
        return CollectionMember.model_validate(response)

    def update_collection_member(
        self,
        workspace_slug: str,
        collection_id: str,
        member_id: str,
        data: UpdateCollectionMember,
    ) -> CollectionMember:
        """Update a collection member's access level.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            member_id: UUID of the CollectionMember row (not the user id)
            data: New access level
        """
        response = self._patch(
            f"{workspace_slug}/collections/{collection_id}/members/{member_id}",
            data.model_dump(exclude_none=True),
        )
        return CollectionMember.model_validate(response)

    def remove_collection_member(
        self, workspace_slug: str, collection_id: str, member_id: str
    ) -> None:
        """Remove a member from a collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            member_id: UUID of the CollectionMember row (not the user id)
        """
        return self._delete(f"{workspace_slug}/collections/{collection_id}/members/{member_id}")
