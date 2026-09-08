"""Live smoke test for the v2 surface; skips unless
PLANE_BASE_URL/PLANE_API_KEY/WORKSPACE_SLUG/V2_PROJECT are set.

Outside `tests/v2/integration/`, so outside the silent-skip guard's scope -- but the
same trap applies, and this file fell into it too: both tests were written against the
retired `client.v2.workspace(slug).project(key)` locator and had been skipping green
ever since. `tests/v2/test_integration_surface.py` does not cover this path either,
so the two calls below are deliberately spelled once each way: the flat path and a
loaded row. A regression in either is a compile error under `mypy tests/v2`."""

import os

import pytest

from plane.client import PlaneClient


@pytest.fixture(scope="module")
def live_client() -> PlaneClient:
    base_url = os.getenv("PLANE_BASE_URL")
    api_key = os.getenv("PLANE_API_KEY")
    if not base_url or not api_key:
        pytest.skip("PLANE_BASE_URL and PLANE_API_KEY must be set for live v2 tests")
    return PlaneClient(base_url=base_url, api_key=api_key)


@pytest.fixture(scope="module")
def workspace_slug() -> str:
    slug = os.getenv("WORKSPACE_SLUG")
    if not slug:
        pytest.skip("WORKSPACE_SLUG not set")
    return slug


@pytest.fixture(scope="module")
def project_key() -> str:
    key = os.getenv("V2_PROJECT")
    if not key:
        pytest.skip("V2_PROJECT (project key or id) not set")
    return key


def test_states_round_trip(live_client: PlaneClient, workspace_slug: str, project_key: str) -> None:
    """The flat path, with both ids passed explicitly."""
    states = live_client.v2.workspaces.projects.states
    page = states.list(workspace_slug, project_key, fields=["id", "name"])
    assert page.data, "expected at least one state in the project"

    first = page.data[0]
    assert first.name is not None
    found = states.find_by_name(workspace_slug, project_key, first.name)
    assert found.id == first.id


def test_labels_list_through_a_loaded_project(
    live_client: PlaneClient, workspace_slug: str, project_key: str
) -> None:
    """The other way in: fetch the project, then navigate off the row."""
    project = live_client.v2.workspaces.projects.retrieve(workspace_slug, project_key)
    assert project.labels.list(fields=["id", "name"]) is not None
