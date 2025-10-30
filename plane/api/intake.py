from typing import Any

from ..models.intake import (
    CreateIntakeWorkItem,
    IntakeWorkItem,
    PaginatedIntakeWorkItemResponse,
    UpdateIntakeWorkItem,
)
from ..models.query_params import PaginatedQueryParams, RetrieveQueryParams
from .base_resource import BaseResource


class Intake(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        params: PaginatedQueryParams | None = None,
    ) -> PaginatedIntakeWorkItemResponse:
        """List intake work items in a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters for filtering, ordering, and pagination
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/intake-issues", params=query_params
        )
        return PaginatedIntakeWorkItemResponse.model_validate(response)

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        params: RetrieveQueryParams | None = None,
    ) -> IntakeWorkItem:
        """Retrieve an intake work item by work item ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item (use the issue field from
                IntakeWorkItem response, not the intake work item ID)
            params: Optional query parameters for expand, fields, etc.
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/intake-issues/{work_item_id}",
            params=query_params,
        )
        return IntakeWorkItem.model_validate(response)

    def create(
        self, workspace_slug: str, project_id: str, data: CreateIntakeWorkItem
    ) -> IntakeWorkItem:
        """Create a new intake work item.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Intake work item data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/intake-issues",
            data.model_dump(exclude_none=True),
        )
        return IntakeWorkItem.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        work_item_id: str,
        data: UpdateIntakeWorkItem,
    ) -> IntakeWorkItem:
        """Update an intake work item by work item ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item (use the issue field from
                IntakeWorkItem response, not the intake work item ID)
            data: Updated intake work item data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/intake-issues/{work_item_id}",
            data.model_dump(exclude_none=True),
        )
        return IntakeWorkItem.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, work_item_id: str) -> None:
        """Delete an intake work item by work item ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            work_item_id: UUID of the work item (use the issue field from
                IntakeWorkItem response, not the intake work item ID)
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/intake-issues/{work_item_id}"
        )
