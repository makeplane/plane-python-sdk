"""Models for the workload feature: per-work-item time estimates, the
assignee x period workload matrix, and parent-rollup aggregation.

Mirrors the server-side semantics implemented in ``apps/api/plane/workload/``
of the plane fork (``aggregation.py`` / ``rollup.py`` / ``service.py``).
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

WorkloadGranularity = Literal["day", "week", "month"]


class WorkloadRow(BaseModel):
    """One assignee's scheduled hours, bucketed by period."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    assignee_id: str | None = None
    assignee_name: str | None = None
    buckets: dict[str, float] = Field(default_factory=dict)
    total: float = 0.0


class WorkloadUnscheduled(BaseModel):
    """Hours with no ``target_date`` for one assignee — excluded from any
    period bucket in the matrix."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    assignee_id: str | None = None
    hours: float = 0.0


class WorkloadMeta(BaseModel):
    """Diagnostic counters accompanying a workload matrix response."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    issues_counted: int | None = None
    issues_unscheduled: int | None = None
    dirty_date_count: int | None = None
    zero_estimate_count: int | None = None
    truncated: bool | None = None
    unscheduled_ratio: float | None = None


class WorkloadMatrixResponse(BaseModel):
    """Response for the workspace/project workload matrix endpoints.

    Counts LEAF work items only — a work item with one or more countable
    sub-items never contributes its own estimate to the matrix (its
    sub-items do, individually; the parent's aggregate is available via
    :meth:`~plane.api.workload.Workload.list_rollups`). Defaults to
    excluding ``completed``/``cancelled`` state groups unless a
    ``state_group`` filter was supplied on the request.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    granularity: WorkloadGranularity
    date_from: str
    date_to: str
    periods: list[str] = Field(default_factory=list)
    rows: list[WorkloadRow] = Field(default_factory=list)
    unscheduled: list[WorkloadUnscheduled] = Field(default_factory=list)
    meta: WorkloadMeta | None = None


class WorkloadRollup(BaseModel):
    """Aggregate rollup for a parent work item, computed over its full
    descendant tree (max depth 10, capped at 10,000 traversed rows).

    - ``hours``: sum of countable LEAF estimates (hours > 0) across the
      entire descendant tree.
    - ``done_hours``: subset of ``hours`` contributed by leaves whose state
      group is ``completed``.
    - ``percent``: ``round(done_hours / hours, 4)``; ``None`` when ``hours``
      is 0 (no countable estimates yet — avoids a division by zero).
    - ``due_date``: max ``target_date`` across ALL countable descendants
      (leaves and intermediate nodes), as an ISO date string, or ``None``.
    - ``leaf_count``: count of countable leaves with hours > 0.

    A descendant is "countable" when it is not soft-deleted, not archived,
    not a draft, and its state group is not ``cancelled``/``triage``.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    hours: float
    done_hours: float
    percent: float | None = None
    due_date: str | None = None
    leaf_count: int


class WorkloadEstimateDetail(BaseModel):
    """Response for the single work-item ``workload-estimate`` GET/PUT
    endpoints.

    ``hours`` is ``None`` when no estimate is stored, and is ALWAYS ``None``
    for a parent work item (``is_parent=True``) — a legacy stored value
    never leaks once a work item has countable sub-items; set estimates on
    the sub-items instead. ``is_parent`` / ``rollup`` are populated on GET
    only; the PUT response never carries them (a PUT can only succeed
    against a leaf work item — see
    :class:`~plane.errors.errors.WorkloadParentHasChildrenError`).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    work_item_id: str | None = Field(default=None, alias="issue")
    hours: float | None = None
    created_at: str | None = None
    updated_at: str | None = None
    is_parent: bool | None = None
    rollup: WorkloadRollup | None = None


class UpdateWorkloadEstimate(BaseModel):
    """Request body for ``PUT .../workload-estimate/``."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    hours: float = Field(..., ge=0, le=10000)


class WorkloadQueryParams(BaseModel):
    """Query parameters for the workspace/project workload matrix
    endpoints.

    ``granularity``, ``date_from``, and ``date_to`` are required. Date span
    is capped server-side depending on granularity (92 days for ``day``,
    366 for ``week``, 730 for ``month``).
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    granularity: WorkloadGranularity
    date_from: str
    date_to: str
    project_ids: list[str] | None = Field(
        default=None,
        description="Work item project UUIDs to narrow the matrix to. CSV-joined on the wire.",
    )
    assignee_ids: list[str] | None = Field(
        default=None,
        description="Assignee UUIDs to narrow the matrix to. CSV-joined on the wire.",
    )
    state_group: list[str] | None = Field(
        default=None,
        description=(
            "State groups to include (overrides the completed/cancelled "
            "default exclusion). CSV-joined on the wire."
        ),
    )


__all__ = [
    "WorkloadGranularity",
    "WorkloadRow",
    "WorkloadUnscheduled",
    "WorkloadMeta",
    "WorkloadMatrixResponse",
    "WorkloadRollup",
    "WorkloadEstimateDetail",
    "UpdateWorkloadEstimate",
    "WorkloadQueryParams",
]
