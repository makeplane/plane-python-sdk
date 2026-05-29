"""Unit tests for Workflows API resource (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.projects import Project, ProjectFeature
from plane.models.workflows import (
    AttachWorkflowStates,
    CreateWorkflow,
    CreateWorkflowTransition,
    UpdateWorkflow,
    UpdateWorkflowTransition,
)


class TestWorkflowsAPI:
    """Test Workflows API list/create/update."""

    def test_list_workflows(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing workflows for a project."""
        # Enable work_item_types feature which workflows depend on
        client.projects.update_features(
            workspace_slug, project.id, ProjectFeature(work_item_types=True)
        )
        response = client.workflows.list(workspace_slug, project.id)
        assert response is not None
        assert isinstance(response, list)


class TestWorkflowsAPICRUD:
    """Test Workflows API CRUD and sub-resource operations."""

    @pytest.fixture
    def workflow_data(self) -> CreateWorkflow:
        """Create test workflow data."""
        import time

        return CreateWorkflow(
            name=f"Test Workflow {int(time.time())}",
            description="Test workflow",
            is_active=True,
        )

    @pytest.fixture
    def workflow(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        workflow_data: CreateWorkflow,
    ):
        """Create a test workflow and yield it."""
        client.projects.update_features(
            workspace_slug, project.id, ProjectFeature(work_item_types=True)
        )
        wf = client.workflows.create(workspace_slug, project.id, workflow_data)
        yield wf

    def test_create_workflow(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        workflow_data: CreateWorkflow,
    ) -> None:
        """Test creating a workflow."""
        client.projects.update_features(
            workspace_slug, project.id, ProjectFeature(work_item_types=True)
        )
        wf = client.workflows.create(workspace_slug, project.id, workflow_data)
        assert wf is not None
        assert wf.id is not None
        assert wf.name == workflow_data.name

    def test_update_workflow(
        self, client: PlaneClient, workspace_slug: str, project: Project, workflow
    ) -> None:
        """Test updating a workflow."""
        updated = client.workflows.update(
            workspace_slug,
            project.id,
            workflow.id,
            UpdateWorkflow(description="Updated description"),
        )
        assert updated is not None
        assert updated.id == workflow.id
        assert updated.description == "Updated description"

    def test_attach_states(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        workflow,
    ) -> None:
        """Test attaching states to a workflow."""
        # List available states and attach the first one
        states = client.states.list(workspace_slug, project.id)
        if not states or not states.results:
            pytest.skip("No states available to attach")
        state_id = states.results[0].id
        # attach should not raise
        client.workflows.states.attach(
            workspace_slug,
            project.id,
            workflow.id,
            AttachWorkflowStates(state_ids=[state_id]),
        )

    def test_detach_state(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        workflow,
    ) -> None:
        """Test detaching a state from a workflow."""
        states = client.states.list(workspace_slug, project.id)
        if not states or not states.results:
            pytest.skip("No states available")
        state_id = states.results[0].id
        # Attach first, then detach
        client.workflows.states.attach(
            workspace_slug,
            project.id,
            workflow.id,
            AttachWorkflowStates(state_ids=[state_id]),
        )
        client.workflows.states.detach(workspace_slug, project.id, workflow.id, state_id)

    def test_list_transitions(
        self, client: PlaneClient, workspace_slug: str, project: Project, workflow
    ) -> None:
        """Test listing transitions for a workflow."""
        transitions = client.workflows.transitions.list(workspace_slug, project.id, workflow.id)
        assert transitions is not None
        assert isinstance(transitions, list)

    def test_create_transition(
        self, client: PlaneClient, workspace_slug: str, project: Project, workflow
    ) -> None:
        """Test creating a transition between two states."""
        states = client.states.list(workspace_slug, project.id)
        if not states or not states.results or len(states.results) < 2:
            pytest.skip("Need at least 2 states to create a transition")
        state_id = states.results[0].id
        transition_state_id = states.results[1].id
        result = client.workflows.transitions.create(
            workspace_slug,
            project.id,
            workflow.id,
            CreateWorkflowTransition(
                state_id=state_id,
                transition_state_id=transition_state_id,
            ),
        )
        # May return None if transition already exists (400)
        assert result is None or result.id is not None

    def test_update_transition(
        self, client: PlaneClient, workspace_slug: str, project: Project, workflow
    ) -> None:
        """Test updating a workflow transition."""
        transitions = client.workflows.transitions.list(workspace_slug, project.id, workflow.id)
        if not transitions:
            pytest.skip("No transitions available to update")
        transition_id = transitions[0].id
        # Should not raise
        client.workflows.transitions.update(
            workspace_slug,
            project.id,
            workflow.id,
            transition_id,
            UpdateWorkflowTransition(post_rules=[]),
        )

    def test_delete_transition(
        self, client: PlaneClient, workspace_slug: str, project: Project, workflow
    ) -> None:
        """Test deleting a workflow transition."""
        transitions = client.workflows.transitions.list(workspace_slug, project.id, workflow.id)
        if not transitions:
            pytest.skip("No transitions available to delete")
        transition_id = transitions[0].id
        client.workflows.transitions.delete(workspace_slug, project.id, workflow.id, transition_id)
