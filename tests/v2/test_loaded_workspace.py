"""`Workspaces` is the design's navigable row #1 and was the last one that was not.

`client.v2.workspaces.retrieve("acme")` used to hand back a bare `Workspace`, so
`workspace.projects` raised `AttributeError` on the SDK's most-used entry point while
every other fetch returned a navigable row. These are the behaviour tests for the
fix; `tests/v2/test_loaded_navigation.py` is the structural sweep that keeps
`LoadedWorkspace` in step with what `Workspaces.__init__` attaches.
"""

from __future__ import annotations

import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._loaded.workspace import LoadedWorkspace
from plane.config import Configuration

BASE = "https://api.example.com/api/v2/workspaces/acme"


@responses.activate
def test_a_fetched_workspace_is_a_loaded_row(config: Configuration) -> None:
    responses.get(f"{BASE}/", json={"id": "ws1", "slug": "acme", "name": "Acme"})

    workspace = V2Namespace(config).workspaces.retrieve("acme")

    assert isinstance(workspace, LoadedWorkspace)
    assert workspace.name == "Acme"


@responses.activate
def test_a_fetched_workspace_reaches_its_projects_without_repeating_the_slug(
    config: Configuration,
) -> None:
    responses.get(f"{BASE}/", json={"id": "ws1", "slug": "acme", "name": "Acme"})
    responses.get(
        f"{BASE}/projects/",
        json={
            "data": [{"id": "p1", "identifier": "ENG", "name": "Engineering"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = V2Namespace(config).workspaces.retrieve("acme").projects.list()

    assert str(responses.calls[1].request.url).startswith(f"{BASE}/projects/")
    assert page.data[0].name == "Engineering"


@responses.activate
def test_navigation_off_a_workspace_chains_three_levels_deep(config: Configuration) -> None:
    """The whole point of the entry point: workspace -> project -> work item ->
    comments, with the slug typed once."""
    responses.get(f"{BASE}/", json={"id": "ws1", "slug": "acme"})
    responses.get(f"{BASE}/projects/ENG/", json={"id": "p1", "identifier": "ENG"})
    responses.get(f"{BASE}/projects/ENG/work-items/ENG-12/", json={"id": "w1"})
    responses.get(
        f"{BASE}/projects/ENG/work-items/w1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    workspace = V2Namespace(config).workspaces.retrieve("acme")
    workspace.projects.retrieve("ENG").work_items.retrieve("ENG-12").comments.list()

    assert responses.calls[-1].request.url == f"{BASE}/projects/ENG/work-items/w1/comments/"


@pytest.mark.parametrize(
    ("attribute", "url"),
    [
        ("roles", f"{BASE}/roles/"),
        ("teamspaces", f"{BASE}/teamspaces/"),
        ("customers", f"{BASE}/customers/"),
        ("initiatives", f"{BASE}/initiatives/"),
        ("stickies", f"{BASE}/stickies/"),
        ("work_items", f"{BASE}/work-items/"),
        ("work_item_types", f"{BASE}/work-item-types/"),
        ("views", f"{BASE}/views/"),
        ("webhooks", f"{BASE}/webhooks/"),
        ("releases", f"{BASE}/releases/"),
    ],
)
@responses.activate
def test_a_sample_of_children_reach_their_own_urls_from_the_row(
    config: Configuration, attribute: str, url: str
) -> None:
    """A spot check across the band that the sweep's structural equality cannot make:
    the `Owned` really does prepend the slug into a working URL."""
    responses.get(f"{BASE}/", json={"id": "ws1", "slug": "acme"})
    responses.get(url, json={"data": [], "pagination": {"style": "offset"}, "total_count": 0})

    workspace = V2Namespace(config).workspaces.retrieve("acme")
    getattr(workspace, attribute).list()

    assert str(responses.calls[1].request.url).startswith(url)


@responses.activate
def test_the_workspace_singleton_child_is_reachable_too(config: Configuration) -> None:
    """`features` is a singleton (`get`/`update`), not CRUD -- it still binds the slug."""
    responses.get(f"{BASE}/", json={"id": "ws1", "slug": "acme"})
    responses.get(f"{BASE}/features/", json={"id": "f1", "is_project_grouping_enabled": True})

    V2Namespace(config).workspaces.retrieve("acme").features.get()

    assert str(responses.calls[1].request.url).startswith(f"{BASE}/features/")


@responses.activate
def test_field_presence_still_bites_on_a_loaded_workspace(config: Configuration) -> None:
    responses.get(f"{BASE}/", json={"id": "ws1", "slug": "acme", "name": "Acme"})

    workspace = V2Namespace(config).workspaces.retrieve("acme", fields=["name"])

    assert workspace.name == "Acme"
    with pytest.raises(FieldNotRequested, match="timezone"):
        _ = workspace.timezone


@responses.activate
def test_a_projection_that_drops_the_slug_still_navigates(config: Configuration) -> None:
    """Every other resource falls back to `id` for its children's path id; a
    workspace cannot, because `{slug}` does not accept the UUID. `retrieve` fills the
    slug the caller addressed the row by, so `fields=["name"]` does not silently
    build `/workspaces/None/projects/`."""
    responses.get(f"{BASE}/", json={"id": "ws1", "name": "Acme"})
    responses.get(
        f"{BASE}/projects/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    workspace = V2Namespace(config).workspaces.retrieve("acme", fields=["name"])
    workspace.projects.list()

    assert str(responses.calls[1].request.url).startswith(f"{BASE}/projects/")
    # Filling it in is a navigation fix, not a widening of what was requested.
    with pytest.raises(FieldNotRequested, match="slug"):
        _ = workspace.slug


@responses.activate
def test_the_grouping_nodes_are_not_navigation_properties(config: Configuration) -> None:
    """`wiki` and `group_sync` hold no `V2Resource` base and consume no path id, so
    they are not children a row can bind -- reach them from the namespace instead.
    Asserted so the omission reads as the ruling it is."""
    responses.get(f"{BASE}/", json={"id": "ws1", "slug": "acme"})

    workspace = V2Namespace(config).workspaces.retrieve("acme")

    assert not hasattr(workspace, "wiki")
    assert not hasattr(workspace, "group_sync")
