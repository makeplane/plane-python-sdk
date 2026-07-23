from __future__ import annotations

from typing import Any

from plane.api.base_resource import BaseResource
from plane.api.collections.members import CollectionMembers
from plane.api.collections.pages import CollectionPages
from plane.models.collections import (
    Collection,
    CreateCollection,
    UpdateCollection,
)


class Collections(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.pages = CollectionPages(config)
        self.members = CollectionMembers(config)

    def list(self, workspace_slug: str) -> list[Collection]:
        """List all collections in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/collections")
        return [Collection.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreateCollection) -> Collection:
        """Create a new collection in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Collection data
        """
        response = self._post(f"{workspace_slug}/collections", data.model_dump(exclude_none=True))
        return Collection.model_validate(response)

    def retrieve(self, workspace_slug: str, collection_id: str) -> Collection:
        """Retrieve a collection by ID.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
        """
        response = self._get(f"{workspace_slug}/collections/{collection_id}")
        return Collection.model_validate(response)

    def update(self, workspace_slug: str, collection_id: str, data: UpdateCollection) -> Collection:
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

    def delete(
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
