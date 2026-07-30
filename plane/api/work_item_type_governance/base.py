from __future__ import annotations

from typing import Any

from ...models.work_item_type_governance import (
    GovernancePreview,
    TypeGovernance,
    TypeGovernancePreviewRequest,
    UpdateTypeGovernance,
)
from ..base_resource import BaseResource
from .pins import WorkItemTypeWorkflowPins
from .project_workflows import ProjectTypeWorkflows


class WorkItemTypeGovernance(BaseResource):
    """API client for work item type governance (workspace governance only).

    Governs which workflows a workspace-level work item type may use
    (``any`` / ``constrained`` / ``required`` modes and allowlists). Per-project
    pins live on ``.pins``; the project-side view of effective workflows and
    picks lives on ``.project_workflows``. Every endpoint requires the workspace
    to own states and workflows — otherwise the API responds 400 with code
    ``workspace_not_managed``.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.pins = WorkItemTypeWorkflowPins(config)
        self.project_workflows = ProjectTypeWorkflows(config)

    def retrieve(self, workspace_slug: str, type_id: str) -> TypeGovernance:
        """Retrieve a type's governance settings (mode, required workflow, allowlist).

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
        """
        response = self._get(f"{workspace_slug}/work-item-types/{type_id}/governance/")
        return TypeGovernance.model_validate(response)

    def update(
        self, workspace_slug: str, type_id: str, data: UpdateTypeGovernance
    ) -> TypeGovernance:
        """Update a type's governance mode / allowlist / required workflow.

        Destructive changes (dropping in-use workflows, mandating one) require
        ``data.acknowledge`` and may need a ``data.state_mapping`` for orphaned
        work items.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            data: The governance change
        """
        response = self._patch(
            f"{workspace_slug}/work-item-types/{type_id}/governance/",
            data.model_dump(exclude_none=True),
        )
        return TypeGovernance.model_validate(response)

    def preview(
        self, workspace_slug: str, type_id: str, data: TypeGovernancePreviewRequest
    ) -> GovernancePreview:
        """Dry-run a governance change and report affected work items (no writes).

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the workspace work item type
            data: The governance change to preview
        """
        response = self._post(
            f"{workspace_slug}/work-item-types/{type_id}/governance/preview/",
            data.model_dump(exclude_none=True),
        )
        payload = response.get("preview", response) if isinstance(response, dict) else response
        return GovernancePreview.model_validate(payload)
