from typing import Any

from ..models.work_item_type_governance import (
    CreateWorkItemTypeWorkflowPins,
    GovernancePreview,
    ProjectTypeWorkflow,
    SetProjectWorkflowPick,
    TypeGovernance,
    TypeGovernancePreviewRequest,
    UpdateTypeGovernance,
    WorkflowFallbackPreviewRequest,
    WorkItemTypeWorkflowPin,
)
from .base_resource import BaseResource


class WorkItemTypeGovernance(BaseResource):
    """API client for work item type governance (workspace governance only).

    Governs which workflows a workspace-level work item type may use
    (``any`` / ``constrained`` / ``required`` modes, allowlists, and pins) and
    exposes the project-side view: each type's effective workflow and the
    project's workflow pick. Every endpoint requires the workspace to own
    states and workflows — otherwise the API responds 400 with code
    ``workspace_not_managed``.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    # --- type-side governance (workspace scope) ---

    def retrieve(self, workspace_slug: str, type_id: str) -> TypeGovernance:
        """Get a type's governance settings (mode, required workflow, allowlist).

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
        """
        response = self._get(f"{workspace_slug}/work-item-types/{type_id}/governance/")
        return TypeGovernance.model_validate(response)

    def update(
        self, workspace_slug: str, type_id: str, data: UpdateTypeGovernance
    ) -> TypeGovernance:
        """Change a type's governance mode / allowlist / required workflow.

        Destructive changes (dropping in-use workflows, mandating one) require
        ``acknowledge`` and may need a ``state_mapping`` for orphaned items.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            data: The governance change
        """
        response = self._patch(
            f"{workspace_slug}/work-item-types/{type_id}/governance/",
            data.model_dump(exclude_none=True),
        )
        return TypeGovernance.model_validate(response)

    def preview(
        self, workspace_slug: str, type_id: str, data: TypeGovernancePreviewRequest
    ) -> GovernancePreview:
        """Dry-run a governance change and report affected work items (no writes).

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            data: The governance change to preview
        """
        response = self._post(
            f"{workspace_slug}/work-item-types/{type_id}/governance/preview/",
            data.model_dump(exclude_none=True),
        )
        payload = response.get("preview", response) if isinstance(response, dict) else response
        return GovernancePreview.model_validate(payload)

    # --- pins (workspace scope) ---

    def list_pins(self, workspace_slug: str, type_id: str) -> list[WorkItemTypeWorkflowPin]:
        """List a type's project-to-workflow pins.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
        """
        data = self._get(f"{workspace_slug}/work-item-types/{type_id}/governance/pins/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkItemTypeWorkflowPin.model_validate(item) for item in items]

    def create_pins(
        self, workspace_slug: str, type_id: str, data: CreateWorkItemTypeWorkflowPins
    ) -> list[WorkItemTypeWorkflowPin]:
        """Pin a workflow for this type across one or more projects.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            data: The workflow and target projects
        """
        response = self._post(
            f"{workspace_slug}/work-item-types/{type_id}/governance/pins/",
            data.model_dump(exclude_none=True),
        )
        items = response.get("results", response) if isinstance(response, dict) else response
        return [WorkItemTypeWorkflowPin.model_validate(item) for item in items]

    def delete_pin(self, workspace_slug: str, type_id: str, pin_id: str) -> None:
        """Remove a pin.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            pin_id: UUID of the pin
        """
        return self._delete(f"{workspace_slug}/work-item-types/{type_id}/governance/pins/{pin_id}/")

    # --- project-side view (picks and effective workflows) ---

    def list_project_type_workflows(
        self, workspace_slug: str, project_id: str
    ) -> list[ProjectTypeWorkflow]:
        """List every active type's governance pill, effective workflow, and
        pickable options for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        data = self._get(f"{workspace_slug}/projects/{project_id}/work-item-types/workflows/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [ProjectTypeWorkflow.model_validate(item) for item in items]

    def retrieve_project_type_workflow(
        self, workspace_slug: str, project_id: str, type_id: str
    ) -> ProjectTypeWorkflow:
        """Get one type's governance pill and effective workflow in a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/workflows/"
        )
        return ProjectTypeWorkflow.model_validate(response)

    def retrieve_project_pick(
        self, workspace_slug: str, project_id: str, type_id: str
    ) -> ProjectTypeWorkflow:
        """Get the project's current workflow pick context for a type.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/workflow/"
        )
        return ProjectTypeWorkflow.model_validate(response)

    def update_project_pick(
        self,
        workspace_slug: str,
        project_id: str,
        type_id: str,
        data: SetProjectWorkflowPick,
    ) -> dict[str, Any]:
        """Set the project's workflow pick for a type.

        Runs the workflow fallback for stranded work items; every orphan must
        be covered by ``data.state_mapping`` (400 with an orphan report
        otherwise). Returns ``{"workflow_id": "<picked id>"}``.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            data: The pick (workflow and optional orphan state mapping)
        """
        response = self._put(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/workflow/",
            data.model_dump(exclude_none=True),
        )
        return response if isinstance(response, dict) else {"workflow_id": response}

    def preview_project_workflow_fallback(
        self, workspace_slug: str, project_id: str, data: WorkflowFallbackPreviewRequest
    ) -> GovernancePreview:
        """Dry-run the project's workflow fallback (re-type / switch dialogs).

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: The scenario to preview (re-type or workflow switch)
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/workflow-fallback-preview/",
            data.model_dump(exclude_none=True),
        )
        payload = response.get("preview", response) if isinstance(response, dict) else response
        return GovernancePreview.model_validate(payload)
