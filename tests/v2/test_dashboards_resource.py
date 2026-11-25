"""Offline coverage for `Dashboards` and its `widgets` child: CRUD, `copy`, `widget_types`, the
`chart`/`charts` reads, and navigation from a fetched dashboard and workspace."""

import json
from urllib.parse import parse_qs, urlparse

import pytest
import responses
from pydantic import ValidationError

from plane.api.v2 import PlaneAPIError, V2Namespace
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.dashboards import Dashboards
from plane.config import Configuration
from plane.models.v2.dashboards import (
    CopyDashboard,
    CreateDashboard,
    CreateWidget,
    Dashboard,
    UpdateDashboard,
    UpdateWidget,
    Widget,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/dashboards"
EMPTY_PAGE = {"data": [], "pagination": {"style": "offset"}, "total_count": 0}


@pytest.fixture
def dashboards(config: Configuration) -> Dashboards:
    return Dashboards(V2Transport(config))


def _query(call_index: int = 0) -> dict[str, list[str]]:
    return parse_qs(urlparse(responses.calls[call_index].request.url).query)


# -- Dashboards ---------------------------------------------------------------------


@responses.activate
def test_list_sends_filters_and_order_by(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "d1", "name": "Engineering overview", "access": 1}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = dashboards.list("acme", access=1, search="eng", order_by="-updated_at", per_page=10)

    assert page.total_count == 1
    assert page.data[0].name == "Engineering overview"
    assert _query() == {
        "access": ["1"],
        "search": ["eng"],
        "order_by": ["-updated_at"],
        "per_page": ["10"],
    }


def test_list_rejects_an_unknown_order_by(dashboards: Dashboards) -> None:
    with pytest.raises(ValueError, match="Unknown order_by"):
        dashboards.list("acme", order_by="priority")  # type: ignore[arg-type]


@responses.activate
def test_iterate_follows_pages(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "d1"}], "next": 1, "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "d2"}], "next": None, "pagination": {"style": "offset"}},
    )

    rows = list(dashboards.iterate("acme", per_page=1))

    assert [row.id for row in rows] == ["d1", "d2"]
    assert rows[1].widgets._ids == ("acme", "d2")


@responses.activate
def test_create_sends_the_body(dashboards: Dashboards) -> None:
    responses.post(f"{BASE}/", json={"id": "d1", "name": "Eng", "access": 1}, status=201)

    created = dashboards.create(
        "acme",
        CreateDashboard(
            name="Eng",
            access=1,
            project_ids=["p1"],
            pql_filters={"json": {}, "stripped": 'priority = "high"'},
        ),
    )

    assert created.id == "d1"
    assert json.loads(responses.calls[0].request.body) == {
        "name": "Eng",
        "access": 1,
        "project_ids": ["p1"],
        "pql_filters": {"json": {}, "stripped": 'priority = "high"'},
    }


def test_create_requires_a_name() -> None:
    with pytest.raises(ValueError):
        CreateDashboard(name="")


@responses.activate
def test_retrieve_passes_fields(dashboards: Dashboards) -> None:
    responses.get(f"{BASE}/d1/", json={"id": "d1", "name": "Eng"})

    row = dashboards.retrieve("acme", "d1", fields=["id", "name"])

    assert row.name == "Eng"
    assert _query() == {"fields": ["id,name"]}


@responses.activate
def test_update_uses_patch_and_sends_only_set_fields(dashboards: Dashboards) -> None:
    responses.patch(f"{BASE}/d1/", json={"id": "d1", "name": "Eng (Q4)"})

    updated = dashboards.update("acme", "d1", UpdateDashboard(name="Eng (Q4)"))

    assert updated.name == "Eng (Q4)"
    assert json.loads(responses.calls[0].request.body) == {"name": "Eng (Q4)"}


@responses.activate
def test_delete_returns_none(dashboards: Dashboards) -> None:
    responses.delete(f"{BASE}/d1/", status=204)

    assert dashboards.delete("acme", "d1") is None


