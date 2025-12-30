from typing import Any

from ...models.agent_runs import AgentRun, CreateAgentRun
from ..base_resource import BaseResource
from .activities import AgentRunActivities


class AgentRuns(BaseResource):
    """Agent Runs API resource.

    Handles all agent run operations.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.activities = AgentRunActivities(config)

    def create(
        self,
        workspace_slug: str,
        data: CreateAgentRun,
    ) -> AgentRun:
        """Create a new agent run.

        Args:
            workspace_slug: The workspace slug identifier
            data: The agent run data to create

        Returns:
            The created agent run
        """
        response = self._post(
            f"{workspace_slug}/runs",
            data.model_dump(exclude_none=True),
        )
        return AgentRun.model_validate(response)

    def retrieve(
        self,
        workspace_slug: str,
        run_id: str,
    ) -> AgentRun:
        """Retrieve an agent run by ID.

        Args:
            workspace_slug: The workspace slug identifier
            run_id: UUID of the agent run

        Returns:
            The agent run
        """
        response = self._get(f"{workspace_slug}/runs/{run_id}")
        return AgentRun.model_validate(response)