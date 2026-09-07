"""Collection pages (api_v2) -- page membership and search on a wiki collection.
**`search` is confirmed unreliable**: it collides with the collection list filter,
404ing as if `collection_id` didn't exist (plane-ee bug)."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.collections import CollectionPageSearch, CollectionPagesManage
from .._kernel.resource import V2Resource

__all__ = ["CollectionPages"]


class CollectionPages(
    V2Resource[CollectionPageSearch, CollectionPagesManage, CollectionPagesManage]
):
    path = "/workspaces/{slug}/collections/{collection_id}/"
    extra_paths = {
        "add": "/workspaces/{slug}/collections/{collection_id}/pages/",
        "remove": "/workspaces/{slug}/collections/{collection_id}/pages/",
    }
    model = CollectionPageSearch
    operations = {
        "search": "collections_pages_search",
        "bridge": "collections_pages",
    }

    def add(self, collection_id: str, page_ids: Sequence[str]) -> builtins.list[str]:
        """Add 1..100 pages to this collection; returns the ids actually
        added."""
        return self._bridge(key="add", ids=page_ids, collection_id=collection_id)

    def remove(self, collection_id: str, page_ids: Sequence[str]) -> builtins.list[str]:
        """Remove 1..100 pages from this collection; returns the ids actually
        removed."""
        return self._bridge(key="remove", ids=page_ids, collection_id=collection_id)

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
