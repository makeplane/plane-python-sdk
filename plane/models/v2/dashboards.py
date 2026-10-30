"""Dashboard and widget models for api_v2. A dashboard is a workspace-level page of charts; a
widget is one chart on it. Every read field but `id` is optional."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

DashboardAccess = Literal[0, 1]  # 0 = Private, 1 = Public

# Every chart type a stored widget can carry, including legacy ones the API no longer creates.
WidgetChartType = Literal[
    "BAR_CHART",
    "LINE_CHART",
    "AREA_CHART",
    "PIE_CHART",
    "DONUT_CHART",
    "NUMBER",
    "TABLE_CHART",
    "RICH_TEXT",
    "WORK_ITEMS_TABLE",
    "ASSIGNED_WORK_ITEMS_TABLE",
    "WORK_ITEMS_STATISTICS",
    "WORK_ITEM_TYPE_PROGRESS",
    "WORK_ITEMS_CREATED_VS_RESOLVED",
    "WORK_ITEMS_SMART_COUNTER",
    "WORK_ITEMS_SMART_GAUGE",
    "CYCLE_PROGRESS_BAR",
    "CYCLE_BURN_DOWN_CHART",
    "ACTIVE_CYCLE_PROGRESS_BAR",
    "INTAKE_VOLUME_BY_SOURCE",
    "INTAKE_ITEMS_AGEING",
    "INTAKE_ACCEPT_VS_DECLINE_AVERAGE",
    "INTAKE_ACCEPT_VS_DECLINE",
    "INTAKE_BREAKDOWN",
]
# The chart types a create or update accepts.
WidgetWriteChartType = Literal[
    "BAR_CHART",
    "LINE_CHART",
    "AREA_CHART",
    "PIE_CHART",
    "DONUT_CHART",
    "NUMBER",
    "TABLE_CHART",
    "WORK_ITEMS_TABLE",
    "ASSIGNED_WORK_ITEMS_TABLE",
    "WORK_ITEMS_STATISTICS",
    "WORK_ITEM_TYPE_PROGRESS",
    "WORK_ITEMS_SMART_COUNTER",
    "WORK_ITEMS_SMART_GAUGE",
    "CYCLE_PROGRESS_BAR",
    "ACTIVE_CYCLE_PROGRESS_BAR",
    "INTAKE_VOLUME_BY_SOURCE",
    "INTAKE_ITEMS_AGEING",
    "INTAKE_ACCEPT_VS_DECLINE_AVERAGE",
    "INTAKE_ACCEPT_VS_DECLINE",
    "INTAKE_BREAKDOWN",
]
WidgetChartModel = Literal["BASIC", "STACKED", "GROUPED", "MULTI_LINE", "COMPARISON", "PROGRESS"]
WidgetLastUsedFilter = Literal["pql_filters", "rich_filters"]
WidgetDateGrouping = Literal["DAY", "WEEK", "MONTH", "YEAR"]
WidgetMetric = Literal[
    "WORK_ITEM_COUNT",
    "ESTIMATE_POINT_COUNT",
    "PENDING_WORK_ITEM_COUNT",
    "COMPLETED_WORK_ITEM_COUNT",
    "IN_PROGRESS_WORK_ITEM_COUNT",
    "WORK_ITEM_DUE_THIS_WEEK_COUNT",
    "WORK_ITEM_DUE_TODAY_COUNT",
    "BLOCKED_WORK_ITEM_COUNT",
]


# -- Dashboards ---------------------------------------------------------------------


class Dashboard(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    access: DashboardAccess | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    filters: dict[str, Any] | None = None
    is_published: bool | None = None
    is_shared: bool | None = None
    logo_props: dict[str, Any] | None = None
    name: str | None = None
    owned_by_id: str | None = None
    pql_filters: dict[str, Any] | None = None
    project_ids: list[str] | None = None
    updated_at: datetime | None = None
    updated_by_id: str | None = None


class CreateDashboard(BaseModel):
    """POST body. `pql_filters` is `{"raw": "<PQL>", "stripped": "<PQL>"}`; `filters` is a filter
    object such as `{"priority__in": "urgent"}`. Both are validated on save."""

    model_config = ConfigDict(extra="ignore")

    name: str = Field(min_length=1, max_length=255)
    access: DashboardAccess | None = None
    project_ids: list[str] | None = None
    pql_filters: dict[str, Any] | None = None
    filters: dict[str, Any] | None = None
    logo_props: dict[str, Any] | None = None


class UpdateDashboard(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT. `project_ids` replaces the whole list."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    access: DashboardAccess | None = None
    project_ids: list[str] | None = None
    pql_filters: dict[str, Any] | None = None
    filters: dict[str, Any] | None = None
    logo_props: dict[str, Any] | None = None


class CopyDashboard(BaseModel):
    """POST body for `copy` -- every field optional; each one sent replaces the copied value.
    `name` defaults to `"<source name> (Copy)"` server-side."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    access: DashboardAccess | None = None
    project_ids: list[str] | None = None
    pql_filters: dict[str, Any] | None = None
    filters: dict[str, Any] | None = None
    logo_props: dict[str, Any] | None = None


