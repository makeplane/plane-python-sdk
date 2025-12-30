from collections.abc import Mapping
from typing import Any

from ...models.agent_runs import (
    AgentRunActivity,
    CreateAgentRunActivity,
    PaginatedAgentRunActivityResponse,
)
from ..base_resource import BaseResource


class AgentRunActivities(BaseResource):
    """Agent Run Activities API resource.

    Handles all agent run activity operations.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        run_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> PaginatedAgentRunActivityResponse:
        """List activities for an agent run.

        Args:
            workspace_slug: The workspace slug identifier
            run_id: UUID of the agent run
            params: Optional query parameters for pagination (per_page, cursor)

        Returns:
            Paginated list of agent run activities
        """
        response = self._get(
            f"{workspace_slug}/runs/{run_id}/activities",
            params=params,
        )
        return PaginatedAgentRunActivityResponse.model_validate(response)

    def retrieve(
        self,
        workspace_slug: str,
        run_id: str,
        activity_id: str,
    ) -> AgentRunActivity:
        """Retrieve a specific agent run activity by ID.

        Args:
            workspace_slug: The workspace slug identifier
            run_id: UUID of the agent run
            activity_id: UUID of the activity

        Returns:
            The agent run activity
        """
        response = self._get(
            f"{workspace_slug}/runs/{run_id}/activities/{activity_id}"
        )
        return AgentRunActivity.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        run_id: str,
        data: CreateAgentRunActivity,
    ) -> AgentRunActivity:
        """Create a new agent run activity.

        Args:
            workspace_slug: The workspace slug identifier
            run_id: UUID of the agent run
            data: The activity data to create

        Returns:
            The created agent run activity
        """
        response = self._post(
            f"{workspace_slug}/runs/{run_id}/activities",
            data.model_dump(exclude_none=True),
        )
        return AgentRunActivity.model_validate(response)

