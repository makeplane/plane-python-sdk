"""Dashboards (api_v2) -- workspace-level pages of charts built from the work items in one or more
projects. A dashboard's charts are its `.widgets`.

A dashboard is visible to its owner, to everyone in the workspace when public (`access=1`), and to
members it was shared with; one the caller can't see answers 404, never 403. Guests can't use
dashboards.

A fetched row (`retrieve`/`create`/`update`/`copy`, and every row in a `list` page) comes back as
a `LoadedDashboard`, which reaches `dashboard.widgets.list()` without repeating
`slug`/`dashboard`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.dashboards import (
    CopyDashboard,
    CreateDashboard,
    Dashboard,
    UpdateDashboard,
    WidgetType,
    WidgetTypeList,
)
from .._generated.constants import (
    DashboardsCopyField,
    DashboardsCreateField,
    DashboardsListField,
    DashboardsListFilters,
    DashboardsListOrderBy,
    DashboardsPartialUpdateField,
    DashboardsRetrieveField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.dashboard import LoadedDashboard
from .widgets import Widgets

__all__ = ["Dashboards", "Widgets"]


class Dashboards(
    V2Resource[Dashboard, CreateDashboard, UpdateDashboard], LoadsNavigableRows[LoadedDashboard]
):
    path = "/workspaces/{slug}/dashboards/"
    model = Dashboard
    loaded_model = LoadedDashboard
    loaded_names = ("slug", "dashboard")
    operations = {
        "list": "dashboards_list",
        "retrieve": "dashboards_retrieve",
        "create": "dashboards_create",
        "update": "dashboards_partial_update",
        "delete": "dashboards_destroy",
        "copy": "dashboards_copy",
        "widget_types": "dashboards_widget_types",
    }
    extra_paths = {"widget_types": "/workspaces/{slug}/dashboards/widget-types/"}

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.widgets = Widgets(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[DashboardsListField] | None = None,
        order_by: DashboardsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[DashboardsListFilters],
    ) -> Page[LoadedDashboard]:
        """One page of the dashboards the caller can see, newest first by default."""
        page = self._list(
            params={
                "fields": fields,
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
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[DashboardsListField] | None = None,
        order_by: DashboardsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[DashboardsListFilters],
    ) -> Iterator[LoadedDashboard]:
        """Every dashboard the caller can see, following pages automatically."""
        rows = self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        dashboard: str,
        *,
        fields: Sequence[DashboardsRetrieveField] | None = None,
    ) -> LoadedDashboard:
        row = self._retrieve(pk=dashboard, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def create(
        self,
        slug: str,
        data: CreateDashboard,
        *,
        fields: Sequence[DashboardsCreateField] | None = None,
    ) -> LoadedDashboard:
        """Create an empty dashboard owned by the caller."""
        row = self._create(data, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        dashboard: str,
        data: UpdateDashboard,
        *,
        fields: Sequence[DashboardsPartialUpdateField] | None = None,
    ) -> LoadedDashboard:
        """Change only the fields sent. Making a dashboard public (`access=1`) removes its shared
        members; only the owner, or an admin on a public dashboard, can change `access`."""
        row = self._update(data, pk=dashboard, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, dashboard: str) -> None:
        """Delete the dashboard and remove it from every user's favorites. Its public link stops
        serving straight away."""
        return self._delete(pk=dashboard, slug=slug)

    def copy(
        self,
        slug: str,
        dashboard: str,
        data: CopyDashboard | None = None,
        *,
        fields: Sequence[DashboardsCopyField] | None = None,
    ) -> LoadedDashboard:
        """A new dashboard owned by the caller with the source's settings, projects, filters and
        every widget. Shared members and the public link aren't copied. Each field in `data`
        replaces the copied value."""
        row = self._action(
            "copy",
            pk=dashboard,
            data=data or CopyDashboard(),
            params={"fields": fields},
            slug=slug,
        )
        return self._load(row, slug, fields=fields)

    def widget_types(self, slug: str) -> builtins.list[WidgetType]:
        """Every widget type a dashboard can hold, the chart models each accepts, and whether the
        workspace's plan includes it (`available`)."""
        return self._custom_action(
            "widget_types", model=WidgetTypeList, method="GET", slug=slug
        ).data
