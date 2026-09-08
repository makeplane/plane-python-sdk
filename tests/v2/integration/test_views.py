"""Live coverage for the `views` resource, both project- and workspace-scoped.

Deliberately mixed: the project-scoped half navigates off the loaded `project` row,
while the workspace-scoped half goes down the flat path with the slug passed
explicitly. The point of the last test is that the two are *different URLs*, so
spelling both the same way would make the assertion read as a tautology."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.views import CreateView, UpdateView

from .helpers import unique_name


@pytest.fixture
def project_view(project: LoadedProject) -> Iterator[Any]:
    created = project.views.create(CreateView(name=unique_name("view")))
    yield created
    try:
        project.views.delete(created.id)
    except Exception:
        pass


class TestProjectViews:
    def test_list_includes_the_created_view(self, project: LoadedProject, project_view: Any) -> None:
        page = project.views.list()
        assert any(row.id == project_view.id for row in page.data)

    def test_patch_updates_the_name(self, project: LoadedProject, project_view: Any) -> None:
        updated = project.views.update(project_view.id, UpdateView(name="Renamed view"))
        assert updated.name == "Renamed view"

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        created = project.views.create(CreateView(name=unique_name("view")))
        project.views.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.views.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkspaceViews:
    def test_create_list_delete_round_trip(self, client: PlaneClient, workspace_slug: str) -> None:
        views = client.v2.workspaces.views
        created = views.create(workspace_slug, CreateView(name=unique_name("ws-view")))
        try:
            page = views.list(workspace_slug)
            assert any(row.id == created.id for row in page.data)
        finally:
            views.delete(workspace_slug, created.id)

    def test_uses_a_different_path_than_project_views(
        self, client: PlaneClient, workspace_slug: str, project_view: Any
    ) -> None:
        """A project-scoped view must not leak into the workspace-scoped list --
        the two hit different path templates against project=NULL vs a real one."""
        workspace_page = client.v2.workspaces.views.list(workspace_slug)
        assert not any(row.id == project_view.id for row in workspace_page.data)
