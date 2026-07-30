from __future__ import annotations

from typing import Any

from ...models.work_item_type_governance import (
    CreateWorkItemTypeWorkflowPins,
    WorkItemTypeWorkflowPin,
)
from ..base_resource import BaseResource


class WorkItemTypeWorkflowPins(BaseResource):
    """API client for a work item type's per-project workflow pins.

    A pin forces one project to resolve a type to a specific workflow,
    overriding the workspace default and the constrained allowlist.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, type_id: str) -> list[WorkItemTypeWorkflowPin]:
        """List a type's project-to-workflow pins.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
        """
        data = self._get(f"{workspace_slug}/work-item-types/{type_id}/governance/pins/")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkItemTypeWorkflowPin.model_validate(item) for item in items]

    def create(
        self, workspace_slug: str, type_id: str, data: CreateWorkItemTypeWorkflowPins
    ) -> list[WorkItemTypeWorkflowPin]:
        """Pin a workflow for this type across one or more projects.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            data: The workflow and the target projects

        Returns:
            The type's pins after the change
        """
        response = self._post(
            f"{workspace_slug}/work-item-types/{type_id}/governance/pins/",
            data.model_dump(exclude_none=True),
        )
        items = response.get("results", response) if isinstance(response, dict) else response
        return [WorkItemTypeWorkflowPin.model_validate(item) for item in items]

    def delete(self, workspace_slug: str, type_id: str, pin_id: str) -> None:
        """Remove a pin.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            pin_id: UUID of the pin
        """
        return self._delete(f"{workspace_slug}/work-item-types/{type_id}/governance/pins/{pin_id}/")
