from collections.abc import Mapping
from typing import Any

from ..models.states import (
    CreateWorkspaceState,
    PaginatedStateResponse,
    State,
    UpdateWorkspaceState,
)
from .base_resource import BaseResource


class WorkspaceStates(BaseResource):
    """API client for workspace-level work-item states.

    Reads are dual-mode: under workspace governance ``list``/``retrieve`` serve
    the workspace states catalog; in ungoverned workspaces they aggregate the
    states of every project the caller can access. Writes are only available
    when the workspace owns states and workflows — otherwise the API responds
    400 with code ``workspace_not_managed``. Check
    ``Workspaces.get_features(...).states_owned_by_workspace`` to know which
    mode a workspace is in.

    Not to be confused with ``WorkspaceProjectStates`` (``{slug}/project-states/``),
    which manages project *lifecycle* states.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedStateResponse:
        """List states at workspace scope.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters (e.g. cursor, per_page)
        """
        response = self._get(f"{workspace_slug}/states/", params=params)
        return PaginatedStateResponse.model_validate(response)

    def retrieve_by_external_id(
        self, workspace_slug: str, external_id: str, external_source: str
    ) -> State:
        """Retrieve a workspace state by its external ID and source.

        Args:
            workspace_slug: The workspace slug identifier
            external_id: External identifier of the state
            external_source: External source system name
        """
        response = self._get(
            f"{workspace_slug}/states/",
            params={"external_id": external_id, "external_source": external_source},
        )
        return State.model_validate(response)

    def create(self, workspace_slug: str, data: CreateWorkspaceState) -> State:
        """Create a new workspace (catalog) state.

        Governed workspaces only (400 ``workspace_not_managed`` otherwise).
        Catalog state names are workspace-unique — a duplicate name responds
        409 with code ``state_name_in_use``.

        Args:
            workspace_slug: The workspace slug identifier
            data: State data (name, color, and one of the five lifecycle groups)
        """
        response = self._post(f"{workspace_slug}/states/", data.model_dump(exclude_none=True))
        return State.model_validate(response)

    def retrieve(self, workspace_slug: str, state_id: str) -> State:
        """Retrieve a workspace state by ID.

        Args:
            workspace_slug: The workspace slug identifier
            state_id: UUID of the state
        """
        response = self._get(f"{workspace_slug}/states/{state_id}/")
        return State.model_validate(response)

    def update(self, workspace_slug: str, state_id: str, data: UpdateWorkspaceState) -> State:
        """Update a workspace (catalog) state by ID.

        Governed workspaces only. The triage state cannot be updated, and the
        ``default`` flag is managed by the workflow's default state.

        Args:
            workspace_slug: The workspace slug identifier
            state_id: UUID of the state
            data: Updated state data
        """
        response = self._patch(
            f"{workspace_slug}/states/{state_id}/", data.model_dump(exclude_none=True)
        )
        return State.model_validate(response)

    def delete(self, workspace_slug: str, state_id: str) -> None:
        """Delete a workspace (catalog) state by ID.

        Governed workspaces only. Deletion is blocked (400) while any workflow
        chain references the state or any work item still points at it; the
        triage state is never deletable.

        Args:
            workspace_slug: The workspace slug identifier
            state_id: UUID of the state
        """
        return self._delete(f"{workspace_slug}/states/{state_id}/")
