from __future__ import annotations

from typing import Any

from ...models.work_item_type_governance import (
    GovernancePreview,
    ProjectTypeWorkflow,
    ProjectWorkflowPickResult,
    SetProjectWorkflowPick,
    WorkflowFallbackPreviewRequest,
)
from ..base_resource import BaseResource


class ProjectTypeWorkflows(BaseResource):
    """API client for the project side of work item type governance.

    Reports each active type's governance mode and the workflow it effectively
    resolves to within a project, and manages the project's own workflow pick
    for a type.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, project_id: str) -> list[ProjectTypeWorkflow]:
        """List every active type's governance mode, effective workflow, and
        pickable options for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
        """
        data = self._get(f"{workspace_slug}/projects/{project_id}/work-item-types/workflows/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [ProjectTypeWorkflow.model_validate(item) for item in items]

    def retrieve(self, workspace_slug: str, project_id: str, type_id: str) -> ProjectTypeWorkflow:
        """Retrieve one type's governance mode and effective workflow in a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/workflows/"
        )
        return ProjectTypeWorkflow.model_validate(response)

    def retrieve_pick(
        self, workspace_slug: str, project_id: str, type_id: str
    ) -> ProjectTypeWorkflow:
        """Retrieve the project's current workflow pick context for a type.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/workflow/"
        )
        return ProjectTypeWorkflow.model_validate(response)

    def update_pick(
        self,
        workspace_slug: str,
        project_id: str,
        type_id: str,
        data: SetProjectWorkflowPick,
    ) -> ProjectWorkflowPickResult:
        """Set the project's workflow pick for a type.

        Runs the workflow fallback for stranded work items; every orphan must be
        covered by ``data.state_mapping`` (400 with an orphan report otherwise).

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            type_id: UUID of the work item type
            data: The pick (workflow and optional orphan state mapping)

        Returns:
            The workflow now in effect for this project and type
        """
        response = self._put(
            f"{workspace_slug}/projects/{project_id}/work-item-types/{type_id}/workflow/",
            data.model_dump(exclude_none=True),
        )
        payload = response if isinstance(response, dict) else {"workflow_id": response}
        return ProjectWorkflowPickResult.model_validate(payload)

    def preview_fallback(
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
