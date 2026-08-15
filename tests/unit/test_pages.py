"""Unit tests for Pages API resource (smoke tests with real HTTP requests)."""

import time

import pytest

from plane.client import PlaneClient
from plane.models.pages import CreatePage, PaginatedPageResponse, UpdatePage
from plane.models.projects import Project


def _requires_live(exc: Exception) -> None:
    """Skip when the live collaboration service is absent, and only then.

    It answers one identified failure. Skipping on the status alone would swallow any
    other 502 -- a proxy fault or an API regression -- as "environment not available".
    """
    if "Failed to update page document" in str(exc):
        pytest.skip("requires Plane's live collaboration service")
    raise exc


class TestPagesAPI:
    """Test Pages API resource."""

    def test_create_project_page(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test creating a project page."""
        page_data = CreatePage(
            name=f"Test Page {int(time.time())}",
            description_html="<p>Test page description</p>",
            color="#4ECDC4",
        )

        page = client.pages.create_project_page(workspace_slug, project.id, page_data)
        assert page is not None
        assert page.id is not None
        assert page.name == page_data.name

    def test_create_workspace_page(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test creating a workspace page."""
        page_data = CreatePage(
            name=f"Test Workspace Page {int(time.time())}",
            description_html="<p>Test workspace page</p>",
            color="#FF6B6B",
        )

        page = client.pages.create_workspace_page(workspace_slug, page_data)
        assert page is not None
        assert page.id is not None
        assert page.name == page_data.name

    def test_list_workspace_pages(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test listing workspace pages returns paginated response."""
        response = client.pages.list_workspace_pages(workspace_slug)
        assert isinstance(response, PaginatedPageResponse)
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    def test_list_workspace_pages_contains_created_page(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test that a freshly created workspace page appears in the list."""
        page_data = CreatePage(
            name=f"Listable Workspace Page {int(time.time())}",
            description_html="<p>list test</p>",
        )
        created = client.pages.create_workspace_page(workspace_slug, page_data)
        try:
            response = client.pages.list_workspace_pages(workspace_slug)
            page_ids = [p.id for p in response.results]
            assert created.id in page_ids
        finally:
            try:
                client.pages.delete_workspace_page(workspace_slug, created.id)
            except Exception:
                pass

    def test_list_project_pages(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing project pages returns paginated response."""
        response = client.pages.list_project_pages(workspace_slug, project.id)
        assert isinstance(response, PaginatedPageResponse)
        assert hasattr(response, "results")
        assert isinstance(response.results, list)

    def test_list_project_pages_contains_created_page(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test that a freshly created project page appears in the list."""
        page_data = CreatePage(
            name=f"Listable Project Page {int(time.time())}",
            description_html="<p>list test</p>",
        )
        created = client.pages.create_project_page(workspace_slug, project.id, page_data)
        try:
            response = client.pages.list_project_pages(workspace_slug, project.id)
            page_ids = [p.id for p in response.results]
            assert created.id in page_ids
        finally:
            try:
                client.pages.delete_project_page(workspace_slug, project.id, created.id)
            except Exception:
                pass

    def test_update_project_page(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test updating a project page's name and content."""
        page = client.pages.create_project_page(
            workspace_slug,
            project.id,
            CreatePage(
                name=f"Test Update {int(time.time())}",
                description_html="<p>first draft</p>",
            ),
        )

        try:
            updated = client.pages.update_project_page(
                workspace_slug,
                project.id,
                page.id,
                UpdatePage(name=f"{page.name} (edited)", description_html="<p>revised</p>"),
            )
        except Exception as exc:  # noqa: BLE001 - a missing live server is a skip, not a failure
            _requires_live(exc)

        assert updated.id == page.id
        assert updated.name == f"{page.name} (edited)"
        assert "revised" in (updated.description_html or "")

    def test_update_workspace_page(self, client: PlaneClient, workspace_slug: str) -> None:
        """Test updating a workspace page."""
        page = client.pages.create_workspace_page(
            workspace_slug,
            CreatePage(
                name=f"Test WS Update {int(time.time())}",
                description_html="<p>first draft</p>",
            ),
        )

        try:
            updated = client.pages.update_workspace_page(
                workspace_slug, page.id, UpdatePage(name=f"{page.name} (edited)")
            )
        except Exception as exc:  # noqa: BLE001 - a missing live server is a skip, not a failure
            _requires_live(exc)

        assert updated.id == page.id
        assert updated.name == f"{page.name} (edited)"

    def test_update_project_page_needs_a_field_to_change(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """An update carrying nothing is refused rather than reported as a no-op."""
        page = client.pages.create_project_page(
            workspace_slug,
            project.id,
            CreatePage(name=f"Test Empty {int(time.time())}", description_html="<p>draft</p>"),
        )

        try:
            client.pages.update_project_page(workspace_slug, project.id, page.id, UpdatePage())
        except Exception as exc:  # noqa: BLE001 - the message is the assertion
            assert "name or description_html" in str(exc)
        else:
            raise AssertionError("an empty update was accepted")

    def test_delete_project_page_requires_archiving_first(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """The API refuses to delete a live page; the message says what to do."""
        page = client.pages.create_project_page(
            workspace_slug,
            project.id,
            CreatePage(name=f"Test Delete {int(time.time())}", description_html="<p>draft</p>"),
        )

        try:
            client.pages.delete_project_page(workspace_slug, project.id, page.id)
        except Exception as exc:  # noqa: BLE001 - the message is the assertion
            assert "archived" in str(exc)
        else:
            raise AssertionError("an unarchived page was deleted")
