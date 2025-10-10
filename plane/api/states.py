from collections.abc import Mapping
from typing import Any

from ..models.states import CreateState, PaginatedStateResponse, State, UpdateState
from .base_resource import BaseResource


class States(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, project_id: str, data: CreateState) -> State:
        """Create a new state.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: State data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/states",
            data.model_dump(exclude_none=True),
        )
        return State.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str, state_id: str) -> State:
        """Retrieve a state by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            state_id: UUID of the state
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/states/{state_id}")
        return State.model_validate(response)

    def update(
        self, workspace_slug: str, project_id: str, state_id: str, data: UpdateState
    ) -> State:
        """Update a state by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            state_id: UUID of the state
            data: Updated state data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/states/{state_id}",
            data.model_dump(exclude_none=True),
        )
        return State.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, state_id: str) -> None:
        """Delete a state by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            state_id: UUID of the state
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/states/{state_id}")

    def list(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedStateResponse:
        """List states with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/states", params=params)
        return PaginatedStateResponse.model_validate(response)
