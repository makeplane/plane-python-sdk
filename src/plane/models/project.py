from typing import Optional
from pydantic import Field
from .base import BaseAPIModel, TimestampMixin


class Project(BaseAPIModel, TimestampMixin):
    """Project model."""

    id: str
    name: str
    description: Optional[str] = None
    description_text: Optional[str] = None
    description_html: Optional[str] = None
    network: Optional[int] = Field(default=2)
    workspace: str
    identifier: str
    default_assignee: Optional[str] = None
    project_lead: Optional[str] = None
    emoji: Optional[str] = None
    icon_prop: Optional[str] = None
    module_view: Optional[bool] = Field(default=True)
    cycle_view: Optional[bool] = Field(default=True)
    issue_views_view: Optional[bool] = Field(default=True)
    page_view: Optional[bool] = Field(default=True)
    intake_view: Optional[bool] = Field(default=False)
    is_time_tracking_enabled: Optional[bool] = Field(default=False)
    is_issue_type_enabled: Optional[bool] = Field(default=False)
    guest_view_all_features: Optional[bool] = Field(default=False)
    cover_image: Optional[str] = None
    cover_image_asset: Optional[str] = None
    estimate: Optional[str] = None
    archive_in: Optional[int] = Field(default=0)
    close_in: Optional[int] = Field(default=0)
    logo_props: Optional[str] = None
    default_state: Optional[str] = None
    archived_at: Optional[str] = None
    timezone: Optional[str] = Field(default="UTC")


class ProjectCreate(BaseAPIModel):
    """Project create model."""

    name: str
    description: Optional[str] = None
    description_text: Optional[str] = None
    description_html: Optional[str] = None
    network: Optional[int] = Field(default=2)
    workspace: str
    identifier: str


class ProjectUpdate(BaseAPIModel):
    """Project update model."""

    name: Optional[str] = None
    description: Optional[str] = None
    description_text: Optional[str] = None
    description_html: Optional[str] = None
    network: Optional[int] = Field(default=2)
    workspace: Optional[str] = None
    identifier: Optional[str] = None
    default_assignee: Optional[str] = None
    project_lead: Optional[str] = None
    emoji: Optional[str] = None
    icon_prop: Optional[str] = None
    module_view: Optional[bool] = Field(default=True)
    cycle_view: Optional[bool] = Field(default=True)
    issue_views_view: Optional[bool] = Field(default=True)
    page_view: Optional[bool] = Field(default=True)
    intake_view: Optional[bool] = Field(default=False)
    is_time_tracking_enabled: Optional[bool] = Field(default=False)
    is_issue_type_enabled: Optional[bool] = Field(default=False)
    guest_view_all_features: Optional[bool] = Field(default=False)
    cover_image: Optional[str] = None
    cover_image_asset: Optional[str] = None
    estimate: Optional[str] = None
    archive_in: Optional[int] = Field(default=0)
    close_in: Optional[int] = Field(default=0)
    logo_props: Optional[str] = None
    default_state: Optional[str] = None
    archived_at: Optional[str] = None
    timezone: Optional[str] = Field(default="UTC")


class ProjectDelete(BaseAPIModel):
    """Project delete model."""

    id: str


class ProjectArchive(BaseAPIModel):
    """Project archive model."""

    id: str


class ProjectUnarchive(BaseAPIModel):
    """Project unarchive model."""

    id: str
