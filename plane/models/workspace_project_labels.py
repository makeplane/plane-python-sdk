"""Models for workspace project labels."""

from pydantic import BaseModel, ConfigDict


class WorkspaceProjectLabel(BaseModel):
    """Workspace project label response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    color: str | None = None
    sort_order: float | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None


class CreateWorkspaceProjectLabel(BaseModel):
    """Request model for creating a workspace project label."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    color: str | None = None
    sort_order: float | None = None


class UpdateWorkspaceProjectLabel(BaseModel):
    """Request model for updating a workspace project label."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    color: str | None = None
    sort_order: float | None = None
