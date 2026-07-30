from typing import Any

from ...models.workflows import AttachWorkflowStates, UpdateWorkflowState, WorkflowState
from ..base_resource import BaseResource


class WorkflowStates(BaseResource):
    """API client for managing states attached to a workflow."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, project_id: str, workflow_id: str) -> list[WorkflowState]:
        """List the states attached to a workflow.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
        """
        data = self._get(f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/states/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkflowState.model_validate(item) for item in items]

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        state_id: str,
        data: UpdateWorkflowState,
    ) -> WorkflowState | None:
        """Update a state's membership row (type, allow_issue_creation, is_default).

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            state_id: UUID of the state
            data: Updated membership data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/states/{state_id}/",
            data.model_dump(exclude_none=True),
        )
        if response is None:
            return None
        return WorkflowState.model_validate(response)

    def transfer(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        state_id: str,
        new_state_id: str,
    ) -> None:
        """Transfer work items off a state and remove it from the workflow.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            state_id: UUID of the state being removed
            new_state_id: UUID of the state that receives its work items
        """
        self._post(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}"
            f"/states/{state_id}/transfer/",
            {"new_state_id": new_state_id},
        )

    def attach(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        data: AttachWorkflowStates,
    ) -> None:
        """Attach states to a workflow.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            data: Request body containing the list of state IDs to attach
        """
        self._post(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/states/",
            data.model_dump(exclude_none=True),
        )

    def detach(
        self,
        workspace_slug: str,
        project_id: str,
        workflow_id: str,
        state_id: str,
    ) -> None:
        """Detach a state from a workflow.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            workflow_id: UUID of the workflow
            state_id: UUID of the state to detach
        """
        self._delete(
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/states/{state_id}/"
        )
