from typing import Any

from pydantic import BaseModel, ConfigDict


class Workflow(BaseModel):
    """Workflow model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str
    description: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    work_item_type_ids: list[str] | None = None
    created_at: str | None = None
    updated_at: str | None = None
    project: str | None = None
    workspace: str | None = None


class CreateWorkflow(BaseModel):
    """Request model for creating a workflow."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    is_active: bool | None = None
    work_item_type_ids: list[str] | None = None


class UpdateWorkflow(BaseModel):
    """Request model for updating a workflow."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    work_item_type_ids: list[str] | None = None


class AttachWorkflowStates(BaseModel):
    """Request model for attaching states to a workflow."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    state_ids: list[str]


class WorkflowTransition(BaseModel):
    """Workflow transition model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    state_id: str | None = None
    transition_state_id: str | None = None
    type: str | None = None
    member_ids: list[str] | None = None
    pre_rules: list[dict[str, Any]] | None = None
    post_rules: list[dict[str, Any]] | None = None
    workflow_state_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CreateWorkflowTransition(BaseModel):
    """Request model for creating a workflow transition."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    state_id: str
    transition_state_id: str
    type: str | None = None
    member_ids: list[str] | None = None
    pre_rules: list[dict[str, Any]] | None = None
    post_rules: list[dict[str, Any]] | None = None


class UpdateWorkflowTransition(BaseModel):
    """Request model for updating a workflow transition."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    pre_rules: list[dict[str, Any]] | None = None
    post_rules: list[dict[str, Any]] | None = None
