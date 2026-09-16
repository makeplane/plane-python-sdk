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
from .._generated.constants import CollectionsMembersListField
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
        slug: str,
        collection: str,
        *,
        fields: Sequence[CollectionsMembersListField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> builtins.list[CollectionMember]:
        """Every member row on a collection. Unpaginated -- see the module
        docstring for why this parses a plain array rather than an envelope."""
        return self._custom_action_list(
            "list",
            model=self.model,
            method="GET",
            params={"fields": fields, "expand": expand},
            slug=slug,
            collection_id=collection,
        )

    def add(
        self, slug: str, collection: str, members: Sequence[CollectionMemberAdd]
    ) -> builtins.list[str]:
        """Grant (or update) access for 1..100 workspace members on this
        collection; returns the member ids actually added or updated."""
        return self._bridge(key="add", ids=members, slug=slug, collection_id=collection)

    def remove(self, slug: str, collection: str, user_ids: Sequence[str]) -> builtins.list[str]:
        """Revoke access for 1..100 members from this collection; returns the
        member ids actually removed (idempotent no-ops omitted)."""
        return self._bridge(key="remove", ids=user_ids, slug=slug, collection_id=collection)
