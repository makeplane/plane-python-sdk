from typing import Any

from ...models.workspace_workflows import (
    AddWorkspaceWorkflowStates,
    RemoveWorkspaceWorkflowState,
    UpdateWorkspaceWorkflowState,
    WorkspaceWorkflowState,
)
from ..base_resource import BaseResource


def _validate_chain(response: Any) -> list[WorkspaceWorkflowState]:
    items = response.get("results", response) if isinstance(response, dict) else response
    if not isinstance(items, list):
        items = [items]
    return [WorkspaceWorkflowState.model_validate(item) for item in items]


class WorkspaceWorkflowStates(BaseResource):
    """API client for a workspace workflow's chain (state memberships)."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def add(
        self,
        workspace_slug: str,
        workflow_id: str,
        data: AddWorkspaceWorkflowStates,
    ) -> list[WorkspaceWorkflowState]:
        """Append catalog states to the workflow's chain.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            data: Request body with the catalog state IDs to append

        Returns:
            The updated chain rows
        """
        response = self._post(
            f"{workspace_slug}/workflows/{workflow_id}/states/",
            data.model_dump(exclude_none=True),
        )
        return _validate_chain(response)

    def update(
        self,
        workspace_slug: str,
        workflow_id: str,
        state_id: str,
        data: UpdateWorkspaceWorkflowState,
    ) -> WorkspaceWorkflowState:
        """Update a chain membership row (type, allow_issue_creation, is_default).

        Changing ``type`` removes the row's existing transitions server-side.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            state_id: UUID of the catalog state
            data: Updated membership data
        """
        response = self._patch(
            f"{workspace_slug}/workflows/{workflow_id}/states/{state_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkspaceWorkflowState.model_validate(response)

    def remove(
        self,
        workspace_slug: str,
        workflow_id: str,
        state_id: str,
        data: RemoveWorkspaceWorkflowState | None = None,
    ) -> None:
        """Remove a state from the chain.

        Orphan-gated: every work item stranded by the removal must be covered
        by ``data.state_mapping`` (409 with an orphan report otherwise).
        Removing the default state requires ``data.new_default_state_id``;
        transitions referencing the state must be removed first.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            state_id: UUID of the catalog state
            data: Optional removal options (new default, orphan state mapping)
        """
        return self._delete(
            f"{workspace_slug}/workflows/{workflow_id}/states/{state_id}/",
            data=data.model_dump(exclude_none=True) if data is not None else None,
        )

    def mark_default(
        self, workspace_slug: str, workflow_id: str, state_id: str
    ) -> WorkspaceWorkflowState | None:
        """Mark a chain state as the workflow's default.

        Also force-enables work-item creation on that state.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            state_id: UUID of the catalog state
        """
        response = self._post(
            f"{workspace_slug}/workflows/{workflow_id}/states/{state_id}/mark-default/",
            None,
        )
        if response is None:
            return None
        return WorkspaceWorkflowState.model_validate(response)
