from typing import Any

from pydantic import BaseModel, ConfigDict


class WorkItemType(BaseModel):
    """Work item type model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    deleted_at: str | None = None
    project_ids: list[str] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    name: str
    description: str | None = None
    logo_props: Any | None = None
    is_epic: bool | None = None
    is_default: bool | None = None
    is_active: bool | None = None
    level: int | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None


class CreateWorkItemType(BaseModel):
    """Request model for creating a work item type."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    project_ids: list[str] | None = None
    name: str
    description: str | None = None
    is_epic: bool | None = None
    is_active: bool | None = None
    external_source: str | None = None
    external_id: str | None = None


class UpdateWorkItemType(BaseModel):
    """Request model for updating a work item type."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    project_ids: list[str] | None = None
    name: str | None = None
    description: str | None = None
    is_epic: bool | None = None
    is_active: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
