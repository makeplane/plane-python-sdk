from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from ..models.milestones import (
    CreateMilestone,
    Milestone,
    MilestoneWorkItem,
    PaginatedMilestoneResponse,
    PaginatedMilestoneWorkItemResponse,
    UpdateMilestone,
)
from .base_resource import BaseResource


class Milestones(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, project_id: str, data: CreateMilestone) -> Milestone:
        """Create a new milestone.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Milestone data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/milestones",
            data.model_dump(exclude_none=True),
        )
        return Milestone.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str, milestone_id: str) -> Milestone:
        """Retrieve a milestone by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            milestone_id: UUID of the milestone
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/milestones/{milestone_id}")
        return Milestone.model_validate(response)

    def update(
        self, workspace_slug: str, project_id: str, milestone_id: str, data: UpdateMilestone
    ) -> Milestone:
        """Update a milestone by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            milestone_id: UUID of the milestone
            data: Updated milestone data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/milestones/{milestone_id}",
            data.model_dump(exclude_none=True),
        )
        return Milestone.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, milestone_id: str) -> None:
        """Delete a milestone by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            milestone_id: UUID of the milestone
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/milestones/{milestone_id}")

    def list(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedMilestoneResponse:
        """List milestones with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/milestones", params=params)
        return PaginatedMilestoneResponse.model_validate(response)

    def add_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        milestone_id: str,
        issue_ids: list[str],
    ) -> None:
        """Add work items to a milestone.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            milestone_id: UUID of the milestone
            issue_ids: List of issue IDs to add to the milestone
        """
        return self._post(
            f"{workspace_slug}/projects/{project_id}/milestones/{milestone_id}/work-items",
            {"issues": issue_ids},
        )

    def remove_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        milestone_id: str,
        issue_ids: list[str],
    ) -> None:
        """Remove work items from a milestone.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            milestone_id: UUID of the milestone
            issue_ids: List of issue IDs to remove from the milestone
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/milestones/{milestone_id}/work-items",
            {"issues": issue_ids},
        )

    def list_work_items(
        self,
        workspace_slug: str,
        project_id: str,
        milestone_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedMilestoneWorkItemResponse:
        """List work items in a milestone.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            milestone_id: UUID of the milestone
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/milestones/{milestone_id}/work-items",
            params=params,
        )
        return PaginatedMilestoneWorkItemResponse.model_validate(response)
