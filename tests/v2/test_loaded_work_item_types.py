"""Navigable rows for both work item type families: `LoadedWorkItemType` (child
`properties`, bound with `slug, project, type`) and `LoadedWorkspaceWorkItemType`
(the same child, bound with `slug, type`).

Neither `WorkItemTypes` nor `WorkspaceWorkItemTypes` is wired onto the tree yet
(that is task 6), so both are constructed directly through `V2Transport`, the same
way every other offline resource test in this package is."""

from __future__ import annotations

import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_item_types import WorkItemTypes, WorkspaceWorkItemTypes
from plane.config import Configuration


@responses.activate
def test_fetched_work_item_type_reaches_its_properties(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/work-item-types/t1/", json={"id": "t1", "name": "Bug"})
    responses.get(
        f"{base}/work-item-types/t1/properties/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    work_item_type = WorkItemTypes(V2Transport(config)).retrieve("acme", "ENG", "t1")
    work_item_type.properties.list()

    assert responses.calls[1].request.url == f"{base}/work-item-types/t1/properties/"


@responses.activate
def test_work_item_type_from_a_list_page_also_reaches_its_properties(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(
        f"{base}/work-item-types/",
        json={
            "data": [{"id": "t1", "name": "Bug"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )
    responses.get(
        f"{base}/work-item-types/t1/properties/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    page = WorkItemTypes(V2Transport(config)).list("acme", "ENG")
    page.data[0].properties.list()

    assert responses.calls[1].request.url == f"{base}/work-item-types/t1/properties/"


@responses.activate
def test_enabled_work_item_type_reaches_its_properties(config: Configuration) -> None:
    """`enable` returns a row of the resource's own model, so it is routed through
    `_load` like every other row-returning method."""
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.post(f"{base}/work-item-types/enable/", json={"id": "epic", "is_epic": True})
    responses.get(
        f"{base}/work-item-types/epic/properties/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    work_item_type = WorkItemTypes(V2Transport(config)).enable("acme", "ENG")
    work_item_type.properties.list()

    assert responses.calls[1].request.url == f"{base}/work-item-types/epic/properties/"


@responses.activate
def test_fetched_workspace_work_item_type_reaches_its_properties(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/work-item-types/t2/", json={"id": "t2", "name": "Bug"})
    responses.get(
        f"{base}/work-item-types/t2/properties/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    work_item_type = WorkspaceWorkItemTypes(V2Transport(config)).retrieve("acme", "t2")
    work_item_type.properties.list()

    assert responses.calls[1].request.url == f"{base}/work-item-types/t2/properties/"


@responses.activate
def test_workspace_work_item_type_from_a_list_page_also_reaches_its_properties(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(
        f"{base}/work-item-types/",
        json={"data": [{"id": "t2", "name": "Bug"}], "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{base}/work-item-types/t2/properties/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    page = WorkspaceWorkItemTypes(V2Transport(config)).list("acme")
    page.data[0].properties.list()

    assert responses.calls[1].request.url == f"{base}/work-item-types/t2/properties/"
