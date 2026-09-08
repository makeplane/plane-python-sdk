"""Navigable rows for `Workflows`: `LoadedWorkflow`, whose `states`/`transitions`
children are bound with `slug, project, workflow`.

`Workflows` is not wired onto the tree yet (that is task 6), so it is constructed
directly through `V2Transport`, the same way every other offline resource test in
this package is. `tests/v2/test_workflows_resource.py` covers
`test_fetched_workflow_reaches_its_states`/`_transitions` already; this file adds
the remaining row-returning methods (`list`, `create`, `update`)."""

from __future__ import annotations

import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.workflows import Workflows
from plane.config import Configuration
from plane.models.v2.workflows import CreateWorkflow, UpdateWorkflow


@responses.activate
def test_workflow_from_a_list_page_also_reaches_its_states(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(
        f"{base}/workflows/",
        json={
            "data": [{"id": "w1", "name": "Default"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )
    responses.get(
        f"{base}/workflows/w1/states/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    page = Workflows(V2Transport(config)).list("acme", "ENG")
    page.data[0].states.list()

    assert responses.calls[1].request.url == f"{base}/workflows/w1/states/"


@responses.activate
def test_created_workflow_reaches_its_transitions(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.post(f"{base}/workflows/", json={"id": "w1", "name": "Default"}, status=201)
    responses.get(
        f"{base}/workflows/w1/state-transitions/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    workflow = Workflows(V2Transport(config)).create("acme", "ENG", CreateWorkflow(name="Default"))
    workflow.transitions.list()

    assert responses.calls[1].request.url == f"{base}/workflows/w1/state-transitions/"


@responses.activate
def test_updated_workflow_reaches_its_states(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.patch(f"{base}/workflows/w1/", json={"id": "w1", "name": "Renamed"})
    responses.get(
        f"{base}/workflows/w1/states/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    workflow = Workflows(V2Transport(config)).update(
        "acme", "ENG", "w1", UpdateWorkflow(name="Renamed")
    )
    workflow.states.list()

    assert responses.calls[1].request.url == f"{base}/workflows/w1/states/"
