"""`ProjectPages`/`WikiPages` against a real server; not parametrized through
`helpers.SPECS` since pages have a different shape. Deleting requires archiving
first (server 400s otherwise) -- `_archive` below does that PATCH before every delete."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.pages import ProjectPages, WikiPages
from plane.client import PlaneClient
from plane.models.v2.pages import CreatePage, UpdatePage

from .helpers import unique_name


@pytest.fixture
def project_pages(client: PlaneClient, workspace_slug: str, project_id: str) -> ProjectPages:
    return client.v2.workspace(workspace_slug).project(project_id).pages


@pytest.fixture
def workspace_pages(client: PlaneClient, workspace_slug: str) -> WikiPages:
    return client.v2.workspace(workspace_slug).wiki.pages


def _archive_project_page(project_pages: ProjectPages, page_id: str) -> None:
    # `is_locked=False` rides along unconditionally: a locked page 400s "Page is
    # locked." on any PATCH that omits `is_locked` (`_page_write_guards` in
    # `views/pages.py`), and this is cleanup, not the thing under test.
    project_pages.update(
        page_id, UpdatePage(archived_at=datetime.now(timezone.utc), is_locked=False)
    )


def _archive_workspace_page(workspace_pages: WikiPages, page_id: str) -> None:
    workspace_pages.update(
        page_id, UpdatePage(archived_at=datetime.now(timezone.utc), is_locked=False)
    )


class TestProjectPages:
    def test_create_then_retrieve(self, project_pages: ProjectPages) -> None:
        name = unique_name("page")
        created = project_pages.create(CreatePage(name=name))
        try:
            assert created.name == name
            assert created.id

            fetched = project_pages.retrieve(created.id)
            assert fetched.id == created.id
        finally:
            _archive_project_page(project_pages, created.id)
            project_pages.delete(created.id)

    def test_list_by_project_uuid_and_key_agree(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        project_key: str,
        project_pages: ProjectPages,
    ) -> None:
        created = project_pages.create(CreatePage(name=unique_name("page")))
        try:
            by_id = {row.id for row in project_pages.list().data}
            key_scope = client.v2.workspace(workspace_slug).project(project_key)
            by_key = {row.id for row in key_scope.pages.list().data}
            assert created.id in by_id
            assert by_id == by_key
        finally:
            _archive_project_page(project_pages, created.id)
            project_pages.delete(created.id)

    def test_patch_updates_only_the_given_fields(self, project_pages: ProjectPages) -> None:
        created = project_pages.create(CreatePage(name=unique_name("page")))
        try:
            new_name = unique_name("page-renamed")
            updated = project_pages.update(created.id, UpdatePage(name=new_name))
            assert updated.id == created.id
            assert updated.name == new_name
        finally:
            _archive_project_page(project_pages, created.id)
            project_pages.delete(created.id)

    def test_delete_then_retrieve_404s(self, project_pages: ProjectPages) -> None:
        created = project_pages.create(CreatePage(name=unique_name("page")))
        _archive_project_page(project_pages, created.id)
        project_pages.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project_pages.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_fields_returns_a_sparse_row(self, project_pages: ProjectPages) -> None:
        created = project_pages.create(CreatePage(name=unique_name("page")))
        try:
            sparse = project_pages.retrieve(created.id, fields=["id"])
            assert sparse.id == created.id
            assert sparse.name is None
        finally:
            _archive_project_page(project_pages, created.id)
            project_pages.delete(created.id)

    def test_expand_owned_by_rejects_an_unknown_relation(
        self, project_pages: ProjectPages
    ) -> None:
        with pytest.raises(ValueError, match="bogus"):
            project_pages.list(expand=["bogus"])

    def test_find_by_name(self, project_pages: ProjectPages) -> None:
        name = unique_name("page")
        created = project_pages.create(CreatePage(name=name))
        try:
            assert project_pages.find_by_name(name).id == created.id
        finally:
            _archive_project_page(project_pages, created.id)
            project_pages.delete(created.id)


class TestWikiPages:
    def test_create_then_retrieve_is_global(self, workspace_pages: WikiPages) -> None:
        name = unique_name("wiki-page")
        created = workspace_pages.create(CreatePage(name=name))
        try:
            assert created.name == name
            assert created.is_global is True

            fetched = workspace_pages.retrieve(created.id)
            assert fetched.id == created.id
        finally:
            _archive_workspace_page(workspace_pages, created.id)
            workspace_pages.delete(created.id)

    def test_patch_updates_only_the_given_fields(self, workspace_pages: WikiPages) -> None:
        created = workspace_pages.create(CreatePage(name=unique_name("wiki-page")))
        try:
            updated = workspace_pages.update(created.id, UpdatePage(is_locked=True))
            assert updated.is_locked is True
        finally:
            _archive_workspace_page(workspace_pages, created.id)
            workspace_pages.delete(created.id)

    def test_delete_then_retrieve_404s(self, workspace_pages: WikiPages) -> None:
        created = workspace_pages.create(CreatePage(name=unique_name("wiki-page")))
        _archive_workspace_page(workspace_pages, created.id)
        workspace_pages.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            workspace_pages.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_project_scoped_and_workspace_scoped_pages_are_disjoint(
        self,
        project_pages: ProjectPages,
        workspace_pages: WikiPages,
    ) -> None:
        project_page = project_pages.create(CreatePage(name=unique_name("proj-page")))
        try:
            workspace_ids = {row.id for row in workspace_pages.list().data}
            assert project_page.id not in workspace_ids
        finally:
            _archive_project_page(project_pages, project_page.id)
            project_pages.delete(project_page.id)
