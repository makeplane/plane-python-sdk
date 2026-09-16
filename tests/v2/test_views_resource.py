"""Offline coverage for `ProjectViews`/`WorkspaceViews`; shared shape, different path templates,
plus `?expand=owned_by`.

Both are migrated flat: `WorkspaceViews` (leading `slug`), per Task 3, and
`ProjectViews` (leading `slug, project`), per Task 1."""

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
    return ProjectViews(V2Transport(config))


@pytest.fixture
def workspace_views(config: Configuration) -> WorkspaceViews:
    return WorkspaceViews(V2Transport(config))


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

    page = project_views.list("acme", "ENG")
    assert page.data[0].name == "My view"

    created = project_views.create("acme", "ENG", CreateView(name="Sprint board"))
    assert created.id == "2"

    updated = project_views.update("acme", "ENG", created.id, UpdateView(name="Sprint board v2"))
    assert updated.name == "Sprint board v2"

    assert project_views.delete("acme", "ENG", created.id) is None


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

    page = workspace_views.list("acme")

    assert page.data[0].name == "Workspace view"
    assert responses.calls[0].request.url.startswith(f"{BASE}/workspaces/acme/views/")


@responses.activate
def test_views_expand_owned_by(project_views: ProjectViews) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/views/",
        json={"data": [], "pagination": {"style": "offset"}},
    )

    project_views.list("acme", "ENG", expand=["owned_by"])

    assert "expand=owned_by" in responses.calls[0].request.url


def test_views_unknown_expand_is_rejected_before_the_request(project_views: ProjectViews) -> None:
    with pytest.raises(ValueError, match="nope"):
        project_views.list("acme", "ENG", expand=["nope"])


@responses.activate
def test_workspace_views_retrieve(workspace_views: WorkspaceViews) -> None:
    responses.get(f"{BASE}/workspaces/acme/views/1/", json={"id": "1", "name": "Workspace view"})

    view = workspace_views.retrieve("acme", "1")

    assert view.name == "Workspace view"
    assert responses.calls[0].request.url == f"{BASE}/workspaces/acme/views/1/"


@responses.activate
def test_workspace_views_create_then_patch(workspace_views: WorkspaceViews) -> None:
    responses.post(
        f"{BASE}/workspaces/acme/views/", json={"id": "2", "name": "Sprint board"}, status=201
    )
    responses.patch(f"{BASE}/workspaces/acme/views/2/", json={"id": "2", "name": "Sprint board v2"})

    created = workspace_views.create("acme", CreateView(name="Sprint board"))
    assert responses.calls[0].request.url == f"{BASE}/workspaces/acme/views/"

    updated = workspace_views.update("acme", created.id, UpdateView(name="Sprint board v2"))

    assert updated.name == "Sprint board v2"
    assert responses.calls[1].request.url == f"{BASE}/workspaces/acme/views/2/"


@responses.activate
def test_workspace_views_delete(workspace_views: WorkspaceViews) -> None:
    responses.delete(f"{BASE}/workspaces/acme/views/2/", status=204)

    assert workspace_views.delete("acme", "2") is None
    assert responses.calls[0].request.url == f"{BASE}/workspaces/acme/views/2/"


@responses.activate
def test_workspace_views_iterate(workspace_views: WorkspaceViews) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/views/",
        json={"data": [{"id": "1", "name": "Workspace view"}], "pagination": {"style": "offset"}},
    )

    rows = list(workspace_views.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/workspaces/acme/views/")


@responses.activate
def test_workspace_views_list_per_page_and_offset(workspace_views: WorkspaceViews) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/views/", json={"data": [], "pagination": {"style": "offset"}}
    )

    workspace_views.list("acme", per_page=20, offset=40)

    request_url = responses.calls[0].request.url
    assert "per_page=20" in request_url
    assert "offset=40" in request_url


@responses.activate
def test_workspace_views_create_and_update_pass_expand(workspace_views: WorkspaceViews) -> None:
    """`workspace_views_create`/`_partial_update` both expand `owned_by` in the
    golden; the parameter was missing, so the capability was unreachable."""
    responses.post(f"{BASE}/workspaces/acme/views/", json={"id": "v1", "name": "Mine"})
    responses.patch(f"{BASE}/workspaces/acme/views/v1/", json={"id": "v1", "name": "Mine"})

    workspace_views.create("acme", CreateView(name="Mine"), expand=["owned_by"])
    workspace_views.update("acme", "v1", UpdateView(name="Mine"), expand=["owned_by"])

    assert "expand=owned_by" in responses.calls[0].request.url
    assert "expand=owned_by" in responses.calls[1].request.url


def test_workspace_views_create_rejects_unknown_expand(workspace_views: WorkspaceViews) -> None:
    with pytest.raises(ValueError, match="Unknown expand"):
        workspace_views.create("acme", CreateView(name="Mine"), expand=["bogus"])
