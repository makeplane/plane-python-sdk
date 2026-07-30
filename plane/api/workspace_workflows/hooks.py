from __future__ import annotations

from typing import Any

from ...models.workflows import (
    CreateWorkflowTransitionHook,
    UpdateWorkflowTransitionHook,
    WorkflowTransitionHook,
)
from ..base_resource import BaseResource


class WorkspaceWorkflowTransitionHooks(BaseResource):
    """API client for hooks attached to workspace workflow transitions."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def _base(self, workspace_slug: str, workflow_id: str, transition_id: str) -> str:
        return f"{workspace_slug}/workflows/{workflow_id}/state-transitions/{transition_id}/hooks"

    def list(
        self, workspace_slug: str, workflow_id: str, transition_id: str
    ) -> list[WorkflowTransitionHook]:
        """List hooks on a workspace workflow transition.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
        """
        data = self._get(f"{self._base(workspace_slug, workflow_id, transition_id)}/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkflowTransitionHook.model_validate(item) for item in items]

    def create(
        self,
        workspace_slug: str,
        workflow_id: str,
        transition_id: str,
        data: CreateWorkflowTransitionHook,
    ) -> WorkflowTransitionHook:
        """Create a hook on a workspace workflow transition.

        For send_webhook handlers the one-shot ``secret_plaintext`` is included
        in the response of this call only.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            data: Hook data (phase, handler_name, config)
        """
        response = self._post(
            f"{self._base(workspace_slug, workflow_id, transition_id)}/",
            data.model_dump(exclude_none=True),
        )
        return WorkflowTransitionHook.model_validate(response)

    def retrieve(
        self, workspace_slug: str, workflow_id: str, transition_id: str, hook_id: str
    ) -> WorkflowTransitionHook:
        """Retrieve a hook by ID.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            hook_id: UUID of the hook
        """
        response = self._get(f"{self._base(workspace_slug, workflow_id, transition_id)}/{hook_id}/")
        return WorkflowTransitionHook.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        workflow_id: str,
        transition_id: str,
        hook_id: str,
        data: UpdateWorkflowTransitionHook,
    ) -> WorkflowTransitionHook:
        """Update a hook (``phase`` and ``handler_name`` are immutable).

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            hook_id: UUID of the hook
            data: Updated hook data
        """
        response = self._patch(
            f"{self._base(workspace_slug, workflow_id, transition_id)}/{hook_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkflowTransitionHook.model_validate(response)

    def delete(
        self, workspace_slug: str, workflow_id: str, transition_id: str, hook_id: str
    ) -> None:
        """Delete a hook.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            hook_id: UUID of the hook
        """
        return self._delete(f"{self._base(workspace_slug, workflow_id, transition_id)}/{hook_id}/")

    def regenerate_secret(
        self, workspace_slug: str, workflow_id: str, transition_id: str, hook_id: str
    ) -> WorkflowTransitionHook:
        """Regenerate a send_webhook hook's secret.

        The new one-shot ``secret_plaintext`` is included in this response only.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            hook_id: UUID of the hook
        """
        response = self._post(
            f"{self._base(workspace_slug, workflow_id, transition_id)}/{hook_id}"
            "/regenerate-webhook-secret/",
            None,
        )
        return WorkflowTransitionHook.model_validate(response)

    def executions(
        self,
        workspace_slug: str,
        workflow_id: str,
        transition_id: str,
        hook_id: str,
    ) -> list[dict[str, Any]]:
        """List a hook's execution history entries.

        Args:
            workspace_slug: The workspace slug identifier
            workflow_id: UUID of the workflow
            transition_id: UUID of the transition
            hook_id: UUID of the hook
        """
        data = self._get(
            f"{self._base(workspace_slug, workflow_id, transition_id)}/{hook_id}/executions/"
        )
        items = data.get("results", data) if isinstance(data, dict) else data
        return list(items) if isinstance(items, list) else [items]
