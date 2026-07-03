from __future__ import annotations

from typing import Any

from ..errors.errors import HttpError, WorkloadParentHasChildrenError
from ..models.workload import (
    UpdateWorkloadEstimate,
    WorkloadEstimateDetail,
    WorkloadMatrixResponse,
    WorkloadQueryParams,
    WorkloadRollup,
)
from .base_resource import BaseResource

MAX_BULK_WORK_ITEM_IDS = 500


def _prepare_matrix_params(params: WorkloadQueryParams) -> dict[str, Any]:
    """Serialize :class:`WorkloadQueryParams` into HTTP query params.

    CSV-joins the list fields (``project_ids``, ``assignee_ids``,
    ``state_group``) — the API expects comma-separated strings, not
    repeated query keys.
    """
    payload: dict[str, Any] = params.model_dump(exclude_none=True)
    for key in ("project_ids", "assignee_ids", "state_group"):
        value = payload.get(key)
        if isinstance(value, list):
            payload[key] = ",".join(value)
    return payload


def _prepare_bulk_ids(work_item_ids: list[str]) -> str:
    """Validate and CSV-join a bulk ``work_item_ids`` list.

    Mirrors the server's cap/empty validation (shared by the bulk estimates
    and bulk rollups endpoints) so callers fail fast without a round trip.
    """
    if not work_item_ids:
        raise ValueError("work_item_ids must not be empty")
    if len(work_item_ids) > MAX_BULK_WORK_ITEM_IDS:
        raise ValueError(
            f"Too many work_item_ids (max {MAX_BULK_WORK_ITEM_IDS}, " f"got {len(work_item_ids)})"
        )
    return ",".join(work_item_ids)


class Workload(BaseResource):
    """Resource for the workload feature: per-work-item time estimates, the
    assignee x period workload matrix, and parent-rollup aggregation.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    # ── Matrix ───────────────────────────────────────────────────

    def get_matrix(
        self, workspace_slug: str, params: WorkloadQueryParams
    ) -> WorkloadMatrixResponse:
        """Workspace-wide workload matrix (assignee x period hours).

        Counts LEAF work items only — a work item with countable sub-items
        never contributes its own estimate (its sub-items do; the parent's
        aggregate is available via :meth:`list_rollups`). Defaults to
        excluding ``completed``/``cancelled`` state groups unless
        ``params.state_group`` is supplied.

        Args:
            workspace_slug: The workspace slug identifier.
            params: Matrix query parameters (``granularity``, ``date_from``,
                ``date_to`` are required; ``project_ids``, ``assignee_ids``,
                ``state_group`` optionally narrow the result).
        """
        response = self._get(
            f"{workspace_slug}/workload",
            params=_prepare_matrix_params(params),
        )
        return WorkloadMatrixResponse.model_validate(response)

    def get_project_matrix(
        self, workspace_slug: str, project_id: str, params: WorkloadQueryParams
    ) -> WorkloadMatrixResponse:
        """Project-scoped workload matrix. Same shape/semantics as
        :meth:`get_matrix`, narrowed to a single project.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            params: Matrix query parameters.
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/workload",
            params=_prepare_matrix_params(params),
        )
        return WorkloadMatrixResponse.model_validate(response)

    # ── Single work-item estimate ───────────────────────────────

    def get_estimate(
        self, workspace_slug: str, project_id: str, work_item_id: str
    ) -> WorkloadEstimateDetail:
        """Retrieve the stored workload estimate for a work item.

        For a PARENT work item (has one or more countable sub-items),
        ``hours`` is always ``None`` and ``rollup`` carries the aggregated
        total instead.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            work_item_id: UUID of the work item.
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/issues/{work_item_id}/workload-estimate",
        )
        return WorkloadEstimateDetail.model_validate(response)

    def update_estimate(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: UpdateWorkloadEstimate,
    ) -> WorkloadEstimateDetail:
        """Set the workload estimate (hours) for a work item.

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            work_item_id: UUID of the work item.
            data: The new estimate (``hours``, 0..10000).

        Raises:
            WorkloadParentHasChildrenError: the work item has one or more
                countable sub-items — set estimates on the sub-items
                instead. ``error_code`` is always ``"PARENT_HAS_CHILDREN"``.
        """
        try:
            response = self._put(
                f"{workspace_slug}/projects/{project_id}/issues/{work_item_id}/workload-estimate",
                data.model_dump(exclude_none=True),
            )
        except HttpError as exc:
            if (
                isinstance(exc.response, dict)
                and exc.response.get("error_code") == "PARENT_HAS_CHILDREN"
            ):
                # exc.status_code is always set for a constructed HttpError; the
                # attribute is typed as int | None only because the PlaneError
                # base class allows None for ConfigurationError.
                assert exc.status_code is not None
                raise WorkloadParentHasChildrenError(
                    str(exc), exc.status_code, exc.response
                ) from exc
            raise
        return WorkloadEstimateDetail.model_validate(response)

    def delete_estimate(self, workspace_slug: str, project_id: str, work_item_id: str) -> None:
        """Delete the stored workload estimate for a work item.

        Unlike :meth:`update_estimate`, this is allowed on parents (cleanup
        of legacy/ignored rows).

        Args:
            workspace_slug: The workspace slug identifier.
            project_id: UUID of the project.
            work_item_id: UUID of the work item.
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/issues/{work_item_id}/workload-estimate",
        )

    # ── Bulk ─────────────────────────────────────────────────────

    def list_estimates(self, workspace_slug: str, work_item_ids: list[str]) -> dict[str, float]:
        """Bulk-fetch stored estimates for up to 500 work items.

        Returns ``{work_item_id: hours}``. Work items with no stored row
        are omitted (treat as unset). Rows belonging to a PARENT work item
        are also omitted — a parent's legacy hours never leak here; see
        :meth:`list_rollups` for parent aggregates.

        Args:
            workspace_slug: The workspace slug identifier.
            work_item_ids: Work item UUIDs to fetch (non-empty, max 500).

        Raises:
            ValueError: ``work_item_ids`` is empty or exceeds 500 entries.
        """
        response = self._get(
            f"{workspace_slug}/workload-estimates",
            params={"issue_ids": _prepare_bulk_ids(work_item_ids)},
        )
        return {str(k): float(v) for k, v in response.items()}

    def list_rollups(
        self, workspace_slug: str, work_item_ids: list[str]
    ) -> dict[str, WorkloadRollup]:
        """Bulk-fetch parent rollups for up to 500 work items.

        Returns ``{work_item_id: WorkloadRollup}`` for ids that ARE parents
        (one or more countable sub-items); non-parent ids — and ids outside
        the caller's access — are both simply omitted (indistinguishable by
        design; mirrors :meth:`list_estimates`).

        Args:
            workspace_slug: The workspace slug identifier.
            work_item_ids: Work item UUIDs to fetch (non-empty, max 500).

        Raises:
            ValueError: ``work_item_ids`` is empty or exceeds 500 entries.
        """
        response = self._get(
            f"{workspace_slug}/workload-rollups",
            params={"issue_ids": _prepare_bulk_ids(work_item_ids)},
        )
        return {k: WorkloadRollup.model_validate(v) for k, v in response.items()}
