"""Feature-toggle models for api_v2 (GET/PATCH singletons); `ProjectFeature` has no `id` field,
unlike `WorkspaceFeature`."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WorkspaceFeature(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    is_customer_enabled: bool | None = None
    is_initiative_enabled: bool | None = None
    is_member_project_creation_enabled: bool | None = None
    is_pi_enabled: bool | None = None
    is_project_grouping_enabled: bool | None = None
    is_release_enabled: bool | None = None
    is_state_duration_enabled: bool | None = None
    is_teams_enabled: bool | None = None
    is_wiki_enabled: bool | None = None
    is_work_item_types_enabled: bool | None = None
    is_workitem_hierarchy_enabled: bool | None = None
    work_item_type_default_level: int | None = None
    created_at: datetime | None = None


class UpdateWorkspaceFeature(BaseModel):
    model_config = ConfigDict(extra="ignore")

    is_customer_enabled: bool | None = None
    is_initiative_enabled: bool | None = None
    is_member_project_creation_enabled: bool | None = None
    is_pi_enabled: bool | None = None
    is_project_grouping_enabled: bool | None = None
    is_release_enabled: bool | None = None
    is_state_duration_enabled: bool | None = None
    is_teams_enabled: bool | None = None
    is_wiki_enabled: bool | None = None
    is_work_item_types_enabled: bool | None = None
    is_workitem_hierarchy_enabled: bool | None = None
    work_item_type_default_level: int | None = None


class ProjectFeature(BaseModel):
    """No `id` field -- the golden schema has none for this singleton."""

    model_config = ConfigDict(extra="allow")

    is_automated_cycle_enabled: bool | None = None
    is_epic_enabled: bool | None = None
    is_manually_start_end_cycles_enabled: bool | None = None
    is_milestone_enabled: bool | None = None
    is_parallel_cycles_enabled: bool | None = None
    is_project_updates_enabled: bool | None = None
    is_workflow_enabled: bool | None = None


class UpdateProjectFeature(BaseModel):
    model_config = ConfigDict(extra="ignore")

    is_automated_cycle_enabled: bool | None = None
    is_epic_enabled: bool | None = None
    is_manually_start_end_cycles_enabled: bool | None = None
    is_milestone_enabled: bool | None = None
    is_parallel_cycles_enabled: bool | None = None
    is_project_updates_enabled: bool | None = None
    is_workflow_enabled: bool | None = None
