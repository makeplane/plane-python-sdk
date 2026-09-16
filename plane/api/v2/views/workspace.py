"""Workspace-scoped saved views (api_v2). Project is NULL for these rows --
different path template than `ProjectViews`, same read/write shape."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.views import CreateView, UpdateView, View
from .._generated.constants import (
    WorkspaceViewsCreateField,
    WorkspaceViewsListField,
    WorkspaceViewsListFilters,
    WorkspaceViewsListOrderBy,
    WorkspaceViewsPartialUpdateField,
    WorkspaceViewsRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


class WorkspaceViews(V2Resource[View, CreateView, UpdateView]):
    path = "/workspaces/{slug}/views/"
    model = View
    operations = {
        "list": "workspace_views_list",
        "retrieve": "workspace_views_retrieve",
        "create": "workspace_views_create",
        "update": "workspace_views_partial_update",
        "delete": "workspace_views_destroy",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceViewsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceViewsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceViewsListFilters],
    ) -> Page[View]:
        """One page of workspace-level views. `**filters` covers `access`,
        `is_locked`, `name`, `owned_by_id`."""
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
        fields: Sequence[WorkspaceViewsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceViewsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceViewsListFilters],
    ) -> Iterator[View]:
        """Every workspace-level view, following pages automatically."""
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
        view: str,
        *,
        fields: Sequence[WorkspaceViewsRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> View:
        return self._retrieve(pk=view, params={"fields": fields, "expand": expand}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateView,
        *,
        fields: Sequence[WorkspaceViewsCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> View:
        return self._create(data, params={"fields": fields, "expand": expand}, slug=slug)

    def update(
        self,
        slug: str,
        view: str,
        data: UpdateView,
        *,
        fields: Sequence[WorkspaceViewsPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> View:
        return self._update(data, pk=view, params={"fields": fields, "expand": expand}, slug=slug)

    def delete(self, slug: str, view: str) -> None:
        return self._delete(pk=view, slug=slug)
