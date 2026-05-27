from typing import Any

from ...models.workflows import AttachWorkflowStates
from ..base_resource import BaseResource


class WorkflowStates(BaseResource):
    """API client for managing states attached to a workflow."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

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
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/states",
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
            f"{workspace_slug}/projects/{project_id}/workflows/{workflow_id}/states/{state_id}"
        )
