"""Pages (api_v2) -- project-scoped (`ProjectPages`) and workspace-scoped wiki
(`WikiPages`) pages; same shape, different path, neither offers upsert/bulk.
A wiki page can belong to a `Collection` (`collection_id`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.pages import CreatePage, UpdatePage
from ...models.v2.pages import Page as PageModel
from ._kernel.errors import MultipleMatchesFound, NoMatchFound
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource

__all__ = ["ProjectPages", "WikiPages"]


class ProjectPages(V2Resource[PageModel, CreatePage, UpdatePage]):
    path = "/workspaces/{slug}/projects/{project_id}/pages/"
    model = PageModel
    operations = {
        "list": "project_pages_list",
        "retrieve": "project_pages_retrieve",
        "create": "project_pages_create",
        "update": "project_pages_partial_update",
        "delete": "project_pages_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[PageModel]:
        """One page of pages in this project."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[PageModel]:
        """Every page in this project, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        page_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        return self._retrieve(pk=page_id, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> PageModel:
        """The one page with this name; raises if none or several match.

        Filters client-side: no `?name=` in the golden; live it returned every page (confirmed)."""
        matches = [row for row in self.iterate() if row.name == name]
        if not matches:
            raise NoMatchFound(f"No ProjectPages matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def create(self, data: CreatePage) -> PageModel:
        return self._create(data)

    def update(self, page_id: str, data: UpdatePage) -> PageModel:
        return self._update(data, pk=page_id)

    def delete(self, page_id: str) -> None:
        return self._delete(pk=page_id)


class WikiPages(V2Resource[PageModel, CreatePage, UpdatePage]):
    """Workspace-scoped wiki pages (`is_global`). Same shape as `ProjectPages`,
    a different path -- no project id anywhere. Reached as `ws.wiki.pages`."""

    path = "/workspaces/{slug}/pages/"
    model = PageModel
    operations = {
        "list": "workspace_pages_list",
        "retrieve": "workspace_pages_retrieve",
        "create": "workspace_pages_create",
        "update": "workspace_pages_partial_update",
        "delete": "workspace_pages_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[PageModel]:
        """One page of workspace wiki pages."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[PageModel]:
        """Every workspace wiki page, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        page_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        return self._retrieve(pk=page_id, params={"fields": fields, "expand": expand})

    def find_by_name(self, name: str) -> PageModel:
        """The one wiki page with this name; raises if none or several match.

        Filters client-side -- see `ProjectPages.find_by_name` (same confirmed gap)."""
        matches = [row for row in self.iterate() if row.name == name]
        if not matches:
            raise NoMatchFound(f"No WikiPages matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def create(self, data: CreatePage) -> PageModel:
        """Create a workspace wiki page. Omitting `data.collection_id` auto-assigns
        the default (public) collection (confirmed live) -- a private page needs an
        explicit private `collection_id`."""
        return self._create(data)

    def update(self, page_id: str, data: UpdatePage) -> PageModel:
        return self._update(data, pk=page_id)

    def delete(self, page_id: str) -> None:
        return self._delete(pk=page_id)
