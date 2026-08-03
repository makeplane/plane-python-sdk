from typing import Any

from pydantic import BaseModel, ConfigDict, model_validator

from .pagination import PaginatedResponse


class WorkspaceWorkflowState(BaseModel):
    """One state row in a workspace workflow's chain.

    Rows are keyed by catalog state IDs, so ``id`` is the state's own ID — the
    inverse of the project-scoped :class:`plane.models.workflows.WorkflowState`,
    where ``id`` is the membership row's ID and ``state_id`` is the state's. The
    API never sends ``state_id`` on these rows; the SDK fills it from ``id`` so
    that ``state_id`` identifies the state in both models and only ``id``
    differs.

    ``transitions`` embeds the outgoing transitions (with approvers) when the
    payload is the full chain projection.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    state_id: str | None = None
    type: str | None = None
    allow_issue_creation: bool | None = None
    is_default: bool | None = None
    sequence: float | None = None
    transitions: list[dict[str, Any]] | None = None

    @model_validator(mode="before")
    @classmethod
    def _fill_state_id_from_id(cls, data: Any) -> Any:
        """Populate ``state_id`` from ``id`` when the payload omits it.

        Without this the field would silently parse as ``None`` on every chain
        row, which reads as "this row has no state" rather than "the server
        does not send this key". If a future payload does carry ``state_id``,
        that value wins.
        """
        if isinstance(data, dict) and data.get("state_id") is None and data.get("id") is not None:
            return {**data, "state_id": data["id"]}
        return data


class WorkspaceWorkflow(BaseModel):
    """Workspace workflow model (catalog list row / detail superset).

    The list endpoint returns the count fields only; ``retrieve`` adds the full
    ``states`` chain, ``project_ids``/``work_item_type_ids`` usage, and
    ``referenced_resources``.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str
    description: str | None = None
    is_default: bool | None = None
    is_active: bool | None = None
    workspace_id: str | None = None
    project_id: str | None = None
    states_count: int | None = None
    projects_count: int | None = None
    work_item_types_count: int | None = None
    project_ids: list[str] | None = None
    work_item_type_ids: list[str] | None = None
    states: list[WorkspaceWorkflowState] | None = None
    referenced_resources: Any | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None


class PaginatedWorkspaceWorkflowResponse(PaginatedResponse):
    """Paginated response for workspace workflows."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkspaceWorkflow]


class CreateWorkspaceWorkflow(BaseModel):
    """Request model for creating a workspace workflow (a draft until its chain
    is configured via the states endpoints)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None


class UpdateWorkspaceWorkflow(BaseModel):
    """Request model for updating workspace workflow metadata."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class AddWorkspaceWorkflowStates(BaseModel):
    """Request model for appending catalog states to a workflow's chain."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    state_ids: list[str]


class UpdateWorkspaceWorkflowState(BaseModel):
    """Request model for updating a chain membership row.

    Changing ``type`` (e.g. to/from ``approval``) removes the row's existing
    transitions server-side.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    type: str | None = None
    allow_issue_creation: bool | None = None
    is_default: bool | None = None


class RemoveWorkspaceWorkflowState(BaseModel):
    """Request body for removing a state from a chain.

    Orphan-gated: every work item stranded by the removal must be covered by
    ``state_mapping`` (409 with an orphan report otherwise). Removing the
    default state requires ``new_default_state_id``.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    new_default_state_id: str | None = None
    state_mapping: dict[str, str] | None = None


class WorkspaceWorkflowUsageProject(BaseModel):
    """One project resolving to a workflow in the usage report."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    project_id: str | None = None
    name: str | None = None
    types: list[str | None] = []


class WorkspaceWorkflowUsage(BaseModel):
    """Usage report for a workspace workflow: projects/types resolving to it,
    plus the types mandating or allowing it."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    projects: list[WorkspaceWorkflowUsageProject] = []
    types_mandating: list[str] = []
    types_allowing: list[str] = []


class WorkspaceWorkflowTransition(BaseModel):
    """State transition within a workspace workflow."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    workflow_state_id: str | None = None
    transition_state_id: str | None = None
    rejection_state_id: str | None = None
    required_approvals: int | None = None
    member_ids: list[str] | None = None
    pre_hooks: list[dict[str, Any]] | None = None
    post_hooks: list[dict[str, Any]] | None = None
    created_at: str | None = None
    updated_at: str | None = None


class CreateWorkspaceWorkflowTransition(BaseModel):
    """Request model for creating a workspace workflow transition.

    ``state_id`` is the chain state the transition starts from;
    ``member_ids`` are the approvers (approval-type states only).
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    state_id: str
    transition_state_id: str
    rejection_state_id: str | None = None
    required_approvals: int | None = None
    member_ids: list[str] | None = None


class UpdateWorkspaceWorkflowTransition(BaseModel):
    """Request model for updating a workspace workflow transition."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    transition_state_id: str | None = None
    rejection_state_id: str | None = None
    required_approvals: int | None = None
    member_ids: list[str] | None = None
