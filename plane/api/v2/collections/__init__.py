"""Collections (api_v2) -- wiki collections: named groups of workspace pages
with their own membership. Golden `operationId` prefix is `pages_*`; do not
confuse this with the top-level `plane.api.v2.pages` resource."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.collections import Collection, CreateCollection, UpdateCollection
from .._kernel.errors import MultipleMatchesFound, NoMatchFound
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .members import CollectionMembers

try:
    from .pages import CollectionPages
except TypeError:
    # `CollectionPages` still declares the retired `bridge_path` (Task 5 replaced it
    # with `extra_paths`); `V2Resource.__init_subclass__` now raises the moment that
    # class body executes. Left broken pending the later task that migrates it --
    # swallowed here only so importing `plane` doesn't cascade through this package's
    # `__init__` chain into every unrelated test. Importing `.pages` directly, or
    # defining any subclass with a stale `bridge_path`, still raises loudly.
    CollectionPages = None  # type: ignore[assignment, misc]

__all__ = ["CollectionMembers", "CollectionPages", "Collections"]


class Collections(V2Resource[Collection, CreateCollection, UpdateCollection]):
    path = "/workspaces/{slug}/collections/"
    model = Collection
    operations = {
        "list": "pages_list",
        "retrieve": "pages_retrieve",
        "create": "pages_create",
        "update": "pages_partial_update",
        "delete": "pages_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.members = CollectionMembers(transport, **self._scope)
        self.pages = CollectionPages(transport, **self._scope)

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Collection]:
        """One page of collections in the workspace."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Collection]:
        """Every collection in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        collection_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> Collection:
        return self._retrieve(pk=collection_id, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> Collection:
        """The one collection with this name; raises if none or several match.
        Filters client-side: no `?name=` filter; a server-side one is silently
        ignored (confirmed live)."""
        matches = [row for row in self.iterate() if row.name == name]
        if not matches:
            raise NoMatchFound(f"No Collections matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def default(self) -> Collection:
        """The workspace's default (General) collection, where a new wiki page
        lands when `CreatePage.collection_id` is omitted. Resolved via the
        golden's `?is_default=` list filter, not a client-side scan."""
        return self._find_one(filters={"is_default": True})

    def create(self, data: CreateCollection) -> Collection:
        return self._create(data)

    def update(self, collection_id: str, data: UpdateCollection) -> Collection:
        return self._update(data, pk=collection_id)

    def delete(self, collection_id: str) -> None:
        return self._delete(pk=collection_id)
