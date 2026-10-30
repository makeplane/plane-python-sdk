"""Live coverage for `client.v2.workspaces.dashboards` and its `widgets`: CRUD, `copy`,
`widget_types`, and the `chart`/`charts` reads. Gated by `FeatureFlag.DASHBOARDS` (402 when
the plan lacks it), which is a declared server-capability skip.

Widgets are reached off the fetched dashboard row (`dashboard.widgets.create(...)`), so the
dashboard id is never repeated."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from plane.api.v2 import LoadedDashboard, LoadedProject, PlaneAPIError
from plane.api.v2.dashboards import Dashboards
from plane.client import PlaneClient
from plane.models.v2.dashboards import (
    CopyDashboard,
    CreateDashboard,
    CreateWidget,
    UpdateDashboard,
    UpdateWidget,
)

from ._guard import skip_absent_capability
from .helpers import unique_name


@pytest.fixture
def dashboards(client: PlaneClient) -> Dashboards:
    return client.v2.workspaces.dashboards


@pytest.fixture
def dashboard(
    dashboards: Dashboards, workspace_slug: str, project: LoadedProject
) -> Iterator[LoadedDashboard]:
    try:
        created = dashboards.create(
            workspace_slug,
            CreateDashboard(name=unique_name("dashboard"), project_ids=[project.id]),
        )
    except PlaneAPIError as exc:
        if exc.status == 402:
            skip_absent_capability("DASHBOARDS is not enabled on this workspace's plan")
        raise
    yield created
    try:
        dashboards.delete(workspace_slug, created.id)
    except PlaneAPIError as exc:
        if exc.status != 404:
            raise


class TestDashboards:
    def test_retrieve_update_and_list(
        self, dashboards: Dashboards, dashboard: LoadedDashboard, workspace_slug: str
    ) -> None:
        fetched = dashboards.retrieve(workspace_slug, dashboard.id)
        assert fetched.name == dashboard.name

        renamed = unique_name("dashboard")
        updated = dashboards.update(workspace_slug, dashboard.id, UpdateDashboard(name=renamed))
        assert updated.name == renamed

        ids = {row.id for row in dashboards.iterate(workspace_slug, search=renamed)}
        assert dashboard.id in ids

    def test_widget_types_lists_bar_chart(
        self, dashboards: Dashboards, dashboard: LoadedDashboard, workspace_slug: str
    ) -> None:
        types = {row.chart_type: row for row in dashboards.widget_types(workspace_slug)}
        assert "BAR_CHART" in types
        assert "BASIC" in (types["BAR_CHART"].chart_models or [])

    def test_copy_carries_the_widgets(
        self, dashboards: Dashboards, dashboard: LoadedDashboard, workspace_slug: str
    ) -> None:
        dashboard.widgets.create(
            CreateWidget(
                name="Total",
                chart_type="NUMBER",
                chart_model="BASIC",
                y_axis_metric="WORK_ITEM_COUNT",
            )
        )
        copy_name = unique_name("dashboard-copy")
        copied = dashboards.copy(workspace_slug, dashboard.id, CopyDashboard(name=copy_name))
        try:
            assert copied.name == copy_name
            assert [row.name for row in copied.widgets.iterate()] == ["Total"]
        finally:
            dashboards.delete(workspace_slug, copied.id)

    def test_delete_then_retrieve_is_404(
        self, dashboards: Dashboards, dashboard: LoadedDashboard, workspace_slug: str
    ) -> None:
        dashboards.delete(workspace_slug, dashboard.id)
        with pytest.raises(PlaneAPIError) as excinfo:
            dashboards.retrieve(workspace_slug, dashboard.id)
        assert excinfo.value.status == 404


class TestWidgets:
    def test_crud_and_chart(self, dashboard: LoadedDashboard) -> None:
        widget = dashboard.widgets.create(
            CreateWidget(
                name="By priority",
                chart_type="BAR_CHART",
                chart_model="BASIC",
                x_axis_property="PRIORITY",
                y_axis_metric="WORK_ITEM_COUNT",
            )
        )
        assert widget.dashboard_id == dashboard.id

        moved = dashboard.widgets.update(widget.id, UpdateWidget(x_axis_coord=6))
        assert moved.x_axis_coord == 6

        chart = dashboard.widgets.chart(widget.id)
        assert isinstance(chart.data, list)
        assert chart.page == 1

        results = dashboard.widgets.charts(widget_ids=[widget.id])
        assert [(row.widget_id, row.status) for row in results] == [(widget.id, 200)]

        dashboard.widgets.delete(widget.id)
        assert widget.id not in {row.id for row in dashboard.widgets.iterate()}

    def test_an_invalid_widget_is_refused(self, dashboard: LoadedDashboard) -> None:
        with pytest.raises(PlaneAPIError) as excinfo:
            dashboard.widgets.create(
                CreateWidget(name="No axis", chart_type="BAR_CHART", chart_model="BASIC")
            )
        assert excinfo.value.status == 400
