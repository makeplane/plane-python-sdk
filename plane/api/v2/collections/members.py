"""Collection members (api_v2) -- membership on a wiki collection.

`list` is unpaginated: the golden documents a bare `CollectionMember`, parsed as a plain array."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.collections import (
    CollectionMember,
    CollectionMemberAdd,
    CollectionMembersManage,
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
        "bridge": "collections_members",
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

    def add(self, collection_id: str, members: Sequence[CollectionMemberAdd]) -> builtins.list[str]:
        """Grant (or update) access for 1..100 workspace members on this
        collection; returns the member ids actually added or updated."""
        return self._bridge(key="add", ids=members, collection_id=collection_id)

    def remove(self, collection_id: str, user_ids: Sequence[str]) -> builtins.list[str]:
        """Revoke access for 1..100 members from this collection; returns the
        member ids actually removed (idempotent no-ops omitted)."""
        return self._bridge(key="remove", ids=user_ids, collection_id=collection_id)