@responses.activate
def test_copy_without_a_body_posts_an_empty_object(dashboards: Dashboards) -> None:
    responses.post(f"{BASE}/d1/copy/", json={"id": "d2", "name": "Eng (Copy)"}, status=201)

    copied = dashboards.copy("acme", "d1")

    assert copied.id == "d2"
    assert json.loads(responses.calls[0].request.body) == {}


@responses.activate
def test_copy_overrides_the_copied_fields(dashboards: Dashboards) -> None:
    responses.post(f"{BASE}/d1/copy/", json={"id": "d2", "name": "Mine"}, status=201)

    copied = dashboards.copy("acme", "d1", CopyDashboard(name="Mine", access=0))

    assert json.loads(responses.calls[0].request.body) == {"name": "Mine", "access": 0}
    assert copied.widgets._ids == ("acme", "d2")


@responses.activate
def test_widget_types_unwraps_the_envelope(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/widget-types/",
        json={
            "data": [
                {
                    "chart_type": "BAR_CHART",
                    "name": "Bar Chart",
                    "chart_models": ["BASIC", "STACKED", "GROUPED"],
                    "available": True,
                },
                {
                    "chart_type": "NUMBER",
                    "name": "Number",
                    "chart_models": ["BASIC"],
                    "available": False,
                },
            ]
        },
    )

    types = dashboards.widget_types("acme")

    assert [(row.chart_type, row.available) for row in types] == [
        ("BAR_CHART", True),
        ("NUMBER", False),
    ]
    assert types[0].chart_models == ["BASIC", "STACKED", "GROUPED"]


# -- Widgets ------------------------------------------------------------------------


@responses.activate
def test_widgets_list_sends_filters(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/d1/widgets/",
        json={
            "data": [{"id": "w1", "name": "By priority", "chart_type": "BAR_CHART"}],
            "pagination": {"style": "offset"},
        },
    )

    page = dashboards.widgets.list("acme", "d1", chart_type="BAR_CHART", order_by="created_at")

    assert page.data[0].chart_type == "BAR_CHART"
    assert _query() == {"chart_type": ["BAR_CHART"], "order_by": ["created_at"]}


@responses.activate
def test_widgets_create_sends_the_body(dashboards: Dashboards) -> None:
    responses.post(
        f"{BASE}/d1/widgets/",
        json={
            "id": "w1",
            "dashboard_id": "d1",
            "chart_type": "BAR_CHART",
            "chart_model": "STACKED",
            "config": {"x_axis_property": "PRIORITY", "group_by": "STATE_GROUPS"},
        },
        status=201,
    )

    widget = dashboards.widgets.create(
        "acme",
        "d1",
        CreateWidget(
            name="By priority",
            chart_type="BAR_CHART",
            chart_model="STACKED",
            x_axis_property="PRIORITY",
            y_axis_metric="WORK_ITEM_COUNT",
            group_by="STATE_GROUPS",
            width=6,
            height=4,
        ),
    )

    assert widget.dashboard_id == "d1"
    assert widget.config == {"x_axis_property": "PRIORITY", "group_by": "STATE_GROUPS"}
    assert json.loads(responses.calls[0].request.body) == {
        "name": "By priority",
        "chart_type": "BAR_CHART",
        "chart_model": "STACKED",
        "x_axis_property": "PRIORITY",
        "y_axis_metric": "WORK_ITEM_COUNT",
        "group_by": "STATE_GROUPS",
        "width": 6,
        "height": 4,
    }


def test_widgets_create_rejects_a_chart_type_the_api_does_not_create() -> None:
    with pytest.raises(ValueError):
        CreateWidget(name="Notes", chart_type="RICH_TEXT", chart_model="BASIC")  # type: ignore[arg-type]


@responses.activate
def test_widgets_retrieve_update_delete(dashboards: Dashboards) -> None:
    responses.get(f"{BASE}/d1/widgets/w1/", json={"id": "w1", "name": "By priority"})
    responses.patch(f"{BASE}/d1/widgets/w1/", json={"id": "w1", "x_axis_coord": 6})
    responses.delete(f"{BASE}/d1/widgets/w1/", status=204)

    assert dashboards.widgets.retrieve("acme", "d1", "w1").name == "By priority"
    updated = dashboards.widgets.update("acme", "d1", "w1", UpdateWidget(x_axis_coord=6))
    assert updated.x_axis_coord == 6
    assert json.loads(responses.calls[1].request.body) == {"x_axis_coord": 6}
    assert dashboards.widgets.delete("acme", "d1", "w1") is None


