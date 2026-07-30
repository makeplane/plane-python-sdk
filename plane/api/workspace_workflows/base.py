from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ...models.workflows import WorkflowActivity
from ...models.workspace_workflows import (
    CreateWorkspaceWorkflow,
    PaginatedWorkspaceWorkflowResponse,
    UpdateWorkspaceWorkflow,
    WorkspaceWorkflow,
    WorkspaceWorkflowUsage,
)
from ..base_resource import BaseResource
from .hooks import WorkspaceWorkflowTransitionHooks
from .states import WorkspaceWorkflowStates
from .transitions import WorkspaceWorkflowTransitions


class WorkspaceWorkflows(BaseResource):
    """API client for the workspace workflow catalog.

    ``list`` is dual-mode: under workspace governance it serves the workspace
    workflow catalog; in ungoverned workspaces it aggregates project workflows.
    All writes require the workspace to own states and workflows — otherwise
    the API responds 400 with code ``workspace_not_managed``.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        self.states = WorkspaceWorkflowStates(config)
        self.transitions = WorkspaceWorkflowTransitions(config)
        self.hooks = WorkspaceWorkflowTransitionHooks(config)

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedWorkspaceWorkflowResponse:
        """List workspace workflows.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters (search, is_active, sort_by,
                sort_order, cursor, per_page)
        """
        response = self._get(f"{workspace_slug}/workflows/", params=params)
        return PaginatedWorkspaceWorkflowResponse.model_validate(response)

    def create(self, workspace_slug: str, data: CreateWorkspaceWorkflow) -> WorkspaceWorkflow:
        """Create a workspace workflow draft (configure its chain via ``states``).

        Workflow names are workspace-unique.

        Args:
            workspace_slug: The workspace slug identifier
            data: Workflow data
        """
        response = self._post(f"{workspace_slug}/workflows/", data.model_dump(exclude_none=True))
        return WorkspaceWorkflow.model_validate(response)

    def retrieve(self, workspace_slug: str, workflow_id: str) -> WorkspaceWorkflow:
        """Retrieve a workspace workflow with its full chain.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
        """
        response = self._get(f"{workspace_slug}/workflows/{workflow_id}/")
        return WorkspaceWorkflow.model_validate(response)

    def update(
        self, workspace_slug: str, workflow_id: str, data: UpdateWorkspaceWorkflow
    ) -> WorkspaceWorkflow:
        """Update workspace workflow metadata (name, description, is_active).

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            data: Updated workflow data
        """
        response = self._patch(
            f"{workspace_slug}/workflows/{workflow_id}/", data.model_dump(exclude_none=True)
        )
        return WorkspaceWorkflow.model_validate(response)

    def delete(self, workspace_slug: str, workflow_id: str) -> None:
        """Delete a workspace workflow.

        The default workflow and workflows in use by projects cannot be deleted.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
        """
        return self._delete(f"{workspace_slug}/workflows/{workflow_id}/")

    def usage(self, workspace_slug: str, workflow_id: str) -> WorkspaceWorkflowUsage:
        """Report which projects/types resolve to this workflow, and which types
        mandate or allow it.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
        """
        response = self._get(f"{workspace_slug}/workflows/{workflow_id}/usage/")
        return WorkspaceWorkflowUsage.model_validate(response)

    def activities(
        self,
        workspace_slug: str,
        workflow_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkflowActivity]:
        """List the workflow's activity/audit entries.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            params: Optional query parameters (e.g. created_at__gt, cursor,
                per_page)
        """
        data = self._get(f"{workspace_slug}/workflows/{workflow_id}/activities/", params=params)
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkflowActivity.model_validate(item) for item in items]
