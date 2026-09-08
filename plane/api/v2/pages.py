"""Pages (api_v2) -- project-scoped (`ProjectPages`) and workspace-scoped wiki
(`WikiPages`) pages; same shape, different path, neither offers upsert/bulk.
A wiki page can belong to a `Collection` (`collection_id`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.pages import CreatePage, UpdatePage
from ...models.v2.pages import Page as PageModel
from ._generated.constants import (
    ProjectPagesCreateField,
    ProjectPagesListField,
    ProjectPagesListFilters,
    ProjectPagesListOrderBy,
    ProjectPagesPartialUpdateField,
    ProjectPagesRetrieveField,
    WorkspacePagesCreateField,
    WorkspacePagesListField,
    WorkspacePagesListFilters,
    WorkspacePagesListOrderBy,
    WorkspacePagesPartialUpdateField,
    WorkspacePagesRetrieveField,
)
from ._kernel.errors import MultipleMatchesFound, NoMatchFound
from ._kernel.pagination import Page, PaginateStyle
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
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectPagesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectPagesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ProjectPagesListFilters],
    ) -> Page[PageModel]:
        """One page of pages in this project."""
        return self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
            project_id=project,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[ProjectPagesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ProjectPagesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ProjectPagesListFilters],
    ) -> Iterator[PageModel]:
        """Every page in this project, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
            project_id=project,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        page: str,
        *,
        fields: Sequence[ProjectPagesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        return self._retrieve(
            pk=page, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )

    def find_by_name(self, slug: str, project: str, name: str) -> PageModel:
        """The one page with this name; raises if none or several match.

        Filters client-side: no `?name=` in the golden; live it returned every page (confirmed)."""
        matches = [row for row in self.iterate(slug, project) if row.name == name]
        if not matches:
            raise NoMatchFound(f"No ProjectPages matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def create(
        self,
        slug: str,
        project: str,
        data: CreatePage,
        *,
        fields: Sequence[ProjectPagesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        return self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )

    def update(
        self,
        slug: str,
        project: str,
        page: str,
        data: UpdatePage,
        *,
        fields: Sequence[ProjectPagesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        return self._update(
            data,
            pk=page,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )

    def delete(self, slug: str, project: str, page: str) -> None:
        return self._delete(pk=page, slug=slug, project_id=project)


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
        slug: str,
        *,
        fields: Sequence[WorkspacePagesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspacePagesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspacePagesListFilters],
    ) -> Page[PageModel]:
        """One page of workspace wiki pages."""
        return self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspacePagesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspacePagesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspacePagesListFilters],
    ) -> Iterator[PageModel]:
        """Every workspace wiki page, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        page: str,
        *,
        fields: Sequence[WorkspacePagesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        return self._retrieve(pk=page, params={"fields": fields, "expand": expand}, slug=slug)

    def find_by_name(self, slug: str, name: str) -> PageModel:
        """The one wiki page with this name; raises if none or several match.

        Filters client-side -- see `ProjectPages.find_by_name` (same confirmed gap)."""
        matches = [row for row in self.iterate(slug) if row.name == name]
        if not matches:
            raise NoMatchFound(f"No WikiPages matched name={name!r}.")
        if len(matches) > 1:
            raise MultipleMatchesFound(
                f"Multiple rows matched name={name!r}; "
                f"use the id instead, or list to see every match."
            )
        return matches[0]

    def create(
        self,
        slug: str,
        data: CreatePage,
        *,
        fields: Sequence[WorkspacePagesCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        """Create a workspace wiki page. Omitting `data.collection_id` auto-assigns
        the default (public) collection (confirmed live) -- a private page needs an
        explicit private `collection_id`."""
        return self._create(data, params={"fields": fields, "expand": expand}, slug=slug)

    def update(
        self,
        slug: str,
        page: str,
        data: UpdatePage,
        *,
        fields: Sequence[WorkspacePagesPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> PageModel:
        return self._update(data, pk=page, params={"fields": fields, "expand": expand}, slug=slug)

    def delete(self, slug: str, page: str) -> None:
        return self._delete(pk=page, slug=slug)
