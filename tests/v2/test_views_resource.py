"""Offline coverage for `ProjectViews`/`WorkspaceViews`; shared shape, different path templates,
plus `?expand=owned_by`."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.views import ProjectViews, WorkspaceViews
from plane.config import Configuration
from plane.models.v2.views import CreateView, UpdateView

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def project_views(config: Configuration) -> ProjectViews:
    return ProjectViews(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_views(config: Configuration) -> WorkspaceViews:
    return WorkspaceViews(V2Transport(config), slug="acme")


@responses.activate
def test_project_views_crud(project_views: ProjectViews) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/views/",
        json={"data": [{"id": "1", "name": "My view"}], "pagination": {"style": "offset"}},
    )
    responses.post(
        f"{BASE}/workspaces/acme/projects/ENG/views/",
        json={"id": "2", "name": "Sprint board"},
        status=201,
    )
    responses.patch(
        f"{BASE}/workspaces/acme/projects/ENG/views/2/",
        json={"id": "2", "name": "Sprint board v2"},
    )
    responses.delete(f"{BASE}/workspaces/acme/projects/ENG/views/2/", status=204)

    page = project_views.list()
    assert page.data[0].name == "My view"

    created = project_views.create(CreateView(name="Sprint board"))
    assert created.id == "2"

    updated = project_views.update(created.id, UpdateView(name="Sprint board v2"))
    assert updated.name == "Sprint board v2"

    assert project_views.delete(created.id) is None


@responses.activate
def test_workspace_views_use_a_different_path_than_project_views(
    workspace_views: WorkspaceViews,
) -> None:
    """Project and workspace views share a read/write shape but hit different path
    templates -- `.../projects/{project_id}/views/` vs `.../views/` with no project
    segment at all."""
    responses.get(
        f"{BASE}/workspaces/acme/views/",
        json={"data": [{"id": "1", "name": "Workspace view"}], "pagination": {"style": "offset"}},
    )

    page = workspace_views.list()

    assert page.data[0].name == "Workspace view"
    assert responses.calls[0].request.url.startswith(f"{BASE}/workspaces/acme/views/")


@responses.activate
def test_views_expand_owned_by(project_views: ProjectViews) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/views/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    project_views.list(expand=["owned_by"])

    assert "expand=owned_by" in responses.calls[0].request.url


def test_views_unknown_expand_is_rejected_before_the_request(project_views: ProjectViews) -> None:
    with pytest.raises(ValueError, match="nope"):
        project_views.list(expand=["nope"])
