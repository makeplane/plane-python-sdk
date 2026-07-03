"""Unit tests for the Workload API resource (smoke tests with real HTTP
requests, plus offline model-validation tests)."""

import time

import pytest
from pydantic import ValidationError

from plane.client import PlaneClient
from plane.errors.errors import WorkloadParentHasChildrenError
from plane.models.projects import Project
from plane.models.work_items import CreateWorkItem
from plane.models.workload import (
    UpdateWorkloadEstimate,
    WorkloadEstimateDetail,
    WorkloadMatrixResponse,
    WorkloadQueryParams,
    WorkloadRollup,
)


class TestWorkloadEstimateAPI:
    """Test the single work-item estimate GET/PUT/DELETE endpoints."""

    @pytest.fixture
    def work_item(self, client: PlaneClient, workspace_slug: str, project: Project):
        """Create a leaf work item and yield it, then delete it."""
        work_item = client.work_items.create(
            workspace_slug,
            project.id,
            CreateWorkItem(name=f"Workload Test Leaf {int(time.time() * 1000)}"),
        )
        yield work_item
        try:
            client.work_items.delete(workspace_slug, project.id, work_item.id)
        except Exception:
            pass

    def test_get_estimate_unset_returns_none_hours(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """A leaf work item with no stored estimate returns hours=None."""
        estimate = client.workload.get_estimate(workspace_slug, project.id, work_item.id)
        assert isinstance(estimate, WorkloadEstimateDetail)
        assert estimate.hours is None
        assert estimate.is_parent is False

    def test_update_and_get_estimate(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Setting an estimate on a leaf work item persists and round-trips."""
        updated = client.workload.update_estimate(
            workspace_slug,
            project.id,
            work_item.id,
            UpdateWorkloadEstimate(hours=4.5),
        )
        assert isinstance(updated, WorkloadEstimateDetail)
        assert updated.hours == 4.5
        assert updated.work_item_id == work_item.id

        fetched = client.workload.get_estimate(workspace_slug, project.id, work_item.id)
        assert fetched.hours == 4.5
        assert fetched.is_parent is False
        assert fetched.rollup is None

    def test_delete_estimate(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item
    ) -> None:
        """Deleting a stored estimate clears it back to unset."""
        client.workload.update_estimate(
            workspace_slug, project.id, work_item.id, UpdateWorkloadEstimate(hours=2)
        )
        result = client.workload.delete_estimate(workspace_slug, project.id, work_item.id)
        assert result is None

        fetched = client.workload.get_estimate(workspace_slug, project.id, work_item.id)
        assert fetched.hours is None


class TestWorkloadParentRollup:
    """Test parent-rollup behavior: single-GET, PUT-block, bulk endpoints."""

    @pytest.fixture
    def parent_with_child(self, client: PlaneClient, workspace_slug: str, project: Project):
        """Create a parent work item with one countable child estimate, yield
        (parent, child), then delete both."""
        timestamp = int(time.time() * 1000)
        parent = client.work_items.create(
            workspace_slug,
            project.id,
            CreateWorkItem(name=f"Workload Test Parent {timestamp}"),
        )
        child = client.work_items.create(
            workspace_slug,
            project.id,
            CreateWorkItem(
                name=f"Workload Test Child {timestamp}",
                parent=parent.id,
            ),
        )
        client.workload.update_estimate(
            workspace_slug, project.id, child.id, UpdateWorkloadEstimate(hours=3)
        )
        yield parent, child
        for item_id in (child.id, parent.id):
            try:
                client.work_items.delete(workspace_slug, project.id, item_id)
            except Exception:
                pass

    def test_parent_single_get_has_rollup_and_null_hours(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        parent_with_child,
    ) -> None:
        parent, _child = parent_with_child
        estimate = client.workload.get_estimate(workspace_slug, project.id, parent.id)
        assert estimate.hours is None
        assert estimate.is_parent is True
        assert estimate.rollup is not None
        assert isinstance(estimate.rollup, WorkloadRollup)
        assert estimate.rollup.leaf_count >= 1
        assert estimate.rollup.hours >= 3

    def test_put_on_parent_raises_typed_error(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        parent_with_child,
    ) -> None:
        parent, _child = parent_with_child
        with pytest.raises(WorkloadParentHasChildrenError) as exc_info:
            client.workload.update_estimate(
                workspace_slug, project.id, parent.id, UpdateWorkloadEstimate(hours=1)
            )
        assert exc_info.value.error_code == "PARENT_HAS_CHILDREN"
        assert exc_info.value.status_code == 400

    def test_bulk_estimates_omits_parent(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        parent_with_child,
    ) -> None:
        parent, child = parent_with_child
        result = client.workload.list_estimates(workspace_slug, [parent.id, child.id])
        assert child.id in result
        assert result[child.id] == 3.0
        assert parent.id not in result

    def test_bulk_rollups_returns_parent_only(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        parent_with_child,
    ) -> None:
        parent, child = parent_with_child
        result = client.workload.list_rollups(workspace_slug, [parent.id, child.id])
        assert parent.id in result
        assert child.id not in result
        assert isinstance(result[parent.id], WorkloadRollup)


class TestWorkloadMatrix:
    """Test the workspace/project workload matrix endpoints."""

    def test_get_matrix_well_formed(self, client: PlaneClient, workspace_slug: str) -> None:
        """Only asserts response shape — parallel test data may pollute
        exact totals, so this does not assert on row/period values."""
        result = client.workload.get_matrix(
            workspace_slug,
            WorkloadQueryParams(
                granularity="day",
                date_from="2026-08-01",
                date_to="2026-08-31",
            ),
        )
        assert isinstance(result, WorkloadMatrixResponse)
        assert result.granularity == "day"
        assert result.date_from == "2026-08-01"
        assert result.date_to == "2026-08-31"
        assert isinstance(result.rows, list)
        assert isinstance(result.periods, list)
        assert isinstance(result.unscheduled, list)

    def test_get_project_matrix_well_formed(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        result = client.workload.get_project_matrix(
            workspace_slug,
            project.id,
            WorkloadQueryParams(
                granularity="week",
                date_from="2026-08-01",
                date_to="2026-08-31",
            ),
        )
        assert isinstance(result, WorkloadMatrixResponse)
        assert result.granularity == "week"


class TestWorkloadModels:
    """Offline Pydantic model-validation tests (no network)."""

    def test_update_workload_estimate_rejects_negative_hours(self) -> None:
        with pytest.raises(ValidationError):
            UpdateWorkloadEstimate(hours=-1)

    def test_update_workload_estimate_rejects_over_max(self) -> None:
        with pytest.raises(ValidationError):
            UpdateWorkloadEstimate(hours=10001)

    def test_update_workload_estimate_valid(self) -> None:
        data = UpdateWorkloadEstimate(hours=7.5)
        assert data.hours == 7.5

    def test_query_params_requires_granularity_and_dates(self) -> None:
        with pytest.raises(ValidationError):
            WorkloadQueryParams()

    def test_query_params_accepts_optional_filters(self) -> None:
        params = WorkloadQueryParams(
            granularity="month",
            date_from="2026-01-01",
            date_to="2026-12-31",
            project_ids=["p1", "p2"],
            assignee_ids=["a1"],
            state_group=["started", "backlog"],
        )
        assert params.project_ids == ["p1", "p2"]

    def test_estimate_detail_allows_extra_fields(self) -> None:
        detail = WorkloadEstimateDetail.model_validate(
            {"hours": None, "is_parent": True, "some_future_field": "x"}
        )
        assert detail.hours is None
        assert detail.is_parent is True
        assert detail.some_future_field == "x"

    def test_estimate_detail_maps_issue_alias_to_work_item_id(self) -> None:
        detail = WorkloadEstimateDetail.model_validate(
            {"id": "est-1", "issue": "work-item-1", "hours": 2.0}
        )
        assert detail.work_item_id == "work-item-1"

    def test_rollup_percent_none_when_hours_zero(self) -> None:
        rollup = WorkloadRollup.model_validate(
            {"hours": 0, "done_hours": 0, "percent": None, "due_date": None, "leaf_count": 0}
        )
        assert rollup.percent is None

    def test_matrix_response_defaults(self) -> None:
        matrix = WorkloadMatrixResponse.model_validate(
            {
                "granularity": "day",
                "date_from": "2026-01-01",
                "date_to": "2026-01-31",
                "periods": [],
                "rows": [],
                "unscheduled": [],
                "meta": {"issues_counted": 0},
            }
        )
        assert matrix.rows == []
        assert matrix.meta.issues_counted == 0
