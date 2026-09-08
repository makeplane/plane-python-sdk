"""Live coverage for `client.v2.workspaces.projects.workflows`, driven entirely
through loaded rows: workflows off the loaded `project`, and each workflow's own
states and transitions off the loaded *workflow* returned by `create`.

`project.workflows.states` is not a route (`tests/v2/test_owned_sub_resources.py`) --
a workflow's states hang off a workflow, and `created` already is one, so no id is
repeated anywhere below.

The `WORKFLOWS` feature flag is a 402 with no toggle reachable through this API, so
it is a declared server-capability skip; every other skip in this suite is a
failure."""

from __future__ import annotations

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.models.v2.workflows import (
    CreateWorkflow,
    CreateWorkflowTransition,
    UpdateWorkflow,
    UpdateWorkflowState,
    UpdateWorkflowTransition,
)

from ._guard import skip_absent_capability
from .helpers import unique_name


class TestWorkflows:
    def test_crud_and_nested_states_and_transitions(self, project: LoadedProject) -> None:
        """One end-to-end pass: create a workflow, attach a state, add a
        transition, then tear everything down; a fresh project always has
        >=2 default states."""
        states_page = project.states.list()
        assert len(states_page.data) >= 2, "fixture project needs >=2 default states"
        source_state, target_state = states_page.data[0], states_page.data[1]

        # Workflows are gated by `FeatureFlag.WORKFLOWS` (402, no toggle
        # reachable through this API) -- skip rather than fail when it's off.
        try:
            created = project.workflows.create(CreateWorkflow(name=unique_name("workflow")))
        except PlaneAPIError as exc:
            if exc.status == 402:
                skip_absent_capability("WORKFLOWS is not enabled for this project")
            raise
        try:
            fetched = project.workflows.retrieve(created.id)
            assert fetched.id == created.id

            page = project.workflows.list()
            assert any(w.id == created.id for w in page.data)

            updated = project.workflows.update(created.id, UpdateWorkflow(is_active=True))
            assert updated.is_active is True

            # -- Nested: states --
            # `attach` takes the ids and builds the request DTO itself (it is a
            # bridge, per CLAUDE.md), and answers the attached rows as a bare array
            # rather than one row -- so there is no `workflow_id` on the result to
            # assert; the rows themselves are the evidence.
            attached = created.states.attach([source_state.id, target_state.id])
            assert {row.state_id for row in attached} == {source_state.id, target_state.id}

            states = created.states.list()
            attached_state_ids = {row.state_id for row in states.data}
            assert {source_state.id, target_state.id} <= attached_state_ids
            source_row = next(r for r in states.data if r.state_id == source_state.id)
            target_row = next(r for r in states.data if r.state_id == target_state.id)

            patched_state = created.states.update(
                source_row.id, UpdateWorkflowState(allow_issue_creation=True)
            )
            assert patched_state.allow_issue_creation is True

            # -- Nested: transitions --
            transition = created.transitions.create(
                CreateWorkflowTransition(
                    state_id=source_state.id, transition_state_id=target_state.id
                )
            )
            try:
                fetched_transition = created.transitions.retrieve(transition.id)
                assert fetched_transition.transition_state_id == target_state.id

                patched_transition = created.transitions.update(
                    transition.id, UpdateWorkflowTransition(required_approvals=1)
                )
                assert patched_transition.required_approvals == 1
            finally:
                created.transitions.delete(transition.id)

            created.states.delete(target_row.id)
        finally:
            project.workflows.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            project.workflows.retrieve(created.id)
        assert exc_info.value.status == 404
