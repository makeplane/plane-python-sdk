"""Group sync models for api_v2 (IdP group -> role/project mapping); `GroupSyncConfig` is a
workspace-wide singleton."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class GroupSyncConfig(BaseModel):
    """Workspace-wide IdP group sync settings. Exactly one row per workspace."""

    model_config = ConfigDict(extra="allow")

    id: str
    group_attribute_key: str | None = None
    is_enabled: bool | None = None
    sync_on_login: bool | None = None
    sync_offline: bool | None = None
    auto_remove: bool | None = None
    default_workspace_role_slug: str | None = None


class UpdateGroupSyncConfig(BaseModel):
    """PATCH body -- every field optional. No POST/create for this singleton."""

    model_config = ConfigDict(extra="ignore")

    group_attribute_key: str | None = None
    is_enabled: bool | None = None
    sync_on_login: bool | None = None
    sync_offline: bool | None = None
    auto_remove: bool | None = None
    default_workspace_role_slug: str | None = None


class GroupMapping(BaseModel):
    """IdP group -> project (or every project) + role. Project-level mapping."""

    model_config = ConfigDict(extra="allow")

    id: str
    idp_group_name: str | None = None
    project_id: str | None = None
    all_projects: bool | None = None
    role_slug: str | None = None
    created_at: datetime | None = None


class CreateGroupMapping(BaseModel):
    """POST body; `idp_group_name`/`role_slug` required, set `all_projects=True` to map every
    project instead of one `project_id`."""

    model_config = ConfigDict(extra="ignore")

    idp_group_name: str
    role_slug: str
    project_id: str | None = None
    all_projects: bool | None = None


class UpdateGroupMapping(BaseModel):
    """PATCH body -- every field optional."""

    model_config = ConfigDict(extra="ignore")

    idp_group_name: str | None = None
    role_slug: str | None = None
    project_id: str | None = None
    all_projects: bool | None = None


class WorkspaceGroupMapping(BaseModel):
    """IdP group -> workspace role. Workspace-level mapping (no project)."""

    model_config = ConfigDict(extra="allow")

    id: str
    idp_group_name: str | None = None
    role_slug: str | None = None
    created_at: datetime | None = None


class CreateWorkspaceGroupMapping(BaseModel):
    """POST body. `idp_group_name` and `role_slug` are both required."""

    model_config = ConfigDict(extra="ignore")

    idp_group_name: str
    role_slug: str


class UpdateWorkspaceGroupMapping(BaseModel):
    """PATCH body -- every field optional."""

    model_config = ConfigDict(extra="ignore")

    idp_group_name: str | None = None
    role_slug: str | None = None
