"""Collections (api_v2) -- wiki collections: named groups of workspace pages
with their own membership. Golden `operationId` prefix is `pages_*`; do not
confuse this with the top-level `plane.api.v2.pages` resource."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.collections import Collection, CreateCollection, UpdateCollection
from .._generated.constants import (
    PagesCreateField,
    PagesListField,
    PagesListFilters,
    PagesListOrderBy,
    PagesPartialUpdateField,
    PagesRetrieveField,
)
from .._kernel.errors import MultipleMatchesFound, NoMatchFound
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.collection import LoadedCollection
from .members import CollectionMembers
from .pages import CollectionPages

__all__ = ["CollectionMembers", "CollectionPages", "Collections"]


class Collections(
    V2Resource[Collection, CreateCollection, UpdateCollection], LoadsNavigableRows[LoadedCollection]
):
    path = "/workspaces/{slug}/collections/"
    model = Collection
    loaded_model = LoadedCollection
    loaded_names = ("slug", "collection")
    operations = {
        "list": "pages_list",
        "retrieve": "pages_retrieve",
        "create": "pages_create",
        "update": "pages_partial_update",
        "delete": "pages_destroy",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.members = CollectionMembers(transport)
        self.pages = CollectionPages(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[PagesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: PagesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[PagesListFilters],
    ) -> Page[LoadedCollection]:
        """One page of collections in the workspace."""
        page = self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[PagesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: PagesListOrderBy | None = None,
        **filters: Unpack[PagesListFilters],
    ) -> Iterator[LoadedCollection]:
        """Every collection in the workspace, following pages automatically."""
        rows = self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        collection: str,
        *,
        fields: Sequence[PagesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedCollection:
        row = self._retrieve(pk=collection, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedCollection:
        """The one collection with this name; raises if none or several match.
        Filters client-side: no `?name=` filter; a server-side one is silently
        ignored (confirmed live)."""
        matches = [row for row in self.iterate(slug) if row.name == name]
        if not matches:
            raise NoMatchFound(f"No Collections matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def default(self, slug: str) -> LoadedCollection:
        """The workspace's default (General) collection, where a new wiki page
        lands when `CreatePage.collection_id` is omitted. Resolved via the
        golden's `?is_default=` list filter, not a client-side scan."""
        row = self._find_one(filters={"is_default": True}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateCollection,
        *,
        fields: Sequence[PagesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedCollection:
        row = self._create(data, params={"fields": fields, "expand": expand}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        collection: str,
        data: UpdateCollection,
        *,
        fields: Sequence[PagesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedCollection:
        row = self._update(
            data, pk=collection, params={"fields": fields, "expand": expand}, slug=slug
        )
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, collection: str) -> None:
        return self._delete(pk=collection, slug=slug)
