from __future__ import annotations

from typing import Any, Literal

from ..models.roles import PaginatedRoleResponse, Role
from .base_resource import BaseResource


class Roles(BaseResource):
    """API client for workspace and project role definitions.

    Roles are defined at the workspace level. ``namespace="workspace"`` returns
    workspace-level roles (Owner / Admin / Member / Guest); ``namespace="project"``
    returns the project-role definitions available across the workspace (Admin /
    Contributor / Commenter / Guest). The project-role definitions are shared by
    every project in the workspace — there is no per-project roles endpoint, so
    this resource takes no project id.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        namespace: Literal["workspace", "project"] | None = None,
        per_page: int | None = None,
        cursor: str | None = None,
    ) -> PaginatedRoleResponse:
        """List role definitions in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            namespace: Optional filter — ``"workspace"`` for workspace-level
                roles, ``"project"`` for project-role definitions. When omitted,
                both are returned, ordered by namespace, sort order, then name.
            per_page: Number of results per page (server default 20)
            cursor: Pagination cursor from a previous response's ``next_cursor``
        """
        params: dict[str, Any] = {}
        if namespace is not None:
            params["namespace"] = namespace
        if per_page is not None:
            params["per_page"] = per_page
        if cursor is not None:
            params["cursor"] = cursor

        response = self._get(f"{workspace_slug}/roles", params=params if params else None)
        return PaginatedRoleResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, role_id: str) -> Role:
        """Retrieve a single role definition by id.

        Args:
            workspace_slug: The workspace slug identifier
            role_id: UUID of the role
        """
        response = self._get(f"{workspace_slug}/roles/{role_id}")
        return Role.model_validate(response)
