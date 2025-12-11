"""Unit tests for AgentRuns API resource (smoke tests with real HTTP requests)."""

import os
import time

import pytest

from plane.client import PlaneClient
from plane.models.agent_runs import (
    AgentRun,
    AgentRunActivity,
    AgentRunType,
    CreateAgentRun,
    CreateAgentRunActivity,
    PaginatedAgentRunActivityResponse,
)
from plane.models.projects import Project


@pytest.fixture(scope="module")
def agent_slug() -> str:
    """Get agent slug from environment variable."""
    slug = os.getenv("AGENT_SLUG")
    if not slug:
        pytest.skip("AGENT_SLUG environment variable not set")
    return slug


class TestAgentRunsAPI:
    """Test AgentRuns API resource."""

    @pytest.fixture
    def agent_run_data(self, agent_slug: str, project: Project) -> CreateAgentRun:
        """Create test agent run data."""
        return CreateAgentRun(
            agent_slug=agent_slug,
            project=project.id,
            type=AgentRunType.COMMENT_THREAD,
        )

    @pytest.fixture
    def agent_run(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run_data: CreateAgentRun,
    ) -> AgentRun:
        """Create a test agent run and yield it."""
        agent_run = client.agent_runs.create(workspace_slug, agent_run_data)
        yield agent_run
        # Note: Agent runs typically don't have a delete endpoint

    def test_create_agent_run(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run_data: CreateAgentRun,
    ) -> None:
        """Test creating an agent run."""
        agent_run = client.agent_runs.create(workspace_slug, agent_run_data)
        assert agent_run is not None
        assert agent_run.id is not None
        assert agent_run.workspace is not None
        assert agent_run.status is not None
        assert agent_run.type == AgentRunType.COMMENT_THREAD

    def test_retrieve_agent_run(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run: AgentRun,
    ) -> None:
        """Test retrieving an agent run."""
        retrieved = client.agent_runs.retrieve(workspace_slug, agent_run.id)
        assert retrieved is not None
        assert retrieved.id == agent_run.id
        assert retrieved.workspace == agent_run.workspace
        assert retrieved.status is not None

    def test_resume_agent_run(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run: AgentRun,
    ) -> None:
        """Test resuming an agent run."""
        resumed = client.agent_runs.resume(workspace_slug, agent_run.id)
        assert resumed is not None
        assert resumed.id == agent_run.id


class TestAgentRunActivitiesAPI:
    """Test AgentRunActivities API resource."""

    @pytest.fixture
    def agent_run_data(self, agent_slug: str, project: Project) -> CreateAgentRun:
        """Create test agent run data."""
        return CreateAgentRun(
            agent_slug=agent_slug,
            project=project.id,
            type=AgentRunType.COMMENT_THREAD,
        )

    @pytest.fixture
    def agent_run(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run_data: CreateAgentRun,
    ) -> AgentRun:
        """Create a test agent run and yield it."""
        agent_run = client.agent_runs.create(workspace_slug, agent_run_data)
        yield agent_run

    @pytest.fixture
    def activity_data(self, project: Project) -> CreateAgentRunActivity:
        """Create test activity data."""
        return CreateAgentRunActivity(
            type="response",
            content={"type": "response", "body": f"Test activity {int(time.time())}"},
            project=project.id,
        )

    @pytest.fixture
    def activity(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run: AgentRun,
        activity_data: CreateAgentRunActivity,
    ) -> AgentRunActivity:
        """Create a test activity and yield it."""
        activity = client.agent_runs.activities.create(
            workspace_slug, agent_run.id, activity_data
        )
        yield activity

    def test_list_activities(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run: AgentRun,
    ) -> None:
        """Test listing activities for an agent run."""
        response = client.agent_runs.activities.list(workspace_slug, agent_run.id)
        assert response is not None
        assert isinstance(response, PaginatedAgentRunActivityResponse)
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    def test_list_activities_with_pagination(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run: AgentRun,
    ) -> None:
        """Test listing activities with pagination parameters."""
        response = client.agent_runs.activities.list(
            workspace_slug, agent_run.id, params={"per_page": 10}
        )
        assert response is not None
        assert isinstance(response, PaginatedAgentRunActivityResponse)
        assert hasattr(response, "results")

    def test_create_activity(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run: AgentRun,
        activity_data: CreateAgentRunActivity,
    ) -> None:
        """Test creating an agent run activity."""
        activity = client.agent_runs.activities.create(
            workspace_slug, agent_run.id, activity_data
        )
        assert activity is not None
        assert activity.id is not None
        assert activity.agent_run == agent_run.id
        assert activity.type is not None
        assert activity.content is not None

    def test_retrieve_activity(
        self,
        client: PlaneClient,
        workspace_slug: str,
        agent_run: AgentRun,
        activity: AgentRunActivity,
    ) -> None:
        """Test retrieving a specific agent run activity."""
        retrieved = client.agent_runs.activities.retrieve(
            workspace_slug, agent_run.id, activity.id
        )
        assert retrieved is not None
        assert retrieved.id == activity.id
        assert retrieved.agent_run == agent_run.id
        assert retrieved.type == activity.type

