from __future__ import annotations

from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.collections import (
    AddCollectionPages,
    CollectionPage,
    CollectionPageSearchResult,
    PaginatedCollectionPageResponse,
    UpdateCollectionPage,
)
from plane.models.query_params import CollectionPageQueryParams


class CollectionPages(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
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

    def add(
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

    def search(
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

    def update(
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

    def remove(self, workspace_slug: str, collection_id: str, page_collection_id: str) -> None:
        """Remove a page from a collection (does not delete the page itself).

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            page_collection_id: UUID of the page-collection membership row
        """
        return self._delete(
            f"{workspace_slug}/collections/{collection_id}/pages/{page_collection_id}"
        )
