from typing import Any

from ...models.workspace_workflows import (
    CreateWorkspaceWorkflowTransition,
    UpdateWorkspaceWorkflowTransition,
    WorkspaceWorkflowTransition,
)
from ..base_resource import BaseResource


class WorkspaceWorkflowTransitions(BaseResource):
    """API client for state transitions within a workspace workflow."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, workflow_id: str) -> list[WorkspaceWorkflowTransition]:
        """List all state transitions for a workspace workflow.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
        """
        data = self._get(f"{workspace_slug}/workflows/{workflow_id}/state-transitions/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkspaceWorkflowTransition.model_validate(item) for item in items]

    def create(
        self,
        workspace_slug: str,
        workflow_id: str,
        data: CreateWorkspaceWorkflowTransition,
    ) -> WorkspaceWorkflowTransition:
        """Create a state transition for a workspace workflow.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            data: Transition data (from-state, target state, optional approvers)
        """
        response = self._post(
            f"{workspace_slug}/workflows/{workflow_id}/state-transitions/",
            data.model_dump(exclude_none=True),
        )
        return WorkspaceWorkflowTransition.model_validate(response)

    def retrieve(
        self, workspace_slug: str, workflow_id: str, transition_id: str
    ) -> WorkspaceWorkflowTransition:
        """Retrieve a workspace workflow transition by ID.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
        """
        response = self._get(
            f"{workspace_slug}/workflows/{workflow_id}/state-transitions/{transition_id}/"
        )
        return WorkspaceWorkflowTransition.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        workflow_id: str,
        transition_id: str,
        data: UpdateWorkspaceWorkflowTransition,
    ) -> WorkspaceWorkflowTransition:
        """Update a workspace workflow transition.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            data: Updated transition data
        """
        response = self._patch(
            f"{workspace_slug}/workflows/{workflow_id}/state-transitions/{transition_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkspaceWorkflowTransition.model_validate(response)

    def delete(self, workspace_slug: str, workflow_id: str, transition_id: str) -> None:
        """Delete a workspace workflow transition.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
        """
        return self._delete(
            f"{workspace_slug}/workflows/{workflow_id}/state-transitions/{transition_id}/"
        )