@responses.activate
def test_chart_keeps_the_chart_specific_keys(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/d1/widgets/w1/chart/",
        json={
            "schema": {"priority": {"high": {"id": "high", "name": "High"}}},
            "total_count": 1,
            "total_pages": 1,
            "page": 1,
            "per_page": 20,
            "next_page": None,
            "prev_page": None,
            "data": [{"key": "high", "count": 2, "groups": {}, "projects": {}}],
            "x_axis_schema_key": "priority",
            "group_keys": [],
        },
    )

    chart = dashboards.widgets.chart("acme", "d1", "w1")

    assert chart.chart_schema == {"priority": {"high": {"id": "high", "name": "High"}}}
    assert chart.data[0]["count"] == 2
    assert chart.total_pages == 1
    assert chart.x_axis_schema_key == "priority"  # type: ignore[attr-defined]
    assert chart.model_dump(by_alias=True)["schema"]["priority"]["high"]["name"] == "High"
    assert urlparse(responses.calls[0].request.url).query == ""


@responses.activate
def test_chart_encodes_row_ids_as_a_json_array(dashboards: Dashboards) -> None:
    responses.get(f"{BASE}/d1/widgets/w1/chart/", json={"schema": {}, "data": []})

    dashboards.widgets.chart(
        "acme", "d1", "w1", page=2, column_page=2, row_ids=["backlog", "started"]
    )

    assert _query() == {
        "page": ["2"],
        "column_page": ["2"],
        "row_ids": ['["backlog", "started"]'],
    }


@responses.activate
def test_charts_returns_each_widgets_result(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/d1/widgets/charts/",
        json={
            "data": [
                {
                    "widget_id": "w1",
                    "chart_type": "NUMBER",
                    "status": 200,
                    "chart": {"schema": {}, "value": 10, "y_axis_metric": "WORK_ITEM_COUNT"},
                },
                {
                    "widget_id": "w2",
                    "chart_type": "TABLE_CHART",
                    "status": 402,
                    "error": {"code": "payment_required", "detail": "Upgrade."},
                },
            ]
        },
    )

    results = dashboards.widgets.charts("acme", "d1", widget_ids=["w1", "w2"])

    assert _query() == {"widget_ids": ["w1,w2"]}
    assert results[0].chart is not None
    assert results[0].chart.value == 10  # type: ignore[attr-defined]
    assert results[1].chart is None
    assert results[1].status == 402
    assert results[1].error == {"code": "payment_required", "detail": "Upgrade."}


def test_widget_reads_the_free_text_the_server_stores() -> None:
    widget = Widget.model_validate(
        {
            "id": "w",
            "last_used_filter": "",
            "x_axis_date_grouping": "",
            "y_axis_metric": "SOME_NEW_METRIC",
        }
    )

    assert widget.last_used_filter == ""
    assert widget.x_axis_date_grouping == ""
    assert widget.y_axis_metric == "SOME_NEW_METRIC"


@responses.activate
def test_widgets_list_keeps_a_page_with_blank_choice_fields(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/d1/widgets/",
        json={
            "data": [
                {"id": "w1", "chart_type": "NUMBER", "last_used_filter": ""},
                {"id": "w2", "chart_type": "BAR_CHART", "last_used_filter": "pql_filters"},
            ],
            "pagination": {"style": "offset"},
        },
    )

    page = dashboards.widgets.list("acme", "d1")

    assert [row.last_used_filter for row in page.data] == ["", "pql_filters"]


def test_dashboard_reads_a_legacy_access_value() -> None:
    # `2` ("shared") was retired without a data migration, so old rows can still carry it.
    assert Dashboard.model_validate({"id": "d", "access": 2}).access == 2


