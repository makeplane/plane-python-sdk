"""Unit tests for WorkspaceWorkflows API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.models.states import CreateWorkspaceState
from plane.models.workspace_workflows import (
    AddWorkspaceWorkflowStates,
    CreateWorkspaceWorkflow,
    UpdateWorkspaceWorkflow,
    WorkspaceWorkflow,
    WorkspaceWorkflowState,
)


@pytest.fixture(scope="module")
def governed(client: PlaneClient, workspace_slug: str) -> bool:
    """Whether the test workspace owns states and workflows (workspace governance)."""
    features = client.workspaces.get_features(workspace_slug)
    return bool(features.states_owned_by_workspace)


class TestWorkspaceWorkflows:
    """Test WorkspaceWorkflows API resource."""

    def test_list_workspace_workflows(self, client: PlaneClient, workspace_slug: str) -> None:
        """The list endpoint is dual-mode and must work in every workspace."""
        response = client.workspace_workflows.list(workspace_slug)
        assert isinstance(response.results, list)
        for workflow in response.results:
            assert workflow.id is not None
            assert workflow.name

    def test_workflow_lifecycle_with_chain(
        self, client: PlaneClient, workspace_slug: str, governed: bool
    ) -> None:
        """Create a workflow, configure a two-state chain, and clean up (governed only)."""
        if not governed:
            pytest.skip("workspace does not own states and workflows")

        suffix = uuid4().hex[:8]
        state_a = None
        state_b = None
        workflow = None
        try:
            state_a = client.workspace_states.create(
                workspace_slug,
                CreateWorkspaceState(
                    name=f"test-wf-a-{suffix}", color="#FF0000", group="unstarted"
                ),
            )
            state_b = client.workspace_states.create(
                workspace_slug,
                CreateWorkspaceState(name=f"test-wf-b-{suffix}", color="#00FF00", group="started"),
            )
            workflow = client.workspace_workflows.create(
                workspace_slug, CreateWorkspaceWorkflow(name=f"test-workflow-{suffix}")
            )
            assert workflow.id is not None

            chain = client.workspace_workflows.states.add(
                workspace_slug,
                workflow.id,
                AddWorkspaceWorkflowStates(state_ids=[state_a.id, state_b.id]),
            )
            assert isinstance(chain, list)

            client.workspace_workflows.states.mark_default(workspace_slug, workflow.id, state_a.id)

            detail = client.workspace_workflows.retrieve(workspace_slug, workflow.id)
            assert detail.id == workflow.id
            assert detail.states is not None and len(detail.states) >= 2

            updated = client.workspace_workflows.update(
                workspace_slug,
                workflow.id,
                UpdateWorkspaceWorkflow(description="SDK test workflow"),
            )
            assert updated.id == workflow.id

            usage = client.workspace_workflows.usage(workspace_slug, workflow.id)
            assert isinstance(usage.projects, list)

            transitions = client.workspace_workflows.transitions.list(workspace_slug, workflow.id)
            assert isinstance(transitions, list)
        finally:
            teardown = []
            if workflow is not None and workflow.id:
                teardown.append((client.workspace_workflows.delete, (workspace_slug, workflow.id)))
            for state in (state_a, state_b):
                if state is not None and state.id:
                    teardown.append((client.workspace_states.delete, (workspace_slug, state.id)))
            for func, args in teardown:
                try:
                    func(*args)
                except Exception as exc:
                    warnings.warn(f"Teardown failed: {exc}", stacklevel=1)


class TestWorkspaceWorkflowStateModel:
    """Test Pydantic model validation for workspace workflow chain rows."""

    def test_state_id_filled_from_id(self) -> None:
        """Chain rows are keyed by state ID, and the API omits ``state_id``."""
        row = WorkspaceWorkflowState.model_validate(
            {
                "id": "8f1c2d3e",
                "type": "DEFAULT",
                "allow_issue_creation": True,
                "is_default": False,
                "sequence": 65535.0,
                "transitions": [],
            }
        )
        assert row.state_id == "8f1c2d3e"
        assert row.model_dump()["state_id"] == "8f1c2d3e"

    def test_state_id_filled_on_nested_chain(self) -> None:
        """The detail payload's nested ``states`` rows get the same treatment."""
        workflow = WorkspaceWorkflow.model_validate(
            {"id": "wf-1", "name": "Default", "states": [{"id": "state-1"}, {"id": "state-2"}]}
        )
        assert workflow.states is not None
        assert [state.state_id for state in workflow.states] == ["state-1", "state-2"]

    def test_explicit_state_id_wins(self) -> None:
        """A payload that does carry ``state_id`` keeps its own value."""
        row = WorkspaceWorkflowState.model_validate({"id": "membership-1", "state_id": "state-1"})
        assert row.state_id == "state-1"

    def test_missing_id_leaves_state_id_unset(self) -> None:
        """Nothing to fill from, and nothing to raise about."""
        assert WorkspaceWorkflowState.model_validate({}).state_id is None
