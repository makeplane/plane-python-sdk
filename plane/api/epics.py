from __future__ import annotations

from typing import Any

from ..models.epics import (
    AddEpicWorkItems,
    CreateEpic,
    Epic,
    EpicIssue,
    PaginatedEpicIssueResponse,
    PaginatedEpicResponse,
    UpdateEpic,
)
from ..models.query_params import PaginatedQueryParams, RetrieveQueryParams
from .base_resource import BaseResource


class Epics(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, project_id: str, data: CreateEpic) -> Epic:
        """Create a new epic in a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Epic creation data
        """
        # enable epics feature flag
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/epics",
            data.model_dump(exclude_none=True),
        )
        return Epic.model_validate(response)

    def retrieve(
        self,
        workspace_slug: str,
        project_id: str,
        epic_id: str,
        params: RetrieveQueryParams | None = None,
    ) -> Epic:
        """Retrieve an epic by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            epic_id: UUID of the epic
            params: Optional query parameters for expand, fields, etc.
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/epics/{epic_id}", params=query_params
        )
        return Epic.model_validate(response)

    def update(
        self, workspace_slug: str, project_id: str, epic_id: str, data: UpdateEpic
    ) -> Epic:
        """Partially update an existing epic.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            epic_id: UUID of the epic
            data: Epic update data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/epics/{epic_id}",
            data.model_dump(exclude_none=True),
        )
        return Epic.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, epic_id: str) -> None:
        """Delete an epic.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            epic_id: UUID of the epic
        """
        self._delete(f"{workspace_slug}/projects/{project_id}/epics/{epic_id}")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        params: PaginatedQueryParams | None = None,
    ) -> PaginatedEpicResponse:
        """List epics in a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters for filtering, ordering, and pagination
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(f"{workspace_slug}/projects/{project_id}/epics", params=query_params)
        return PaginatedEpicResponse.model_validate(response)

    def list_issues(
        self,
        workspace_slug: str,
        project_id: str,
        epic_id: str,
        params: PaginatedQueryParams | None = None,
    ) -> PaginatedEpicIssueResponse:
        """List work items under an epic.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            epic_id: UUID of the epic
            params: Optional query parameters for pagination
        """
        query_params = params.model_dump(exclude_none=True) if params else None
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/epics/{epic_id}/issues",
            params=query_params,
        )
        return PaginatedEpicIssueResponse.model_validate(response)

    def add_issues(
        self,
        workspace_slug: str,
        project_id: str,
        epic_id: str,
        data: AddEpicWorkItems,
    ) -> list[EpicIssue]:
        """Add work items as sub-issues under an epic.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            epic_id: UUID of the epic
            data: Work item IDs to add
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/epics/{epic_id}/issues",
            data.model_dump(exclude_none=True),
        )
        return [EpicIssue.model_validate(item) for item in response]