@responses.activate
def test_dashboards_list_keeps_a_page_with_a_legacy_access_value(dashboards: Dashboards) -> None:
    responses.get(
        BASE + "/",
        json={
            "data": [{"id": "d1", "access": 1}, {"id": "d2", "access": 2}],
            "pagination": {"style": "offset"},
        },
    )

    page = dashboards.list("acme")

    assert [row.access for row in page.data] == [1, 2]


def test_widget_reads_a_chart_type_the_sdk_does_not_know_yet() -> None:
    widget = Widget.model_validate(
        {"id": "w", "chart_type": "SOME_NEW_CHART", "chart_model": "SOME_MODEL"}
    )

    assert widget.chart_type == "SOME_NEW_CHART"
    assert widget.chart_model == "SOME_MODEL"


def test_dashboard_write_models_keep_the_access_choices() -> None:
    for model in (CreateDashboard, UpdateDashboard, CopyDashboard):
        with pytest.raises(ValidationError):
            model.model_validate({"name": "D", "access": 2})


def test_write_models_keep_the_fixed_choices() -> None:
    with pytest.raises(ValueError):
        UpdateWidget(last_used_filter="")  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        CreateWidget(
            name="n", chart_type="NUMBER", chart_model="BASIC", y_axis_metric="NOPE"  # type: ignore[arg-type]
        )


@responses.activate
def test_widgets_update_sends_explicit_none_to_clear(dashboards: Dashboards) -> None:
    responses.patch(f"{BASE}/d1/widgets/w1/", json={"id": "w1", "group_by": None})

    dashboards.widgets.update(
        "acme",
        "d1",
        "w1",
        UpdateWidget(
            chart_model="BASIC",
            group_by=None,
            x_axis_property=None,
            x_axis_date_grouping=None,
            y_axis_metric=None,
        ),
    )

    assert json.loads(responses.calls[0].request.body) == {
        "chart_model": "BASIC",
        "group_by": None,
        "x_axis_property": None,
        "x_axis_date_grouping": None,
        "y_axis_metric": None,
    }


@responses.activate
def test_widgets_update_passes_fields(dashboards: Dashboards) -> None:
    responses.patch(f"{BASE}/d1/widgets/w1/", json={"id": "w1", "name": "Renamed"})

    updated = dashboards.widgets.update(
        "acme", "d1", "w1", UpdateWidget(name="Renamed"), fields=["id", "name"]
    )

    assert updated.name == "Renamed"
    assert _query() == {"fields": ["id,name"]}
    assert json.loads(responses.calls[0].request.body) == {"name": "Renamed"}


@responses.activate
def test_widgets_create_with_pql_filters(dashboards: Dashboards) -> None:
    pql = {"json": {}, "stripped": 'priority = "high"'}
    responses.post(
        f"{BASE}/d1/widgets/",
        json={
            "id": "w1",
            "chart_type": "NUMBER",
            "chart_model": "BASIC",
            "pql_filters": pql,
            "last_used_filter": "pql_filters",
        },
        status=201,
    )

    widget = dashboards.widgets.create(
        "acme",
        "d1",
        CreateWidget(
            name="High priority",
            chart_type="NUMBER",
            chart_model="BASIC",
            y_axis_metric="WORK_ITEM_COUNT",
            pql_filters=pql,
            last_used_filter="pql_filters",
        ),
    )

    assert widget.last_used_filter == "pql_filters"
    assert widget.pql_filters == pql
    assert json.loads(responses.calls[0].request.body) == {
        "name": "High priority",
        "chart_type": "NUMBER",
        "chart_model": "BASIC",
        "y_axis_metric": "WORK_ITEM_COUNT",
        "pql_filters": pql,
        "last_used_filter": "pql_filters",
    }


@responses.activate
def test_chart_pages_a_table_chart(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/d1/widgets/w1/chart/",
        json={
            "schema": {},
            "data": [{"group_by_id": "backlog"}],
            "total_count": 25,
            "total_pages": 3,
            "page": 2,
            "per_page": 10,
            "next_page": 3,
            "prev_page": 1,
            "columns": [{"id": "high"}],
        },
    )

    chart = dashboards.widgets.chart("acme", "d1", "w1", page=2, column_page=3)

    assert _query() == {"page": ["2"], "column_page": ["3"]}
    assert (chart.page, chart.next_page, chart.prev_page, chart.total_pages) == (2, 3, 1, 3)
    assert chart.columns == [{"id": "high"}]  # type: ignore[attr-defined]


