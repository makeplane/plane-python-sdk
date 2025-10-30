from collections.abc import Mapping
from typing import Any

from ..models.cycles import (
    CreateCycle,
    Cycle,
    PaginatedArchivedCycleResponse,
    PaginatedCycleResponse,
    PaginatedCycleWorkItemResponse,
    TransferCycleWorkItemsRequest,
    UpdateCycle,
)
from .base_resource import BaseResource


class Cycles(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, project_id: str, data: CreateCycle) -> Cycle:
        """Create a new cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Cycle data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/cycles",
            data.model_dump(exclude_none=True),
        )
        return Cycle.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str, cycle_id: str) -> Cycle:
        """Retrieve a cycle by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}")
        return Cycle.model_validate(response)

    def update(
        self, workspace_slug: str, project_id: str, cycle_id: str, data: UpdateCycle
    ) -> Cycle:
        """Update a cycle by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            data: Updated cycle data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}",
            data.model_dump(exclude_none=True),
        )
        return Cycle.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, cycle_id: str) -> None:
        """Delete a cycle by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}")

    def list(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedCycleResponse:
        """List cycles with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/cycles", params=params)
        return PaginatedCycleResponse.model_validate(response)

    def list_archived(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedArchivedCycleResponse:
        """List archived cycles with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/archived-cycles", params=params
        )
        return PaginatedArchivedCycleResponse.model_validate(response)

    def add_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        cycle_id: str,
        issue_ids: [str],
    ) -> None:
        """Add work items to a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            issue_ids: List of issue IDs to add to the cycle
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues",
            {"issues": issue_ids},
        )

    def remove_work_item(
        self, workspace_slug: str, project_id: str, cycle_id: str, work_item_id: str
    ) -> None:
        """Remove a work item from a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            work_item_id: UUID of the work item
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues/{work_item_id}"
        )

    def list_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        cycle_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedCycleWorkItemResponse:
        """List work items in a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/cycle-issues", params=params
        )
        return PaginatedCycleWorkItemResponse.model_validate(response)

    def transfer_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        cycle_id: str,
        data: TransferCycleWorkItemsRequest,
    ) -> None:
        """Transfer work items from one cycle to another.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the source cycle
            data: Transfer request with target cycle
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/transfer-issues",
            data.model_dump(exclude_none=True),
        )

    def archive(self, workspace_slug: str, project_id: str, cycle_id: str) -> bool:
        """Archive a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        self._post(
            f"{workspace_slug}/projects/{project_id}/cycles/{cycle_id}/archive", {}
        )
        return True

    def unarchive(self, workspace_slug: str, project_id: str, cycle_id: str) -> bool:
        """Unarchive a cycle.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            cycle_id: UUID of the cycle
        """
        self._delete(
            f"{workspace_slug}/projects/{project_id}/archived-cycles/{cycle_id}/unarchive"
        )
        return True
