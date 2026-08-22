"""Collection members (api_v2) -- membership on a wiki collection.

`list` is unpaginated: the golden documents a bare `CollectionMember`, parsed as a plain array."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.collections import (
    CollectionMember,
    CollectionMembersManage,
    CollectionMembersManageResult,
)
from .._kernel.resource import V2Resource

__all__ = ["CollectionMembers"]


class CollectionMembers(
    V2Resource[CollectionMember, CollectionMembersManage, CollectionMembersManage]
):
    path = "/workspaces/{slug}/collections/{collection_id}/members/"
    model = CollectionMember
    operations = {
        "list": "collections_members_list",
        "manage": "collections_members",
    }

    def list(
        self,
        collection_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> builtins.list[CollectionMember]:
        """Every member row on a collection. Unpaginated -- see the module
        docstring for why this parses a plain array rather than an envelope."""
        payload = self.transport.request(
            "GET",
            self._collection_url(collection_id=collection_id),
            params=self._query({"fields": fields, "expand": expand}, action="list"),
        )
        return [CollectionMember.model_validate(row) for row in payload]

    def manage(
        self, collection_id: str, data: CollectionMembersManage
    ) -> CollectionMembersManageResult:
        """Bulk grant/revoke workspace-member access to a collection."""
        payload = self.transport.request(
            "POST",
            self._collection_url(collection_id=collection_id),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return CollectionMembersManageResult.model_validate(payload)
