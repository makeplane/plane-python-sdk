"""Project models for api_v2; every foreign key (`default_assignee_id`, `project_lead_id`, etc.) is
id-only, no readable-name counterpart."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

Priority = Literal["none", "low", "medium", "high", "urgent"]
Network = Literal[0, 2]
"""0 = Secret (private), 2 = Public."""


class Project(BaseModel):
    """A project. `identifier` (e.g. `"ENG"`) is the human-readable key that every
    detail route on `Projects` also accepts in place of the UUID `id` -- see
    `Projects.retrieve`."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    identifier: str | None = None
    network: Network | None = None
    priority: Priority | None = None
    emoji: str | None = None
    icon_prop: dict[str, object] | None = None
    cover_image: str | None = None
    cover_image_url: str | None = None
    logo_props: dict[str, object] | None = None
    module_view: bool | None = None
    cycle_view: bool | None = None
    issue_views_view: bool | None = None
    page_view: bool | None = None
    intake_view: bool | None = None
    guest_view_all_features: bool | None = None
    is_time_tracking_enabled: bool | None = None
    is_issue_type_enabled: bool | None = None
    start_date: datetime | None = None
    target_date: datetime | None = None
    archive_in: int | None = None
    close_in: int | None = None
    default_assignee_id: str | None = None
    project_lead_id: str | None = None
    default_state_id: str | None = None
    estimate_id: str | None = None
    state_id: str | None = None
    timezone: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    archived_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateProject(BaseModel):
    """POST body; `identifier`/`name` required; `default_state_id`/`estimate_id` only apply once
    the project exists (PATCH)."""

    model_config = ConfigDict(extra="ignore")

    identifier: str
    name: str
    description: str | None = None
    network: Network | None = None
    priority: Priority | None = None
    emoji: str | None = None
    icon_prop: dict[str, object] | None = None
    cover_image: str | None = None
    logo_props: dict[str, object] | None = None
    module_view: bool | None = None
    cycle_view: bool | None = None
    issue_views_view: bool | None = None
    page_view: bool | None = None
    intake_view: bool | None = None
    guest_view_all_features: bool | None = None
    is_time_tracking_enabled: bool | None = None
    is_issue_type_enabled: bool | None = None
    start_date: datetime | None = None
    target_date: datetime | None = None
    """Must not be earlier than `start_date`."""
    archive_in: int | None = None
    close_in: int | None = None
    default_assignee_id: str | None = None
    project_lead_id: str | None = None
    default_state_id: str | None = None
    estimate_id: str | None = None
    state_id: str | None = None
    timezone: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateProject(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    identifier: str | None = None
    name: str | None = None
    description: str | None = None
    network: Network | None = None
    priority: Priority | None = None
    emoji: str | None = None
    icon_prop: dict[str, object] | None = None
    cover_image: str | None = None
    logo_props: dict[str, object] | None = None
    module_view: bool | None = None
    cycle_view: bool | None = None
    issue_views_view: bool | None = None
    page_view: bool | None = None
    intake_view: bool | None = None
    guest_view_all_features: bool | None = None
    is_time_tracking_enabled: bool | None = None
    is_issue_type_enabled: bool | None = None
    start_date: datetime | None = None
    target_date: datetime | None = None
    archive_in: int | None = None
    close_in: int | None = None
    default_assignee_id: str | None = None
    project_lead_id: str | None = None
    default_state_id: str | None = None
    estimate_id: str | None = None
    state_id: str | None = None
    timezone: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class ProjectSummary(BaseModel):
    """`GET .../projects/{pk}/summary/` -- identity plus optional resource counts."""

    model_config = ConfigDict(extra="allow")

    id: str
    identifier: str
    name: str
    counts: dict[str, int]
