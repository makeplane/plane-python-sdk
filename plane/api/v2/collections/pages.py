"""Collection pages (api_v2) -- page membership and search on a wiki collection.
**`search` is confirmed unreliable**: it collides with the collection list filter,
404ing as if `collection_id` didn't exist (plane-ee bug)."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.collections import (
    CollectionPageSearch,
    CollectionPagesManage,
    CollectionPagesManageResult,
)
from .._kernel.resource import V2Resource

__all__ = ["CollectionPages"]


class CollectionPages(
    V2Resource[CollectionPageSearch, CollectionPagesManage, CollectionPagesManage]
):
    path = "/workspaces/{slug}/collections/{collection_id}/"
    model = CollectionPageSearch
    operations = {
        "search": "collections_pages_search",
        "manage": "collections_pages",
    }

    def manage(
        self, collection_id: str, data: CollectionPagesManage
    ) -> CollectionPagesManageResult:
        """Bulk add/remove pages from a collection."""
        payload = self.transport.request(
            "POST",
            f"{self._collection_url(collection_id=collection_id)}pages/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return CollectionPagesManageResult.model_validate(payload)

    def search(
        self,
        collection_id: str,
        *,
        search: str | None = None,
        fields: Sequence[str] | None = None,
    ) -> builtins.list[CollectionPageSearch]:
        """Lite rows for pages NOT already in this collection -- see the module
        docstring for the confirmed live server bug around `search`."""
        base = self._collection_url(collection_id=collection_id)
        payload = self.transport.request(
            "GET",
            f"{base}pages-search/",
            params=self._query({"search": search, "fields": fields}, action="search"),
        )
        return [CollectionPageSearch.model_validate(row) for row in payload]
