"""Offline coverage for `Workflows` and its workflow-id-nested `states`/
`transitions` children: CRUD, pagination, and every method's exact request URL.
Neither `Workflows` nor its children are wired onto the tree yet (that is task
6), so all three are constructed directly through `V2Transport`, the same way
every other offline resource test in this package is.

`test_the_opt_out_list_is_empty` closes out `tests/v2/tree_walk.py`'s
`UNMIGRATED_RESOURCES`: workflows were the last family on it."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.workflows import Workflows, WorkflowStates, WorkflowTransitions
from plane.config import Configuration
from plane.models.v2.workflows import (
    CreateWorkflow,
    CreateWorkflowTransition,
    UpdateWorkflow,
    UpdateWorkflowState,
    UpdateWorkflowTransition,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/workflows"


@pytest.fixture
def workflows(config: Configuration) -> Workflows:
    return Workflows(V2Transport(config))


@pytest.fixture
def states(config: Configuration) -> WorkflowStates:
    return WorkflowStates(V2Transport(config))


@pytest.fixture
def transitions(config: Configuration) -> WorkflowTransitions:
    return WorkflowTransitions(V2Transport(config))


def test_workflows_attaches_its_children(workflows: Workflows) -> None:
    assert isinstance(workflows.states, WorkflowStates)
    assert isinstance(workflows.transitions, WorkflowTransitions)


# -- Workflows CRUD ----------------------------------------------------------------


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

    page = workflows.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].name == "Default"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_list_passes_filters_and_pagination(workflows: Workflows) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    workflows.list("acme", "ENG", search="triage", per_page=25, offset=50)

    query = responses.calls[0].request.url
    assert "search=triage" in query
    assert "per_page=25" in query
    assert "offset=50" in query


@responses.activate
def test_iterate_yields_every_workflow(workflows: Workflows) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "wf1", "name": "Default"}],
            "pagination": {"style": "offset"},
        },
    )

    rows = list(workflows.iterate("acme", "ENG"))

    assert rows[0].id == "wf1"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_retrieve_workflow(workflows: Workflows) -> None:
    responses.get(f"{BASE}/wf1/", json={"id": "wf1", "name": "Default"})

    row = workflows.retrieve("acme", "ENG", "wf1")

    assert row.id == "wf1"
    assert responses.calls[0].request.url == f"{BASE}/wf1/"


@responses.activate
def test_find_by_name(workflows: Workflows) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "wf1", "name": "Default"}],
            "pagination": {"style": "offset"},
        },
    )

    row = workflows.find_by_name("acme", "ENG", "Default")

    assert row.id == "wf1"
    query = responses.calls[0].request.url
    assert "name=Default" in query
    assert "per_page=2" in query


@responses.activate
def test_create_then_patch_then_delete_workflow(workflows: Workflows) -> None:
    responses.post(f"{BASE}/", json={"id": "wf1", "name": "Default"}, status=201)
    responses.patch(f"{BASE}/wf1/", json={"id": "wf1", "name": "Renamed"})
    responses.delete(f"{BASE}/wf1/", status=204)

    created = workflows.create("acme", "ENG", CreateWorkflow(name="Default"))
    assert responses.calls[0].request.url == f"{BASE}/"

    updated = workflows.update("acme", "ENG", created.id, UpdateWorkflow(name="Renamed"))
    assert updated.name == "Renamed"
    assert responses.calls[1].request.url == f"{BASE}/wf1/"

    assert workflows.delete("acme", "ENG", "wf1") is None
    assert responses.calls[2].request.url == f"{BASE}/wf1/"


def test_list_rejects_unknown_fields_before_the_request(workflows: Workflows) -> None:
    with pytest.raises(ValueError, match="bogus"):
        workflows.list("acme", "ENG", fields=["bogus"])


# -- Nested: states (bulk-`attach`, not `create`) -----------------------------------


@responses.activate
def test_states_list(states: WorkflowStates) -> None:
    responses.get(
        f"{BASE}/wf1/states/",
        json={
            "data": [{"id": "ws1", "workflow_id": "wf1", "state_id": "st1", "type": "default"}],
            "pagination": {"style": "offset"},
        },
    )

    page = states.list("acme", "ENG", "wf1")

    assert page.data[0].state_id == "st1"
    assert responses.calls[0].request.url == f"{BASE}/wf1/states/"


@responses.activate
def test_states_iterate(states: WorkflowStates) -> None:
    responses.get(
        f"{BASE}/wf1/states/",
        json={"data": [{"id": "ws1"}], "pagination": {"style": "offset"}},
    )

    rows = list(states.iterate("acme", "ENG", "wf1"))

    assert rows[0].id == "ws1"
    assert responses.calls[0].request.url == f"{BASE}/wf1/states/"


@responses.activate
def test_states_retrieve(states: WorkflowStates) -> None:
    responses.get(f"{BASE}/wf1/states/ws1/", json={"id": "ws1", "state_id": "st1"})

    row = states.retrieve("acme", "ENG", "wf1", "ws1")

    assert row.id == "ws1"
    assert responses.calls[0].request.url == f"{BASE}/wf1/states/ws1/"


@responses.activate
def test_states_attach_posts_ids_to_the_collection_url_and_answers_an_array(
    states: WorkflowStates,
) -> None:
    """The genuine spec defect this task preserves: the golden's `$ref` for
    `workflow_states_create` claims a single `WorkflowStateWriteRequest` row, but
    the API actually POSTs `{state_ids}` to the collection URL and answers an
    array of the resulting membership rows. `attach` is not `create` and does not
    go through `_create`."""
    responses.post(
        f"{BASE}/wf1/states/",
        json=[
            {"id": "ws1", "workflow_id": "wf1", "state_id": "st1"},
            {"id": "ws2", "workflow_id": "wf1", "state_id": "st2"},
        ],
        status=201,
    )

    created = states.attach("acme", "ENG", "wf1", ["st1", "st2"])

    assert [row.id for row in created] == ["ws1", "ws2"]
    assert responses.calls[0].request.url == f"{BASE}/wf1/states/"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"state_ids": ["st1", "st2"]}


@responses.activate
def test_states_attach_tolerates_a_lone_object_as_a_one_row_array(
    states: WorkflowStates,
) -> None:
    responses.post(f"{BASE}/wf1/states/", json={"id": "ws1", "state_id": "st1"}, status=201)

    created = states.attach("acme", "ENG", "wf1", ["st1"])

    assert [row.id for row in created] == ["ws1"]


@responses.activate
def test_states_update_changes_the_membership_row(states: WorkflowStates) -> None:
    responses.patch(f"{BASE}/wf1/states/ws1/", json={"id": "ws1", "is_default": True})

    updated = states.update("acme", "ENG", "wf1", "ws1", UpdateWorkflowState(is_default=True))

    assert updated.is_default is True
    assert responses.calls[0].request.url == f"{BASE}/wf1/states/ws1/"


@responses.activate
def test_states_delete_detaches(states: WorkflowStates) -> None:
    responses.delete(f"{BASE}/wf1/states/ws1/", status=204)

    assert states.delete("acme", "ENG", "wf1", "ws1") is None
    assert responses.calls[0].request.url == f"{BASE}/wf1/states/ws1/"


# -- Nested: transitions -------------------------------------------------------------


@responses.activate
def test_transitions_list(transitions: WorkflowTransitions) -> None:
    responses.get(
        f"{BASE}/wf1/state-transitions/",
        json={
            "data": [{"id": "wt1", "workflow_state_id": "ws1"}],
            "pagination": {"style": "offset"},
        },
    )

    page = transitions.list("acme", "ENG", "wf1")

    assert page.data[0].workflow_state_id == "ws1"
    assert responses.calls[0].request.url == f"{BASE}/wf1/state-transitions/"


@responses.activate
def test_transitions_iterate(transitions: WorkflowTransitions) -> None:
    responses.get(
        f"{BASE}/wf1/state-transitions/",
        json={"data": [{"id": "wt1"}], "pagination": {"style": "offset"}},
    )

    rows = list(transitions.iterate("acme", "ENG", "wf1"))

    assert rows[0].id == "wt1"
    assert responses.calls[0].request.url == f"{BASE}/wf1/state-transitions/"


@responses.activate
def test_transitions_retrieve(transitions: WorkflowTransitions) -> None:
    responses.get(f"{BASE}/wf1/state-transitions/wt1/", json={"id": "wt1"})

    row = transitions.retrieve("acme", "ENG", "wf1", "wt1")

    assert row.id == "wt1"
    assert responses.calls[0].request.url == f"{BASE}/wf1/state-transitions/wt1/"


@responses.activate
def test_transitions_create(transitions: WorkflowTransitions) -> None:
    responses.post(
        f"{BASE}/wf1/state-transitions/",
        json={"id": "wt1", "workflow_state_id": "ws1", "transition_state_id": "ws2"},
        status=201,
    )

    created = transitions.create(
        "acme", "ENG", "wf1", CreateWorkflowTransition(state_id="ws1", transition_state_id="ws2")
    )

    assert created.transition_state_id == "ws2"
    assert responses.calls[0].request.url == f"{BASE}/wf1/state-transitions/"


@responses.activate
def test_transitions_update(transitions: WorkflowTransitions) -> None:
    responses.patch(
        f"{BASE}/wf1/state-transitions/wt1/", json={"id": "wt1", "required_approvals": 2}
    )

    updated = transitions.update(
        "acme", "ENG", "wf1", "wt1", UpdateWorkflowTransition(required_approvals=2)
    )

    assert updated.required_approvals == 2
    assert responses.calls[0].request.url == f"{BASE}/wf1/state-transitions/wt1/"


@responses.activate
def test_transitions_delete(transitions: WorkflowTransitions) -> None:
    responses.delete(f"{BASE}/wf1/state-transitions/wt1/", status=204)

    assert transitions.delete("acme", "ENG", "wf1", "wt1") is None
    assert responses.calls[0].request.url == f"{BASE}/wf1/state-transitions/wt1/"


# -- Navigation: a fetched workflow reaches its states/transitions ------------------


@responses.activate
def test_fetched_workflow_reaches_its_states(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/workflows/w1/", json={"id": "w1"})
    responses.get(
        f"{base}/workflows/w1/states/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    workflow = Workflows(V2Transport(config)).retrieve("acme", "ENG", "w1")
    workflow.states.list()

    assert responses.calls[1].request.url == f"{base}/workflows/w1/states/"


@responses.activate
def test_fetched_workflow_reaches_its_transitions(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/workflows/w1/", json={"id": "w1"})
    responses.get(
        f"{base}/workflows/w1/state-transitions/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    workflow = Workflows(V2Transport(config)).retrieve("acme", "ENG", "w1")
    workflow.transitions.list()

    assert responses.calls[1].request.url == f"{base}/workflows/w1/state-transitions/"


def test_the_opt_out_list_is_empty() -> None:
    from tests.v2.tree_walk import UNMIGRATED_RESOURCES

    assert UNMIGRATED_RESOURCES == frozenset(), (
        f"{len(UNMIGRATED_RESOURCES)} classes remain unmigrated: " f"{sorted(UNMIGRATED_RESOURCES)}"
    )
