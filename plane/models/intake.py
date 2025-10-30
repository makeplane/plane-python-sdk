from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import IntakeWorkItemStatusEnum
from .pagination import PaginatedResponse
from .projects import Project
from .work_items import WorkItemExpand, WorkItemForIntakeRequest


class IntakeWorkItem(BaseModel):
    """Intake work item model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    issue_detail: WorkItemExpand | None = None
    inbox: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    status: IntakeWorkItemStatusEnum | None = None
    snoozed_till: str | None = None
    source: str | None = None
    source_email: str | None = None
    external_source: str | None = None
    external_id: str | None = None
    extra: Any | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | Project | None = None
    workspace: str | None = None
    intake: str | None = None
    issue: str | None = None
    duplicate_to: str | None = None


class CreateIntakeWorkItem(BaseModel):
    """Request model for creating an intake work item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    issue: WorkItemForIntakeRequest = Field(
        ...,
        description="Issue data for the intake issue",
    )


class UpdateIntakeWorkItem(BaseModel):
    """Request model for updating an intake work item."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    status: IntakeWorkItemStatusEnum | None = None
    snoozed_till: str | None = None
    duplicate_to: str | None = None
    source: str | None = None
    source_email: str | None = None
    issue: WorkItemForIntakeRequest | None = Field(
        None,
        description="Issue data to update in the intake issue",
    )


class PaginatedIntakeWorkItemResponse(PaginatedResponse):
    """Paginated response for intake work items."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[IntakeWorkItem]
