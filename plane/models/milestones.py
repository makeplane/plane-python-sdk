from typing import TYPE_CHECKING, Any

from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse

if TYPE_CHECKING:
    from .work_items import WorkItem


class Milestone(BaseModel):
    """Milestone model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    title: str
    target_date: str | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class MilestoneLite(BaseModel):
    """Lite milestone information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    title: str
    target_date: str | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CreateMilestone(BaseModel):
    """Request model for creating a milestone."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    title: str
    target_date: str | None = None
    external_source: str | None = None
    external_id: str | None = None


class UpdateMilestone(BaseModel):
    """Request model for updating a milestone."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    title: str | None = None
    target_date: str | None = None
    external_source: str | None = None
    external_id: str | None = None


class MilestoneWorkItem(BaseModel):
    """Work item in a milestone."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    issue: str | None = None
    milestone: str | None = None


class PaginatedMilestoneResponse(PaginatedResponse):
    """Paginated response for milestones."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Milestone]


class PaginatedMilestoneWorkItemResponse(PaginatedResponse):
    """Paginated response for milestone work items."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[MilestoneWorkItem]
