"""Live coverage for the `views` resource, both project- and workspace-scoped.
Reuses shared `client`/`workspace_slug`/`project_id` fixtures (skips without
live credentials); the disposable view is local to this file."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.project import Project
from plane.client import PlaneClient
from plane.models.v2.views import CreateView, UpdateView

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def project_view(proj: Project) -> Iterator[Any]:
    created = proj.views.create(CreateView(name=unique_name("view")))
    yield created
    try:
        proj.views.delete(created.id)
    except Exception:
        pass


class TestProjectViews:
    def test_list_includes_the_created_view(self, proj: Project, project_view: Any) -> None:
        page = proj.views.list()
        assert any(row.id == project_view.id for row in page.data)

    def test_patch_updates_the_name(self, proj: Project, project_view: Any) -> None:
        updated = proj.views.update(project_view.id, UpdateView(name="Renamed view"))
        assert updated.name == "Renamed view"

    def test_delete_then_retrieve_404s(self, proj: Project) -> None:
        created = proj.views.create(CreateView(name=unique_name("view")))
        proj.views.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.views.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkspaceViews:
    def test_create_list_delete_round_trip(self, client: PlaneClient, workspace_slug: str) -> None:
        views = client.v2.workspace(workspace_slug).views
        created = views.create(CreateView(name=unique_name("ws-view")))
        try:
            page = views.list()
            assert any(row.id == created.id for row in page.data)
        finally:
            views.delete(created.id)

    def test_uses_a_different_path_than_project_views(
        self, client: PlaneClient, workspace_slug: str, project_view: Any
    ) -> None:
        """A project-scoped view must not leak into the workspace-scoped list --
        the two hit different path templates against project=NULL vs a real one."""
        workspace_page = client.v2.workspace(workspace_slug).views.list()
        assert not any(row.id == project_view.id for row in workspace_page.data)
