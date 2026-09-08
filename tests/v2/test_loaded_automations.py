"""Navigable rows for both automations families: `LoadedProjectAutomation` (children
`edges`, `nodes`, `activities`, bound with `slug, project, automation`) and
`LoadedWorkspaceAutomation` (the same three children, bound with `slug, automation`).

Neither `ProjectAutomations` nor `WorkspaceAutomations` is wired onto the tree yet
(that is task 6), so both are constructed directly through `V2Transport`, the same
way every other offline resource test in this package is."""

from __future__ import annotations

import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.automations import ProjectAutomations, WorkspaceAutomations
from plane.config import Configuration


@responses.activate
def test_fetched_project_automation_reaches_its_nodes(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/automations/a1/", json={"id": "a1", "name": "On close"})
    responses.get(
        f"{base}/automations/a1/nodes/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    automation = ProjectAutomations(V2Transport(config)).retrieve("acme", "ENG", "a1")
    automation.nodes.list()

    assert responses.calls[1].request.url == f"{base}/automations/a1/nodes/"


@responses.activate
def test_fetched_project_automation_reaches_its_edges(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/automations/a1/", json={"id": "a1"})
    responses.get(
        f"{base}/automations/a1/edges/", json={"data": [], "pagination": {"style": "offset"}}
    )

    automation = ProjectAutomations(V2Transport(config)).retrieve("acme", "ENG", "a1")
    automation.edges.list()

    assert responses.calls[1].request.url == f"{base}/automations/a1/edges/"


@responses.activate
def test_fetched_project_automation_reaches_its_activities(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/automations/a1/", json={"id": "a1"})
    responses.get(
        f"{base}/automations/a1/activities/", json={"data": [], "pagination": {"style": "offset"}}
    )

    automation = ProjectAutomations(V2Transport(config)).retrieve("acme", "ENG", "a1")
    automation.activities.list()

    assert responses.calls[1].request.url == f"{base}/automations/a1/activities/"


@responses.activate
def test_project_automation_from_a_list_page_also_reaches_its_children(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(
        f"{base}/automations/",
        json={
            "data": [{"id": "a1", "name": "On close"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )
    responses.get(
        f"{base}/automations/a1/nodes/", json={"data": [], "pagination": {"style": "offset"}}
    )

    page = ProjectAutomations(V2Transport(config)).list("acme", "ENG")
    page.data[0].nodes.list()

    assert responses.calls[1].request.url == f"{base}/automations/a1/nodes/"


@responses.activate
def test_fetched_workspace_automation_reaches_its_nodes(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/automations/a2/", json={"id": "a2", "name": "Global"})
    responses.get(
        f"{base}/automations/a2/nodes/", json={"data": [], "pagination": {"style": "offset"}}
    )

    automation = WorkspaceAutomations(V2Transport(config)).retrieve("acme", "a2")
    automation.nodes.list()

    assert responses.calls[1].request.url == f"{base}/automations/a2/nodes/"


@responses.activate
def test_fetched_workspace_automation_reaches_its_edges(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/automations/a2/", json={"id": "a2"})
    responses.get(
        f"{base}/automations/a2/edges/", json={"data": [], "pagination": {"style": "offset"}}
    )

    automation = WorkspaceAutomations(V2Transport(config)).retrieve("acme", "a2")
    automation.edges.list()

    assert responses.calls[1].request.url == f"{base}/automations/a2/edges/"


@responses.activate
def test_fetched_workspace_automation_reaches_its_activities(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/automations/a2/", json={"id": "a2"})
    responses.get(
        f"{base}/automations/a2/activities/", json={"data": [], "pagination": {"style": "offset"}}
    )

    automation = WorkspaceAutomations(V2Transport(config)).retrieve("acme", "a2")
    automation.activities.list()

    assert responses.calls[1].request.url == f"{base}/automations/a2/activities/"


@responses.activate
def test_workspace_automation_from_a_list_page_also_reaches_its_children(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(
        f"{base}/automations/",
        json={"data": [{"id": "a2", "name": "Global"}], "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{base}/automations/a2/edges/", json={"data": [], "pagination": {"style": "offset"}}
    )

    page = WorkspaceAutomations(V2Transport(config)).list("acme")
    page.data[0].edges.list()

    assert responses.calls[1].request.url == f"{base}/automations/a2/edges/"
