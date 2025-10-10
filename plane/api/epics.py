from typing import Any

from ..models.epics import Epic, PaginatedEpicResponse
from ..models.query_params import PaginatedQueryParams, RetrieveQueryParams
from .base_resource import BaseResource


class Epics(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

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
