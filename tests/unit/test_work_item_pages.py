"""Unit tests for WorkItemPages sub-resource (smoke tests with real HTTP requests)."""

import time

import pytest

from plane.client import PlaneClient
from plane.models.pages import CreatePage
from plane.models.projects import Project
from plane.models.work_item_pages import CreateWorkItemPage
from plane.models.work_items import CreateWorkItem


class TestWorkItemPagesAPI:
    """Test work item page link CRUD operations."""

    @pytest.fixture
    def work_item(self, client: PlaneClient, workspace_slug: str, project: Project):
        """Create a work item and delete it after the test."""
        wi = client.work_items.create(
            workspace_slug,
            project.id,
            CreateWorkItem(name=f"Test WI for pages {int(time.time())}"),
        )
        yield wi
        try:
            client.work_items.delete(workspace_slug, project.id, wi.id)
        except Exception:
            pass

    @pytest.fixture
    def page(self, client: PlaneClient, workspace_slug: str):
        """Create a workspace page to use in link tests."""
        return client.pages.create_workspace_page(
            workspace_slug,
            CreatePage(
                name=f"Test Page for WI link {int(time.time())}",
                description_html="<p>page for work item link test</p>",
            ),
        )

    def test_create_work_item_page_link(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item, page
    ) -> None:
        """Link a page to a work item."""
        link = None
        try:
            link = client.work_items.pages.create(
                workspace_slug,
                project.id,
                work_item.id,
                CreateWorkItemPage(page_id=page.id),
            )
            assert link is not None
            assert link.id is not None
            assert link.page is not None
            assert link.page.id == page.id
        finally:
            if link and link.id:
                try:
                    client.work_items.pages.delete(
                        workspace_slug, project.id, work_item.id, link.id
                    )
                except Exception:
                    pass

    def test_list_work_item_pages(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item, page
    ) -> None:
        """List page links for a work item."""
        link = client.work_items.pages.create(
            workspace_slug,
            project.id,
            work_item.id,
            CreateWorkItemPage(page_id=page.id),
        )
        try:
            response = client.work_items.pages.list(
                workspace_slug, project.id, work_item.id
            )
            assert response is not None
            assert hasattr(response, "results")
            assert isinstance(response.results, list)
            assert any(r.id == link.id for r in response.results)
        finally:
            try:
                client.work_items.pages.delete(
                    workspace_slug, project.id, work_item.id, link.id
                )
            except Exception:
                pass

    def test_retrieve_work_item_page(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item, page
    ) -> None:
        """Retrieve a specific page link by ID."""
        link = client.work_items.pages.create(
            workspace_slug,
            project.id,
            work_item.id,
            CreateWorkItemPage(page_id=page.id),
        )
        try:
            retrieved = client.work_items.pages.retrieve(
                workspace_slug, project.id, work_item.id, link.id
            )
            assert retrieved is not None
            assert retrieved.id == link.id
            assert retrieved.page is not None
            assert retrieved.page.id == page.id
        finally:
            try:
                client.work_items.pages.delete(
                    workspace_slug, project.id, work_item.id, link.id
                )
            except Exception:
                pass

    def test_delete_work_item_page(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item, page
    ) -> None:
        """Remove a page link from a work item."""
        link = client.work_items.pages.create(
            workspace_slug,
            project.id,
            work_item.id,
            CreateWorkItemPage(page_id=page.id),
        )
        client.work_items.pages.delete(workspace_slug, project.id, work_item.id, link.id)

        response = client.work_items.pages.list(
            workspace_slug, project.id, work_item.id
        )
        assert not any(r.id == link.id for r in response.results)
