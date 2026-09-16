"""`ProjectPages`/`WikiPages` against a real server; not parametrized through
`helpers.SPECS` since pages have a different shape. Deleting requires archiving first
(the server 400s otherwise) -- the `_archive_*` helpers do that PATCH before delete.

One file, both ways in, and the split is forced rather than chosen. Project pages hang
off the loaded `project`. Wiki pages do not: `wiki` is a grouping node holding no
`V2Resource` base of its own, so it consumes no path id, a loaded workspace
deliberately does not reach it, and `client.v2.workspaces.wiki.pages` takes the slug
itself. The uuid-vs-key parity check is flat for the usual reason."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.api.v2.pages import WikiPages
from plane.client import PlaneClient
from plane.models.v2.pages import CreatePage, UpdatePage

from .helpers import unique_name


@pytest.fixture
def workspace_pages(client: PlaneClient) -> WikiPages:
    return client.v2.workspaces.wiki.pages


def _archive_project_page(project: LoadedProject, page_id: str) -> None:
    # `is_locked=False` rides along unconditionally: a locked page 400s "Page is
    # locked." on any PATCH that omits `is_locked` (`_page_write_guards` in
    # `views/pages.py`), and this is cleanup, not the thing under test.
    project.pages.update(
        page_id, UpdatePage(archived_at=datetime.now(timezone.utc), is_locked=False)
    )


def _archive_workspace_page(workspace_pages: WikiPages, workspace_slug: str, page_id: str) -> None:
    workspace_pages.update(
        workspace_slug,
        page_id,
        UpdatePage(archived_at=datetime.now(timezone.utc), is_locked=False),
    )


class TestProjectPages:
    def test_create_then_retrieve(self, project: LoadedProject) -> None:
        name = unique_name("page")
        created = project.pages.create(CreatePage(name=name))
        try:
            assert created.name == name
            assert created.id

            fetched = project.pages.retrieve(created.id)
            assert fetched.id == created.id
        finally:
            _archive_project_page(project, created.id)
            project.pages.delete(created.id)

    def test_list_by_project_uuid_and_key_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        project: LoadedProject,
    ) -> None:
        created = project.pages.create(CreatePage(name=unique_name("page")))
        try:
            by_id = {row.id for row in project.pages.list().data}
            flat_pages = client.v2.workspaces.projects.pages
            by_key = {row.id for row in flat_pages.list(workspace_slug, project_key).data}
            assert created.id in by_id
            assert by_id == by_key
        finally:
            _archive_project_page(project, created.id)
            project.pages.delete(created.id)

    def test_patch_updates_only_the_given_fields(self, project: LoadedProject) -> None:
        created = project.pages.create(CreatePage(name=unique_name("page")))
        try:
            new_name = unique_name("page-renamed")
            updated = project.pages.update(created.id, UpdatePage(name=new_name))
            assert updated.id == created.id
            assert updated.name == new_name
        finally:
            _archive_project_page(project, created.id)
            project.pages.delete(created.id)

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        created = project.pages.create(CreatePage(name=unique_name("page")))
        _archive_project_page(project, created.id)
        project.pages.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.pages.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_fields_returns_a_sparse_row(self, project: LoadedProject) -> None:
        created = project.pages.create(CreatePage(name=unique_name("page")))
        try:
            sparse = project.pages.retrieve(created.id, fields=["id"])
            assert sparse.id == created.id
            assert sparse.name is None
        finally:
            _archive_project_page(project, created.id)
            project.pages.delete(created.id)

    def test_expand_owned_by_rejects_an_unknown_relation(self, project: LoadedProject) -> None:
        with pytest.raises(ValueError, match="bogus"):
            project.pages.list(expand=["bogus"])

    def test_find_by_name(self, project: LoadedProject) -> None:
        name = unique_name("page")
        created = project.pages.create(CreatePage(name=name))
        try:
            assert project.pages.find_by_name(name).id == created.id
        finally:
            _archive_project_page(project, created.id)
            project.pages.delete(created.id)


class TestWikiPages:
    def test_create_then_retrieve_is_global(
        self, workspace_pages: WikiPages, workspace_slug: str
    ) -> None:
        name = unique_name("wiki-page")
        created = workspace_pages.create(workspace_slug, CreatePage(name=name))
        try:
            assert created.name == name
            assert created.is_global is True

            fetched = workspace_pages.retrieve(workspace_slug, created.id)
            assert fetched.id == created.id
        finally:
            _archive_workspace_page(workspace_pages, workspace_slug, created.id)
            workspace_pages.delete(workspace_slug, created.id)

    def test_patch_updates_only_the_given_fields(
        self, workspace_pages: WikiPages, workspace_slug: str
    ) -> None:
        created = workspace_pages.create(workspace_slug, CreatePage(name=unique_name("wiki-page")))
        try:
            updated = workspace_pages.update(workspace_slug, created.id, UpdatePage(is_locked=True))
            assert updated.is_locked is True
        finally:
            _archive_workspace_page(workspace_pages, workspace_slug, created.id)
            workspace_pages.delete(workspace_slug, created.id)

    def test_delete_then_retrieve_404s(
        self, workspace_pages: WikiPages, workspace_slug: str
    ) -> None:
        created = workspace_pages.create(workspace_slug, CreatePage(name=unique_name("wiki-page")))
        _archive_workspace_page(workspace_pages, workspace_slug, created.id)
        workspace_pages.delete(workspace_slug, created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace_pages.retrieve(workspace_slug, created.id)
        assert exc_info.value.status == 404

    def test_project_scoped_and_workspace_scoped_pages_are_disjoint(
        self,
        project: LoadedProject,
        workspace_pages: WikiPages,
        workspace_slug: str,
    ) -> None:
        project_page = project.pages.create(CreatePage(name=unique_name("proj-page")))
        try:
            workspace_ids = {row.id for row in workspace_pages.list(workspace_slug).data}
            assert project_page.id not in workspace_ids
        finally:
            _archive_project_page(project, project_page.id)
            project.pages.delete(project_page.id)
