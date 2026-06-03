from typing import Any

from pydantic import BaseModel, ConfigDict


class WorkItemPropertyContextOption(BaseModel):
    """Option entry within a context response."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    is_default: bool | None = None
    sort_order: float | None = None


class WorkItemPropertyContext(BaseModel):
    """Work item property context model.

    Represents a (project, work-item-type) scope override for a custom property.
    See docs/contexts.md for full semantics.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    property: str | None = None
    name: str | None = None
    is_default: bool | None = None
    applies_to_all_projects: bool | None = None
    applies_to_all_work_item_types: bool | None = None
    is_required: bool | None = None
    is_multi: bool | None = None
    default_value: list[str] | None = None
    settings: dict[str, Any] | None = None
    sort_order: float | None = None
    external_source: str | None = None
    external_id: str | None = None
    project_ids: list[str] | None = None
    issue_type_ids: list[str] | None = None
    options: list[WorkItemPropertyContextOption] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    workspace: str | None = None


class CreateWorkItemPropertyContext(BaseModel):
    """Request model for creating a work item property context."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    applies_to_all_projects: bool | None = None
    applies_to_all_work_item_types: bool | None = None
    is_required: bool | None = None
    is_multi: bool | None = None
    default_value: list[str] | None = None
    settings: dict[str, Any] | None = None
    external_source: str | None = None
    external_id: str | None = None
    project_ids: list[str] | None = None
    issue_type_ids: list[str] | None = None
    options: list[dict[str, Any]] | None = None


class UpdateWorkItemPropertyContext(BaseModel):
    """Request model for updating a work item property context."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    applies_to_all_projects: bool | None = None
    applies_to_all_work_item_types: bool | None = None
    is_required: bool | None = None
    is_multi: bool | None = None
    default_value: list[str] | None = None
    settings: dict[str, Any] | None = None
    sort_order: float | None = None
    external_source: str | None = None
    external_id: str | None = None
    project_ids: list[str] | None = None
    issue_type_ids: list[str] | None = None
    options: list[dict[str, Any]] | None = None
