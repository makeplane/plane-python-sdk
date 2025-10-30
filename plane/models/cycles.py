from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .pagination import PaginatedResponse
from .work_items import WorkItem


class Cycle(BaseModel):
    """Cycle model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    total_issues: int | None = None
    cancelled_issues: int | None = None
    completed_issues: int | None = None
    started_issues: int | None = None
    unstarted_issues: int | None = None
    backlog_issues: int | None = None
    total_estimates: int | None = None
    completed_estimates: int | None = None
    started_estimates: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    view_props: Any | None = None
    sort_order: float | None = None
    external_source: str | None = None
    external_id: str | None = None
    progress_snapshot: Any | None = None
    archived_at: str | None = None
    logo_props: Any | None = None
    timezone: str | None = None
    version: int | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    owned_by: str | None = None


class CycleLite(BaseModel):
    """Lite cycle information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    view_props: Any | None = None
    sort_order: float | None = None
    external_source: str | None = None
    external_id: str | None = None
    progress_snapshot: Any | None = None
    archived_at: str | None = None
    logo_props: Any | None = None
    timezone: str | None = None
    version: int | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str
    workspace: str
    owned_by: str


class CreateCycle(BaseModel):
    """Request model for creating a cycle."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    owned_by: str
    external_source: str | None = None
    external_id: str | None = None
    timezone: str | None = None
    project_id: str


class UpdateCycle(BaseModel):
    """Request model for updating a cycle."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    owned_by: str | None = None
    external_source: str | None = None
    external_id: str | None = None
    timezone: str | None = None


class CycleWorkItem(BaseModel):
    """Work item in a cycle."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    sub_issues_count: int | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None
    issue: str | None = None
    cycle: str | None = None


class TransferCycleWorkItemsRequest(BaseModel):
    """Request model for transferring cycle work items."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    new_cycle_id: str = Field(
        ...,
        description="ID of the target cycle to transfer issues to",
    )


class PaginatedCycleResponse(PaginatedResponse):
    """Paginated response for cycles."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Cycle]


class PaginatedArchivedCycleResponse(PaginatedResponse):
    """Paginated response for archived cycles."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Cycle]


class PaginatedCycleWorkItemResponse(PaginatedResponse):
    """Paginated response for cycle work items."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkItem]
