"""Models for workspace project states."""

from pydantic import BaseModel, ConfigDict


class WorkspaceProjectState(BaseModel):
    """Workspace project state response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    color: str | None = None
    group: str | None = None
    sequence: float | None = None
    default: bool | None = None
    description: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None


class CreateWorkspaceProjectState(BaseModel):
    """Request model for creating a workspace project state."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    color: str | None = None
    group: str | None = None
    sequence: float | None = None
    default: bool | None = None
    description: str | None = None


class UpdateWorkspaceProjectState(BaseModel):
    """Request model for updating a workspace project state."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    color: str | None = None
    group: str | None = None
    sequence: float | None = None
    default: bool | None = None
    description: str | None = None
