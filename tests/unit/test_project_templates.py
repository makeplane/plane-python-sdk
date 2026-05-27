"""Unit tests for Project Templates API resources (smoke tests with real HTTP requests)."""

import pytest

from plane.client import PlaneClient
from plane.models.project_templates import (
    CreatePageTemplate,
    CreateWorkItemTemplate,
    UpdatePageTemplate,
    UpdateWorkItemTemplate,
)
from plane.models.projects import Project


class TestProjectWorkItemTemplatesAPI:
    """Test ProjectWorkItemTemplates API resource."""

    def test_list_work_item_templates(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing work item templates for a project."""
        response = client.project_templates.work_item_templates.list(workspace_slug, project.id)
        assert response is not None
        assert isinstance(response, list)


class TestProjectWorkItemTemplatesAPICRUD:
    """Test ProjectWorkItemTemplates API CRUD operations."""

    @pytest.fixture
    def template_data(self) -> CreateWorkItemTemplate:
        """Create test work item template data."""
        import time

        return CreateWorkItemTemplate(
            name=f"Test WI Template {int(time.time())}",
            short_description="A test work item template",
        )

    @pytest.fixture
    def work_item_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        template_data: CreateWorkItemTemplate,
    ):
        """Create a test work item template and yield it, then delete it."""
        tmpl = client.project_templates.work_item_templates.create(
            workspace_slug, project.id, template_data
        )
        yield tmpl
        try:
            client.project_templates.work_item_templates.delete(workspace_slug, project.id, tmpl.id)
        except Exception:
            pass

    def test_create_work_item_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        template_data: CreateWorkItemTemplate,
    ) -> None:
        """Test creating a work item template."""
        tmpl = client.project_templates.work_item_templates.create(
            workspace_slug, project.id, template_data
        )
        assert tmpl is not None
        assert tmpl.id is not None
        assert tmpl.name == template_data.name
        # Cleanup
        try:
            client.project_templates.work_item_templates.delete(workspace_slug, project.id, tmpl.id)
        except Exception:
            pass

    def test_update_work_item_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_template,
    ) -> None:
        """Test updating a work item template."""
        updated = client.project_templates.work_item_templates.update(
            workspace_slug,
            project.id,
            work_item_template.id,
            UpdateWorkItemTemplate(short_description="Updated description"),
        )
        assert updated is not None
        assert updated.id == work_item_template.id
        assert updated.short_description == "Updated description"

    def test_delete_work_item_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        template_data: CreateWorkItemTemplate,
    ) -> None:
        """Test deleting a work item template."""
        import time

        data = CreateWorkItemTemplate(name=f"Delete Me WI {int(time.time())}")
        tmpl = client.project_templates.work_item_templates.create(workspace_slug, project.id, data)
        assert tmpl.id is not None
        client.project_templates.work_item_templates.delete(workspace_slug, project.id, tmpl.id)


class TestProjectPageTemplatesAPI:
    """Test ProjectPageTemplates API resource."""

    def test_list_page_templates(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> None:
        """Test listing page templates for a project."""
        response = client.project_templates.page_templates.list(workspace_slug, project.id)
        assert response is not None
        assert isinstance(response, list)


class TestProjectPageTemplatesAPICRUD:
    """Test ProjectPageTemplates API CRUD operations."""

    @pytest.fixture
    def page_template_data(self) -> CreatePageTemplate:
        """Create test page template data."""
        import time

        return CreatePageTemplate(
            name=f"Test Page Template {int(time.time())}",
            short_description="A test page template",
        )

    @pytest.fixture
    def page_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        page_template_data: CreatePageTemplate,
    ):
        """Create a test page template and yield it, then delete it."""
        tmpl = client.project_templates.page_templates.create(
            workspace_slug, project.id, page_template_data
        )
        yield tmpl
        try:
            client.project_templates.page_templates.delete(workspace_slug, project.id, tmpl.id)
        except Exception:
            pass

    def test_create_page_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        page_template_data: CreatePageTemplate,
    ) -> None:
        """Test creating a page template."""
        tmpl = client.project_templates.page_templates.create(
            workspace_slug, project.id, page_template_data
        )
        assert tmpl is not None
        assert tmpl.id is not None
        assert tmpl.name == page_template_data.name
        # Cleanup
        try:
            client.project_templates.page_templates.delete(workspace_slug, project.id, tmpl.id)
        except Exception:
            pass

    def test_update_page_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        page_template,
    ) -> None:
        """Test updating a page template."""
        updated = client.project_templates.page_templates.update(
            workspace_slug,
            project.id,
            page_template.id,
            UpdatePageTemplate(short_description="Updated description"),
        )
        assert updated is not None
        assert updated.id == page_template.id
        assert updated.short_description == "Updated description"

    def test_delete_page_template(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
    ) -> None:
        """Test deleting a page template."""
        import time

        data = CreatePageTemplate(name=f"Delete Me Page {int(time.time())}")
        tmpl = client.project_templates.page_templates.create(workspace_slug, project.id, data)
        assert tmpl.id is not None
        client.project_templates.page_templates.delete(workspace_slug, project.id, tmpl.id)
