from collections.abc import Mapping
from typing import Any

from ..models.users import UserLite
from .base_resource import BaseResource


class Workspaces(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def get_members(
        self, workspace_slug: str
    ) -> [UserLite]:
        """Get all members of a workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/members")
        return [UserLite.model_validate(item) for item in response or []]
