"""Workflow models for api_v2. Golden `$ref` mismatch: `workflow_states_create` accepts
`{state_ids}` per prose, but `WorkflowStateWriteRequest` only declares
`type`/`is_default`/`allow_issue_creation` -- modeled on v1's `AttachWorkflowStates` instead."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Workflow(BaseModel):
    """A project's work-item-type workflow configuration."""

    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    is_default: bool | None = None
    work_item_type_ids: list[str] | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateWorkflow(BaseModel):
    """POST body. `name` is the only field the API requires."""

    model_config = ConfigDict(extra="ignore")

    name: str
    description: str | None = None
    is_active: bool | None = None
    work_item_type_ids: list[str] | None = None


class UpdateWorkflow(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description: str | None = None
    is_active: bool | None = None
    work_item_type_ids: list[str] | None = None


class WorkflowState(BaseModel):
    """A project `State` attached to a workflow, plus this workflow's own flags
    for it. `state_id` is the underlying project State's id (matching v1)."""

    model_config = ConfigDict(extra="allow")

    id: str
    workflow_id: str | None = None
    state_id: str | None = None
    type: str | None = None
    is_default: bool | None = None
    allow_issue_creation: bool | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class WorkflowStateCreate(BaseModel):
    """POST body for `workflow_states_create`: bulk-attach existing project states
    to this workflow by id. See the module docstring for why this does not match
    the golden's own `WorkflowStateWriteRequest` component."""

    model_config = ConfigDict(extra="ignore")

    state_ids: list[str]


class UpdateWorkflowState(BaseModel):
    """PATCH body for an already-attached workflow state (type / is_default /
    allow_issue_creation) -- every field optional."""

    model_config = ConfigDict(extra="ignore")

    type: str | None = None
    is_default: bool | None = None
    allow_issue_creation: bool | None = None


class WorkflowTransition(BaseModel):
    """One allowed transition out of a workflow state, with optional approval
    gating (`required_approvals`, `member_ids`) and an optional rejection target."""

    model_config = ConfigDict(extra="allow")

    id: str
    workflow_state_id: str | None = None
    transition_state_id: str | None = None
    rejection_state_id: str | None = None
    required_approvals: int | None = None
    member_ids: list[str] | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateWorkflowTransition(BaseModel):
    """POST body. `state_id` identifies the source workflow state (project State
    id, matching v1) and is effectively required on create, though the golden does
    not mark any field of this shared create/patch schema as required."""

    model_config = ConfigDict(extra="ignore")

    state_id: str | None = None
    transition_state_id: str | None = None
    rejection_state_id: str | None = None
    required_approvals: int | None = None
    member_ids: list[str] | None = None


class UpdateWorkflowTransition(BaseModel):
    """PATCH body -- every field optional. Same shape as `CreateWorkflowTransition`
    (the golden reuses one schema, `PatchedWorkflowTransitionWriteRequest`, for
    both create and patch)."""

    model_config = ConfigDict(extra="ignore")

    state_id: str | None = None
    transition_state_id: str | None = None
    rejection_state_id: str | None = None
    required_approvals: int | None = None
    member_ids: list[str] | None = None