def test_charts_with_no_widget_ids_makes_no_request(dashboards: Dashboards) -> None:
    with responses.RequestsMock() as mocked:
        assert dashboards.widgets.charts("acme", "d1", widget_ids=[]) == []
        assert len(mocked.calls) == 0


# -- Navigation ---------------------------------------------------------------------


@responses.activate
def test_a_fetched_dashboard_reaches_its_widgets(dashboards: Dashboards) -> None:
    responses.get(f"{BASE}/d1/", json={"id": "d1", "name": "Eng"})
    responses.get(f"{BASE}/d1/widgets/", json=EMPTY_PAGE)
    responses.get(f"{BASE}/d1/widgets/w1/chart/", json={"schema": {}, "value": 3})

    dashboard = dashboards.retrieve("acme", "d1")
    dashboard.widgets.list()
    chart = dashboard.widgets.chart("w1")

    assert responses.calls[1].request.url == f"{BASE}/d1/widgets/"
    assert chart.value == 3  # type: ignore[attr-defined]


@responses.activate
def test_a_fetched_workspace_reaches_its_dashboards(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/", json={"id": "ws1", "slug": "acme"}
    )
    responses.get(f"{BASE}/", json=EMPTY_PAGE)

    workspace = V2Namespace(config).workspaces.retrieve("acme")
    workspace.dashboards.list()

    assert responses.calls[1].request.url == f"{BASE}/"


@responses.activate
def test_widgets_update_does_not_send_none_where_the_server_refuses_null(
    dashboards: Dashboards,
) -> None:
    # A pass-through helper sets every field it takes; only the axis fields may go out as null.
    responses.patch(f"{BASE}/d1/widgets/w1/", json={"id": "w1", "width": 4})

    dashboards.widgets.update(
        "acme",
        "d1",
        "w1",
        UpdateWidget(name=None, config=None, filters=None, width=4, group_by=None),
    )

    assert json.loads(responses.calls[0].request.body) == {"width": 4, "group_by": None}


def test_a_bare_string_is_refused_for_id_lists(dashboards: Dashboards) -> None:
    with pytest.raises(TypeError):
        dashboards.widgets.chart("acme", "d1", "w1", row_ids="backlog")
    with pytest.raises(TypeError):
        dashboards.widgets.charts("acme", "d1", widget_ids="w1")


@responses.activate
def test_charts_without_widget_ids_sends_no_filter(dashboards: Dashboards) -> None:
    responses.get(f"{BASE}/d1/widgets/charts/", json={"data": []})

    assert dashboards.widgets.charts("acme", "d1") == []
    assert "widget_ids" not in _query()


@responses.activate
def test_a_chart_error_is_raised_as_plane_api_error(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/d1/widgets/w1/chart/",
        status=402,
        json={"type": "payment_required", "code": "payment_required", "detail": "Upgrade."},
        content_type="application/problem+json",
    )

    with pytest.raises(PlaneAPIError) as exc_info:
        dashboards.widgets.chart("acme", "d1", "w1")

    assert exc_info.value.status_code == 402


@responses.activate
def test_widgets_iterate_follows_pages(dashboards: Dashboards) -> None:
    responses.get(
        f"{BASE}/d1/widgets/",
        json={"data": [{"id": "w1"}], "next": 1, "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{BASE}/d1/widgets/",
        json={"data": [{"id": "w2"}], "next": None, "pagination": {"style": "offset"}},
    )

    assert [row.id for row in dashboards.widgets.iterate("acme", "d1", per_page=1)] == ["w1", "w2"]


@responses.activate
def test_chart_sends_the_null_row_in_row_ids(dashboards: Dashboards) -> None:
    responses.get(f"{BASE}/d1/widgets/w1/chart/", json={"schema": {}, "data": [], "columns": []})

    dashboards.widgets.chart("acme", "d1", "w1", column_page=2, row_ids=["u1", None])

    assert json.loads(_query()["row_ids"][0]) == ["u1", None]
