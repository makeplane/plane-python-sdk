from collections.abc import Iterable, Mapping
from typing import Any

from ...models.users import PaginatedUserLiteResponse, UserLite
from ..base_resource import BaseResource


class TeamspaceMembers(BaseResource):
    """API client for managing members associated with teamspaces."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, teamspace_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedUserLiteResponse:
        """List members associated with a teamspace.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
            params: Optional query parameters (e.g., per_page, cursor)

        Returns:
            Paginated list of members
        """
        response = self._get(
            f"{workspace_slug}/teamspaces/{teamspace_id}/members", params=params
        )
        return PaginatedUserLiteResponse.model_validate(response)

    def add(
        self, workspace_slug: str, teamspace_id: str, member_ids: Iterable[str]
    ) -> Iterable[UserLite]:
        """Add members to a teamspace.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
            member_ids: List of member UUIDs to add

        Returns:
            List of added members
        """
        response = self._post(
            f"{workspace_slug}/teamspaces/{teamspace_id}/members",
            {"member_ids": member_ids},
        )
        return [UserLite.model_validate(member) for member in response]

    def remove(self, workspace_slug: str, teamspace_id: str, member_ids: Iterable[str]) -> None:
        """Remove members from a teamspace.

        Args:
            workspace_slug: The workspace slug identifier
            teamspace_id: UUID of the teamspace
            member_ids: List of member UUIDs to remove
        """
        return self._delete(
            f"{workspace_slug}/teamspaces/{teamspace_id}/members",
            {"member_ids": member_ids},
        )

