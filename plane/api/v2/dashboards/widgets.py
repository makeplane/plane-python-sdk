"""Dashboard widgets (api_v2) -- the charts on a dashboard, always addressed under it.

Every call answers 404 when the dashboard is missing or not visible to the caller, or when the
widget belongs to a different dashboard. `chart` is the widget's data, computed from the current
work items with the dashboard's and the widget's saved filters; `charts` is every widget's first
page in one call.

Which widget filter a chart applies follows its `last_used_filter`: `filters` for `rich_filters`
(the server default), `pql_filters.stripped` for `pql_filters`. `rich_filters` is never read."""

from __future__ import annotations

import builtins
import json
from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.dashboards import (
    CreateWidget,
    UpdateWidget,
    Widget,
    WidgetChart,
    WidgetChartResult,
    WidgetChartResultList,
)
from .._generated.constants import (
    WidgetsCreateField,
    WidgetsListField,
    WidgetsListFilters,
    WidgetsListOrderBy,
    WidgetsPartialUpdateField,
    WidgetsRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource

__all__ = ["Widgets"]


class Widgets(V2Resource[Widget, CreateWidget, UpdateWidget]):
    path = "/workspaces/{slug}/dashboards/{dashboard_id}/widgets/"
    model = Widget
    operations = {
        "list": "widgets_list",
        "retrieve": "widgets_retrieve",
        "create": "widgets_create",
        "update": "widgets_partial_update",
        "delete": "widgets_destroy",
        "chart": "widgets_chart",
        "charts": "widgets_charts",
    }
    extra_paths = {"charts": "/workspaces/{slug}/dashboards/{dashboard_id}/widgets/charts/"}

    def list(
        self,
        slug: str,
        dashboard: str,
        *,
        fields: Sequence[WidgetsListField] | None = None,
        order_by: WidgetsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WidgetsListFilters],
    ) -> Page[Widget]:
        """One page of the dashboard's widgets, with their settings and grid positions."""
        return self._list(
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
            dashboard_id=dashboard,
        )

    def iterate(
        self,
        slug: str,
        dashboard: str,
        *,
        fields: Sequence[WidgetsListField] | None = None,
        order_by: WidgetsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WidgetsListFilters],
    ) -> Iterator[Widget]:
        """Every widget on the dashboard, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
            dashboard_id=dashboard,
        )

    def retrieve(
        self,
        slug: str,
        dashboard: str,
        widget: str,
        *,
        fields: Sequence[WidgetsRetrieveField] | None = None,
    ) -> Widget:
        """The widget's settings only; its data is `chart`."""
        return self._retrieve(
            pk=widget, params={"fields": fields}, slug=slug, dashboard_id=dashboard
        )

    def create(
        self,
        slug: str,
        dashboard: str,
        data: CreateWidget,
        *,
        fields: Sequence[WidgetsCreateField] | None = None,
    ) -> Widget:
        return self._create(data, params={"fields": fields}, slug=slug, dashboard_id=dashboard)

    def update(
        self,
        slug: str,
        dashboard: str,
        widget: str,
        data: UpdateWidget,
        *,
        fields: Sequence[WidgetsPartialUpdateField] | None = None,
    ) -> Widget:
        """Change only the fields set on `data`; a field set to `None` is sent as `null` and
        clears it."""
        payload = self.transport.request(
            "PATCH",
            self._detail_url(widget, "update", slug=slug, dashboard_id=dashboard),
            params=self._query({"fields": fields}, action="update"),
            # Not `_update`'s `exclude_none`: that would drop the `None` a caller sets to clear.
            json=data.model_dump(mode="json", exclude_unset=True),
        )
        return Widget.model_validate(payload)

    def delete(self, slug: str, dashboard: str, widget: str) -> None:
        return self._delete(pk=widget, slug=slug, dashboard_id=dashboard)

    def chart(
        self,
        slug: str,
        dashboard: str,
        widget: str,
        *,
        page: int | None = None,
        column_page: int | None = None,
        row_ids: Sequence[str] | None = None,
    ) -> WidgetChart:
        """The data the widget displays; the shape depends on its chart type. It applies the
        widget's `filters` or `pql_filters` per `last_used_filter`, never `rich_filters`.

        `page` pages the rows (buckets, groups, counters) of a paginated chart type; the page size
        is the chart's own `config` setting. `column_page` and `row_ids` are `TABLE_CHART` only:
        pass the `group_by_id`s already on screen as `row_ids` to load another column page for the
        same rows without ranking them again. A parameter the chart type doesn't read is ignored.
        """
        return self._custom_action(
            "chart",
            model=WidgetChart,
            method="GET",
            pk=widget,
            params={
                "page": page,
                "column_page": column_page,
                # The API reads a JSON array here, not the comma-joined list `_query` builds.
                "row_ids": json.dumps(list(row_ids)) if row_ids is not None else None,
            },
            slug=slug,
            dashboard_id=dashboard,
        )

    def charts(
        self,
        slug: str,
        dashboard: str,
        *,
        widget_ids: Sequence[str] | None = None,
    ) -> builtins.list[WidgetChartResult]:
        """The first page of every widget's chart data, in layout order, in one call; or only the
        widgets in `widget_ids` (ids not on this dashboard are skipped). An empty `widget_ids`
        returns `[]` without a request.

        The call itself succeeds even when some widgets fail: each failing widget's entry has
        `chart=None` and the `status` and `error` body its own `chart` call would have answered
        with (e.g. 402 for a chart type not on the plan), and the other widgets still carry their
        data. Like `chart`, it never reads `rich_filters`. Page further with `chart`."""
        if widget_ids is not None and len(widget_ids) == 0:
            return []
        return self._custom_action(
            "charts",
            model=WidgetChartResultList,
            method="GET",
            params={"widget_ids": widget_ids},
            slug=slug,
            dashboard_id=dashboard,
        ).data
