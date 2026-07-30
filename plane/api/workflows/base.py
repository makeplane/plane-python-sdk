from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.workflows import (
    CreateWorkflow,
    SubmitWorkItemApproval,
    UpdateWorkflow,
    Workflow,
    WorkflowActivity,
    WorkItemApprovalResult,
)
from ..base_resource import BaseResource
from .hooks import ProjectWorkflowTransitionHooks
from .states import WorkflowStates
from .transitions import WorkflowTransitions


class Workflows(BaseResource):
    """API client for managing project workflows.

    Under workspace governance workflows are managed at the workspace level
    (see ``WorkspaceWorkflows``) and project-scoped writes respond 400 with
    code ``workspace_managed``.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        self.states = WorkflowStates(config)
        self.transitions = WorkflowTransitions(config)
        self.hooks = ProjectWorkflowTransitionHooks(config)

    def list(self, workspace_slug: str, project_id: str) -> list[Workflow]:
        """List all workflows for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project

        Returns:
            List of workflows
        """
        data = self._get(f"{workspace_slug}/projects/{project_id}/workflows/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [Workflow.model_validate(item) for item in items]

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        data: CreateWorkflow,
    ) -> Workflow:
        """Create a new workflow for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Workflow data

        Returns:
            The created workflow
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/workflows/",
            data.model_dump(exclude_none=True),
        )
        return Workflow.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        data: UpdateWorkflow,
    ) -> Workflow:
        """Update a workflow by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            data: Updated workflow data

        Returns:
            The updated workflow
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/",
            data.model_dump(exclude_none=True),
        )
        return Workflow.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str, workflow_id: str) -> Workflow:
        """Retrieve a workflow by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/")
        return Workflow.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, workflow_id: str) -> None:
        """Delete a workflow by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/")

    def activities(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkflowActivity]:
        """List the workflow's activity/audit entries.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            params: Optional query parameters (e.g. created_at__gt)
        """
        data = self._get(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/activities/",
            params=params,
        )
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkflowActivity.model_validate(item) for item in items]

    def submit_work_item_approval(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: SubmitWorkItemApproval,
    ) -> WorkItemApprovalResult:
        """Approve or reject a work item's pending workflow transition.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item
            data: The approval decision (``type="approve"`` or ``type="reject"``)
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-items/{work_item_id}"
            "/workflow-approval/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemApprovalResult.model_validate(response)
