from typing import Any

from ...models.workflows import (
    CreateWorkflowTransition,
    UpdateWorkflowTransition,
    WorkflowTransition,
)
from ..base_resource import BaseResource


class WorkflowTransitions(BaseResource):
    """API client for managing state transitions within a workflow."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
    ) -> list[WorkflowTransition]:
        """List all state transitions for a workflow.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow

        Returns:
            List of workflow transitions
        """
        data = self._get(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/state-transitions"
        )
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkflowTransition.model_validate(item) for item in items]

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        data: CreateWorkflowTransition,
    ) -> WorkflowTransition | None:
        """Create a new state transition for a workflow.

        Returns None if the transition already exists (HTTP 400).

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            data: Transition data

        Returns:
            The created workflow transition, or None if it already exists
        """
        from ...errors.errors import HttpError

        try:
            response = self._post(
                f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/state-transitions",
                data.model_dump(exclude_none=True),
            )
        except HttpError as exc:
            if exc.status_code == 400 and "already exists" in str(exc.response).lower():
                return None
            raise
        return WorkflowTransition.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        transition_id: str,
        data: UpdateWorkflowTransition,
    ) -> None:
        """Update a workflow state transition.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            data: Updated transition data
        """
        self._patch(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}"
            f"/state-transitions/{transition_id}",
            data.model_dump(exclude_none=True),
        )

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        transition_id: str,
    ) -> None:
        """Delete a workflow state transition.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
        """
        self._delete(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}"
            f"/state-transitions/{transition_id}"
        )
