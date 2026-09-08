"""Navigable rows for both work item property families: `LoadedWorkItemProperty`
(child `property_options`, bound with `slug, project, property`) and
`LoadedWorkspaceWorkItemProperty` (children `property_options` and `contexts`,
bound with `slug, property`).

`property_options`, not `options`: `WorkItemProperty.options` is itself a real API
field (the inlined choices for OPTION-type properties), so the navigation
property is aliased -- see `NAVIGATION_ALIASES` in `tests/v2/test_loaded_navigation.py`.

Neither `WorkItemProperties` nor `WorkspaceWorkItemProperties` is wired onto the
tree yet (that is task 6), so both are constructed directly through
`V2Transport`, the same way every other offline resource test in this package is."""

from __future__ import annotations

import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_item_properties import WorkItemProperties, WorkspaceWorkItemProperties
from plane.config import Configuration


@responses.activate
def test_fetched_property_reaches_its_options(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/work-item-properties/p1/", json={"id": "p1", "name": "severity"})
    responses.get(
        f"{base}/work-item-properties/p1/options/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    property_row = WorkItemProperties(V2Transport(config)).retrieve("acme", "ENG", "p1")
    property_row.property_options.list()

    assert responses.calls[1].request.url == f"{base}/work-item-properties/p1/options/"


@responses.activate
def test_property_from_a_list_page_also_reaches_its_options(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(
        f"{base}/work-item-properties/",
        json={
            "data": [{"id": "p1", "name": "severity"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )
    responses.get(
        f"{base}/work-item-properties/p1/options/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    page = WorkItemProperties(V2Transport(config)).list("acme", "ENG")
    page.data[0].property_options.list()

    assert responses.calls[1].request.url == f"{base}/work-item-properties/p1/options/"


@responses.activate
def test_fetched_workspace_property_reaches_its_options(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/work-item-properties/p2/", json={"id": "p2", "name": "severity"})
    responses.get(
        f"{base}/work-item-properties/p2/options/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    property_row = WorkspaceWorkItemProperties(V2Transport(config)).retrieve("acme", "p2")
    property_row.property_options.list()

    assert responses.calls[1].request.url == f"{base}/work-item-properties/p2/options/"


@responses.activate
def test_fetched_workspace_property_reaches_its_contexts(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/work-item-properties/p2/", json={"id": "p2", "name": "severity"})
    responses.get(
        f"{base}/work-item-properties/p2/contexts/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    property_row = WorkspaceWorkItemProperties(V2Transport(config)).retrieve("acme", "p2")
    property_row.contexts.list()

    assert responses.calls[1].request.url == f"{base}/work-item-properties/p2/contexts/"


@responses.activate
def test_workspace_property_from_a_list_page_also_reaches_its_children(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(
        f"{base}/work-item-properties/",
        json={"data": [{"id": "p2", "name": "severity"}], "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{base}/work-item-properties/p2/contexts/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    page = WorkspaceWorkItemProperties(V2Transport(config)).list("acme")
    page.data[0].contexts.list()

    assert responses.calls[1].request.url == f"{base}/work-item-properties/p2/contexts/"
