"""Live smoke test for the v2 surface; skips unless
PLANE_BASE_URL/PLANE_API_KEY/WORKSPACE_SLUG/V2_PROJECT are set."""

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
    scope = live_client.v2.workspace(workspace_slug).project(project_key)
    page = scope.states.list(fields=["id", "name"])
    assert page.data, "expected at least one state in the project"

    first = page.data[0]
    assert first.name is not None
    found = scope.states.find_by_name(first.name)
    assert found.id == first.id


def test_chained_labels_list(
    live_client: PlaneClient, workspace_slug: str, project_key: str
) -> None:
    scope = live_client.v2.workspace(workspace_slug).project(project_key)
    assert scope.labels.list(fields=["id", "name"]) is not None
