from typing import Any, Literal

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


class WorkflowState(BaseModel):
    """A state's membership row within a workflow chain.

    ``id`` is the membership row's ID and ``state_id`` the state's own — the
    inverse of :class:`plane.models.workspace_workflows.WorkspaceWorkflowState`,
    whose rows are keyed by state ID.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    state_id: str | None = None
    workflow_id: str | None = None
    type: str | None = None
    allow_issue_creation: bool | None = None
    is_default: bool | None = None
    created_at: str | None = None
    updated_at: str | None = None


class UpdateWorkflowState(BaseModel):
    """Request model for updating a workflow state membership row."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    type: str | None = None
    allow_issue_creation: bool | None = None
    is_default: bool | None = None


class WorkflowActivity(BaseModel):
    """One workflow activity/audit entry."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    verb: str | None = None
    field: str | None = None
    old_value: Any | None = None
    new_value: Any | None = None
    actor: Any | None = None
    created_at: str | None = None


class SubmitWorkItemApproval(BaseModel):
    """Request model for approving or rejecting a work item's pending workflow
    transition. ``type`` is ``"approve"`` or ``"reject"``."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    type: Literal["approve", "reject"]


class WorkItemApprovalResult(BaseModel):
    """Response of a work item workflow approval: the state the item moved to."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    state_id: str | None = None


class WorkflowTransitionHook(BaseModel):
    """A validation/action hook attached to a workflow transition.

    ``config.secret`` is masked for send_webhook handlers; the one-shot
    ``secret_plaintext`` appears on create and regenerate responses only.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    phase: str | None = None
    handler_name: str | None = None
    rule_type: str | None = None
    execution_order: int | None = None
    is_enabled: bool | None = None
    config: dict[str, Any] | None = None
    secret_plaintext: str | None = None


class CreateWorkflowTransitionHook(BaseModel):
    """Request model for creating a workflow transition hook.

    ``phase`` and ``handler_name`` are immutable post-create. The per-handler
    ``config`` shape is validated server-side (e.g. send_webhook requires
    ``config.url``; run_script requires ``config.script_id``).
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    phase: str
    handler_name: str
    config: dict[str, Any]
    is_enabled: bool | None = None


class UpdateWorkflowTransitionHook(BaseModel):
    """Request model for updating a workflow transition hook."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    config: dict[str, Any] | None = None
    is_enabled: bool | None = None
