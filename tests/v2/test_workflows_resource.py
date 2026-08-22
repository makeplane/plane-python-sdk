"""Offline coverage for `Workflows`: project-scoped CRUD plus the workflow-id-nested
`states`/`transitions` sub-resources."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.workflows import Workflows
from plane.config import Configuration
from plane.models.v2.workflows import (
    CreateWorkflow,
    CreateWorkflowTransition,
    UpdateWorkflow,
    UpdateWorkflowState,
    UpdateWorkflowTransition,
    WorkflowStateCreate,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/workflows"


@pytest.fixture
def workflows(config: Configuration) -> Workflows:
    return Workflows(V2Transport(config), slug="acme", project_id="ENG")


@responses.activate
def test_list_workflows(workflows: Workflows) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "wf1", "name": "Default", "is_active": True}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = workflows.list()

    assert page.total_count == 1
    assert page.data[0].name == "Default"


@responses.activate
def test_create_then_patch_then_delete_workflow(workflows: Workflows) -> None:
    responses.post(f"{BASE}/", json={"id": "wf1", "name": "Default"}, status=201)
    responses.patch(f"{BASE}/wf1/", json={"id": "wf1", "name": "Renamed"})
    responses.delete(f"{BASE}/wf1/", status=204)

    created = workflows.create(CreateWorkflow(name="Default"))
    updated = workflows.update(created.id, UpdateWorkflow(name="Renamed"))

    assert updated.name == "Renamed"
    assert workflows.delete("wf1") is None


@responses.activate
def test_retrieve_workflow(workflows: Workflows) -> None:
    responses.get(f"{BASE}/wf1/", json={"id": "wf1", "name": "Default"})

    row = workflows.retrieve("wf1")

    assert row.id == "wf1"


def test_list_rejects_unknown_fields_before_the_request(workflows: Workflows) -> None:
    with pytest.raises(ValueError, match="bogus"):
        workflows.list(fields=["bogus"])


# -- Nested: states (bulk-attach `attach`) ----------------------------------------


@responses.activate
def test_states_bulk_attach(workflows: Workflows) -> None:
    responses.post(
        f"{BASE}/wf1/states/",
        json={"id": "ws1", "workflow_id": "wf1", "state_id": "st1"},
        status=201,
    )

    created = workflows.states.attach("wf1", WorkflowStateCreate(state_ids=["st1", "st2"]))

    assert created.id == "ws1"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"state_ids": ["st1", "st2"]}


@responses.activate
def test_states_list_and_update_membership_row(workflows: Workflows) -> None:
    responses.get(
        f"{BASE}/wf1/states/",
        json={
            "data": [{"id": "ws1", "workflow_id": "wf1", "state_id": "st1", "type": "default"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.patch(
        f"{BASE}/wf1/states/ws1/",
        json={"id": "ws1", "is_default": True},
    )

    page = workflows.states.list("wf1")
    assert page.data[0].state_id == "st1"

    updated = workflows.states.update("wf1", "ws1", UpdateWorkflowState(is_default=True))
    assert updated.is_default is True


@responses.activate
def test_states_delete_detaches(workflows: Workflows) -> None:
    responses.delete(f"{BASE}/wf1/states/ws1/", status=204)

    assert workflows.states.delete("wf1", "ws1") is None


# -- Nested: transitions ---------------------------------------------------------


@responses.activate
def test_transitions_crud(workflows: Workflows) -> None:
    responses.get(
        f"{BASE}/wf1/state-transitions/",
        json={
            "data": [{"id": "wt1", "workflow_state_id": "ws1"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{BASE}/wf1/state-transitions/",
        json={"id": "wt1", "workflow_state_id": "ws1", "transition_state_id": "ws2"},
        status=201,
    )
    responses.patch(
        f"{BASE}/wf1/state-transitions/wt1/",
        json={"id": "wt1", "required_approvals": 2},
    )
    responses.delete(f"{BASE}/wf1/state-transitions/wt1/", status=204)

    page = workflows.transitions.list("wf1")
    assert page.data[0].workflow_state_id == "ws1"

    created = workflows.transitions.create(
        "wf1",
        CreateWorkflowTransition(state_id="ws1", transition_state_id="ws2"),
    )
    assert created.transition_state_id == "ws2"

    updated = workflows.transitions.update(
        "wf1", "wt1", UpdateWorkflowTransition(required_approvals=2)
    )
    assert updated.required_approvals == 2

    assert workflows.transitions.delete("wf1", "wt1") is None
