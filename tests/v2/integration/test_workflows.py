"""Live coverage for `client.v2.workspace(...).project(...).workflows`;
skips (never fails) when required env vars are absent, same convention
as every other file in this directory."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.workflows import (
    CreateWorkflow,
    CreateWorkflowTransition,
    UpdateWorkflow,
    UpdateWorkflowState,
    UpdateWorkflowTransition,
    WorkflowStateCreate,
)

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Any:
    return client.v2.workspace(workspace_slug).project(project_id)


class TestWorkflows:
    def test_crud_and_nested_states_and_transitions(self, proj: Any) -> None:
        """One end-to-end pass: create a workflow, attach a state, add a
        transition, then tear everything down; a fresh project always has
        >=2 default states."""
        states_page = proj.states.list()
        assert len(states_page.data) >= 2, "fixture project needs >=2 default states"
        source_state, target_state = states_page.data[0], states_page.data[1]

        # Workflows are gated by `FeatureFlag.WORKFLOWS` (402, no toggle
        # reachable through this API) -- skip rather than fail when it's off.
        try:
            created = proj.workflows.create(CreateWorkflow(name=unique_name("workflow")))
        except PlaneAPIError as exc:
            if exc.status == 402:
                pytest.skip("Workflows feature is not enabled for this project")
            raise
        try:
            fetched = proj.workflows.retrieve(created.id)
            assert fetched.id == created.id

            page = proj.workflows.list()
            assert any(w.id == created.id for w in page.data)

            updated = proj.workflows.update(created.id, UpdateWorkflow(is_active=True))
            assert updated.is_active is True

            # -- Nested: states --
            attached = proj.workflows.states.attach(
                created.id,
                WorkflowStateCreate(state_ids=[source_state.id, target_state.id]),
            )
            assert attached.workflow_id == created.id

            states = proj.workflows.states.list(created.id)
            attached_state_ids = {row.state_id for row in states.data}
            assert {source_state.id, target_state.id} <= attached_state_ids
            source_row = next(r for r in states.data if r.state_id == source_state.id)
            target_row = next(r for r in states.data if r.state_id == target_state.id)

            patched_state = proj.workflows.states.update(
                created.id,
                source_row.id,
                UpdateWorkflowState(allow_issue_creation=True),
            )
            assert patched_state.allow_issue_creation is True

            # -- Nested: transitions --
            transition = proj.workflows.transitions.create(
                created.id,
                CreateWorkflowTransition(
                    state_id=source_state.id, transition_state_id=target_state.id
                ),
            )
            try:
                fetched_transition = proj.workflows.transitions.retrieve(created.id, transition.id)
                assert fetched_transition.transition_state_id == target_state.id

                patched_transition = proj.workflows.transitions.update(
                    created.id, transition.id, UpdateWorkflowTransition(required_approvals=1)
                )
                assert patched_transition.required_approvals == 1
            finally:
                proj.workflows.transitions.delete(created.id, transition.id)

            proj.workflows.states.delete(created.id, target_row.id)
        finally:
            proj.workflows.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            proj.workflows.retrieve(created.id)
        assert exc_info.value.status == 404
