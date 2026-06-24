from __future__ import annotations

from typing import Any

from ..models.query_params import MemberListQueryParams, MemberQueryParams
from ..models.workspaces import (
    PaginatedWorkspaceMemberResponse,
    WorkspaceFeature,
    WorkspaceMember,
)
from .base_resource import BaseResource


class Workspaces(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def get_members(
        self, workspace_slug: str, params: MemberQueryParams | None = None
    ) -> list[WorkspaceMember]:
        """Get all members of a workspace (unpaginated).

        Returns a list of WorkspaceMember objects that include role (int) and
        role_slug (str) fields in addition to basic identity fields.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional filter query parameters (first_name, last_name,
                email, display_name, role_slug, is_active, is_bot)
        """
        response = self._get(
            f"{workspace_slug}/members",
            params=params.to_query_params() if params else None,
        )
        return [WorkspaceMember.model_validate(item) for item in response or []]

    def get_members_lite(
        self, workspace_slug: str, params: MemberListQueryParams | None = None
    ) -> PaginatedWorkspaceMemberResponse:
        """List workspace members as a paginated "lite" response.

        Unlike :meth:`get_members` (which returns a bare list), this returns a
        cursor-paginated envelope. To page through every member, follow
        ``response.next_cursor`` while ``response.next_page_results`` is True.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional filter + pagination query parameters (the
                :meth:`get_members` filters plus ``cursor`` and ``per_page``)
        """
        response = self._get(
            f"{workspace_slug}/members-lite",
            params=params.to_query_params() if params else None,
        )
        return PaginatedWorkspaceMemberResponse.model_validate(response)

    def get_features(self, workspace_slug: str) -> WorkspaceFeature:
        """Get features of a workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/features")
        return WorkspaceFeature.model_validate(response)

    def update_features(self, workspace_slug: str, data: WorkspaceFeature) -> WorkspaceFeature:
        """Update features of a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Updated workspace features
        """
        response = self._patch(f"{workspace_slug}/features", data.model_dump(exclude_none=True))
        return WorkspaceFeature.model_validate(response)
