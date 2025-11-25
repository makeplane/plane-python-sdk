from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .enums import NetworkEnum, TimezoneEnum
from .pagination import PaginatedResponse


class Project(BaseModel):
    """Project model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    total_members: int | None = None
    total_cycles: int | None = None
    total_modules: int | None = None
    is_member: bool | None = None
    sort_order: float | None = None
    member_role: int | None = None
    is_deployed: bool | None = None
    cover_image_url: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    description_text: Any | None = None
    description_html: Any | None = None
    network: NetworkEnum | None = None
    identifier: str
    emoji: str | None = None
    icon_prop: Any | None = None
    module_view: bool | None = None
    cycle_view: bool | None = None
    issue_views_view: bool | None = None
    page_view: bool | None = None
    intake_view: bool | None = None
    is_time_tracking_enabled: bool | None = None
    is_issue_type_enabled: bool | None = None
    guest_view_all_features: bool | None = None
    cover_image: str | None = None
    archive_in: int | None = None
    close_in: int | None = None
    logo_props: Any | None = None
    archived_at: str | None = None
    timezone: TimezoneEnum | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None
    default_assignee: str | None = None
    project_lead: str | None = None
    cover_image_asset: str | None = None
    estimate: str | None = None
    default_state: str | None = None


class CreateProject(BaseModel):
    """Request model for creating a project."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    project_lead: str | None = None
    default_assignee: str | None = None
    identifier: str
    icon_prop: Any | None = None
    emoji: str | None = None
    cover_image: str | None = None
    module_view: bool | None = None
    cycle_view: bool | None = None
    issue_views_view: bool | None = None
    page_view: bool | None = None
    intake_view: bool | None = None
    guest_view_all_features: bool | None = None
    archive_in: int | None = None
    close_in: int | None = None
    timezone: TimezoneEnum | None = None
    logo_props: Any | None = None
    external_source: str | None = None
    external_id: str | None = None
    is_issue_type_enabled: bool | None = None


class UpdateProject(BaseModel):
    """Request model for updating a project."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    project_lead: str | None = None
    default_assignee: str | None = None
    identifier: str | None = None
    icon_prop: Any | None = None
    emoji: str | None = None
    cover_image: str | None = None
    module_view: bool | None = None
    cycle_view: bool | None = None
    issue_views_view: bool | None = None
    page_view: bool | None = None
    intake_view: bool | None = None
    guest_view_all_features: bool | None = None
    archive_in: int | None = None
    close_in: int | None = None
    timezone: TimezoneEnum | None = None
    logo_props: Any | None = None
    external_source: str | None = None
    external_id: str | None = None
    is_issue_type_enabled: bool | None = None
    is_time_tracking_enabled: bool | None = None
    default_state: str | None = None
    estimate: str | None = None


class ProjectWorklogSummary(BaseModel):
    """Summary of work log for a project."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    issue_id: str = Field(..., description="ID of the work item")
    duration: int = Field(
        ...,
        description="Total duration logged for this work item in seconds",
    )


class PaginatedProjectResponse(PaginatedResponse):
    """Paginated response for projects."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Project]

class ProjectFeature(BaseModel):
  """Project feature model."""

  model_config = ConfigDict(extra="allow", populate_by_name=True)

  epics: bool | None = None
  modules: bool | None = None
  cycles: bool | None = None
  views: bool | None = None
  pages: bool | None = None
  intakes: bool | None = None
  work_item_types: bool | None = None
