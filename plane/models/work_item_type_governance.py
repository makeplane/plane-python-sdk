from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class WorkflowLite(BaseModel):
    """Minimal workflow shape for embedding (pickers, pins)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None


class GovernanceProjectRef(BaseModel):
    """Minimal project reference in governance payloads."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None


class GovernanceAllowlistEntry(BaseModel):
    """One allowlist/mandate row, enriched with its in-use projects.

    ``locked`` marks workflows a project's pick already uses — a constrained
    allowlist must retain them.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    workflow_id: str | None = None
    name: str | None = None
    in_use_by_projects: list[GovernanceProjectRef] = []
    locked: bool | None = None


class TypeGovernance(BaseModel):
    """Governance settings for a work item type: mode, required workflow, and
    allowlist. Pins are served by the dedicated pins endpoints."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    mode: str | None = None
    required_workflow: WorkflowLite | None = None
    allowlist: list[GovernanceAllowlistEntry] = []


class UpdateTypeGovernance(BaseModel):
    """Request model for changing a type's governance mode.

    - ``any``: no restriction; ``workflow_ids``/``required_workflow_id`` unused.
    - ``constrained``: ``workflow_ids`` is the allowlist (in-use workflows are
      locked in). Removing picks in use requires ``acknowledge`` and may need a
      ``state_mapping`` for orphaned work items.
    - ``required``: ``required_workflow_id`` mandates one workflow everywhere;
      requires ``acknowledge`` and may need a ``state_mapping``.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    mode: Literal["any", "constrained", "required"]
    workflow_ids: list[str] | None = None
    required_workflow_id: str | None = None
    acknowledge: bool | None = None
    state_mapping: dict[str, str] | None = None


class TypeGovernancePreviewRequest(BaseModel):
    """Request model for previewing a governance mode change (no writes)."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    mode: Literal["any", "constrained", "required"]
    workflow_ids: list[str] | None = None
    required_workflow_id: str | None = None


class GovernancePreview(BaseModel):
    """Dry-run impact report for a governance change or workflow fallback."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    total: int | None = None
    type_total: int | None = None
    per_state: list[dict[str, Any]] | None = None


class WorkItemTypeWorkflowPin(BaseModel):
    """A single project-to-workflow pin for a work item type."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    project: GovernanceProjectRef | None = None
    workflow: WorkflowLite | None = None


class CreateWorkItemTypeWorkflowPins(BaseModel):
    """Request model for pinning a workflow across one or more projects."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    workflow_id: str
    project_ids: list[str]


class WorkflowOption(BaseModel):
    """A pickable workflow option for a project's type."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    workflow_id: str | None = None
    name: str | None = None


class ProjectTypeWorkflow(BaseModel):
    """One active type's governance pill, effective workflow, and pickable
    options within a project."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type_id: str | None = None
    governance: str | None = None  # any | constrained | required | pinned
    allowlist_count: int | None = None
    allowlist_total: int | None = None
    effective_workflow_id: str | None = None
    source: str | None = None
    options: list[WorkflowOption] = []


class SetProjectWorkflowPick(BaseModel):
    """Request model for setting a project's workflow pick for a type.

    Orphan-gated: work items whose state falls outside the target chain must be
    covered by ``state_mapping``.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    workflow_id: str
    state_mapping: dict[str, str] | None = None


class ProjectWorkflowPickResult(BaseModel):
    """Response of setting a project's workflow pick: the workflow now in effect."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    workflow_id: str | None = None


class WorkflowFallbackPreviewRequest(BaseModel):
    """Request model for previewing the project workflow fallback.

    Provide ``new_type_id`` (+ current ``type_id``) for a re-type preview, or
    ``workflow_id`` (+ ``type_id``) for a workflow-switch preview.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    type_id: str | None = None
    new_type_id: str | None = None
    workflow_id: str | None = None