class WidgetType(BaseModel):
    """One row of `Dashboards.widget_types`. A type with `available=False` isn't on the
    workspace's plan and answers 402 on create and on `chart`."""

    model_config = ConfigDict(extra="allow")

    chart_type: str
    name: str | None = None
    chart_models: list[str] | None = None
    available: bool | None = None


class WidgetTypeList(BaseModel):
    """The `widget-types/` envelope, unwrapped by `Dashboards.widget_types`."""

    model_config = ConfigDict(extra="allow")

    data: list[WidgetType] = []


# -- Widgets ------------------------------------------------------------------------


class Widget(BaseModel):
    """For axis charts the axis fields are mirrored into `config`."""

    model_config = ConfigDict(extra="allow")

    id: str
    chart_model: WidgetChartModel | None = None
    chart_type: WidgetChartType | None = None
    config: dict[str, Any] | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    dashboard_id: str | None = None
    filters: dict[str, Any] | None = None
    group_by: str | None = None
    height: int | None = None
    last_used_filter: WidgetLastUsedFilter | None = None
    name: str | None = None
    pql_filters: dict[str, Any] | None = None
    rich_filters: dict[str, Any] | None = None
    updated_at: datetime | None = None
    updated_by_id: str | None = None
    width: int | None = None
    x_axis_coord: int | None = None
    x_axis_date_grouping: WidgetDateGrouping | None = None
    x_axis_property: str | None = None
    y_axis_coord: int | None = None
    y_axis_metric: WidgetMetric | None = None


class CreateWidget(BaseModel):
    """POST body. Checked against its chart type before it's saved: a missing required setting or
    a model the chart type doesn't support is refused with 400. `x_axis_property`/`group_by` take
    an axis property (`PRIORITY`, `STATE_GROUPS`, ...) or a custom property as `cp_<id>`.
    Set `last_used_filter="pql_filters"` when sending `pql_filters`."""

    model_config = ConfigDict(extra="ignore")

    name: str = Field(min_length=1, max_length=255)
    chart_type: WidgetWriteChartType
    chart_model: WidgetChartModel
    config: dict[str, Any] | None = None
    x_axis_property: str | None = None
    x_axis_date_grouping: WidgetDateGrouping | None = None
    y_axis_metric: WidgetMetric | None = None
    group_by: str | None = None
    width: int | None = Field(default=None, ge=0)
    height: int | None = Field(default=None, ge=0)
    x_axis_coord: int | None = Field(default=None, ge=0)
    y_axis_coord: int | None = Field(default=None, ge=0)
    pql_filters: dict[str, Any] | None = None
    filters: dict[str, Any] | None = None
    rich_filters: dict[str, Any] | None = None
    last_used_filter: WidgetLastUsedFilter | None = None


class UpdateWidget(BaseModel):
    """PATCH body -- every field optional. A change that would leave the widget unable to show
    data is refused with 400 and nothing is saved."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = Field(default=None, min_length=1, max_length=255)
    chart_type: WidgetWriteChartType | None = None
    chart_model: WidgetChartModel | None = None
    config: dict[str, Any] | None = None
    x_axis_property: str | None = None
    x_axis_date_grouping: WidgetDateGrouping | None = None
    y_axis_metric: WidgetMetric | None = None
    group_by: str | None = None
    width: int | None = Field(default=None, ge=0)
    height: int | None = Field(default=None, ge=0)
    x_axis_coord: int | None = Field(default=None, ge=0)
    y_axis_coord: int | None = Field(default=None, ge=0)
    pql_filters: dict[str, Any] | None = None
    filters: dict[str, Any] | None = None
    rich_filters: dict[str, Any] | None = None
    last_used_filter: WidgetLastUsedFilter | None = None


# -- Chart data ---------------------------------------------------------------------


class WidgetChart(BaseModel):
    """A widget's chart data. The shape depends on the chart type, so only the keys most charts
    share are declared; every other key (`x_axis_schema_key`, `group_keys`, `columns`, `value`,
    `results`, ...) is kept and readable as an attribute or via `model_dump()`.

    `schema` maps the ids in `data` to display details, keyed by entity (`state`, `priority`,
    ...). The pagination fields are present only on paginated chart types."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    chart_schema: dict[str, Any] | None = Field(default=None, alias="schema")
    data: Any = None
    total_count: int | None = None
    total_pages: int | None = None
    page: int | None = None
    per_page: int | None = None
    next_page: int | None = None
    prev_page: int | None = None


class WidgetChartResult(BaseModel):
    """One widget's entry in `Widgets.charts`: `chart` on success (`status` 200), otherwise
    `error` (a problem-details body) with that error's `status`."""

    model_config = ConfigDict(extra="allow")

    widget_id: str
    chart_type: str | None = None
    status: int | None = None
    chart: WidgetChart | None = None
    error: dict[str, Any] | None = None


class WidgetChartResultList(BaseModel):
    """The `charts/` envelope, unwrapped by `Widgets.charts`."""

    model_config = ConfigDict(extra="allow")

    data: list[WidgetChartResult] = []
