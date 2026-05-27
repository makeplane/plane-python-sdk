"""Models for work item relation definitions."""

from pydantic import BaseModel, ConfigDict


class WorkItemRelationDefinition(BaseModel):
    """Work item relation definition response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    outward: str | None = None
    inward: str | None = None
    is_default: bool | None = None
    is_active: bool | None = None
    color: str | None = None
    sort_order: float | None = None
    created_at: str | None = None
    updated_at: str | None = None
    workspace: str | None = None


class CreateWorkItemRelationDefinition(BaseModel):
    """Request model for creating a work item relation definition."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    outward: str | None = None
    inward: str | None = None
    is_default: bool | None = None
    is_active: bool | None = None
    color: str | None = None
    sort_order: float | None = None


class UpdateWorkItemRelationDefinition(BaseModel):
    """Request model for updating a work item relation definition."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    outward: str | None = None
    inward: str | None = None
    is_default: bool | None = None
    is_active: bool | None = None
    color: str | None = None
    sort_order: float | None = None
