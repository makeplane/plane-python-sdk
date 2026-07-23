from __future__ import annotations

from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.collections import (
    CollectionMember,
    CreateCollectionMember,
    UpdateCollectionMember,
)


class CollectionMembers(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, collection_id: str) -> list[CollectionMember]:
        """List members of a (typically private) collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
        """
        response = self._get(f"{workspace_slug}/collections/{collection_id}/members")
        return [CollectionMember.model_validate(item) for item in response]

    def add(
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

    def update(
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

    def remove(self, workspace_slug: str, collection_id: str, member_id: str) -> None:
        """Remove a member from a collection.

        Args:
            workspace_slug: The workspace slug identifier
            collection_id: UUID of the collection
            member_id: UUID of the CollectionMember row (not the user id)
        """
        return self._delete(f"{workspace_slug}/collections/{collection_id}/members/{member_id}")
