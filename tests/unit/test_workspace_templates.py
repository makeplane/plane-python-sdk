"""Unit tests for WorkspaceTemplates API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

from plane.client import PlaneClient
from plane.models.workspace_templates import (
    CreatePageTemplate,
    CreateProjectTemplate,
    CreateWorkItemTemplate,
    UpdatePageTemplate,
    UpdateProjectTemplate,
    UpdateWorkItemTemplate,
)


class TestWorkspaceWorkItemTemplates:
    """Test WorkspaceTemplates.work_items sub-resource."""

    def test_list_work_item_templates(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace work item templates."""
        templates = client.workspace_templates.work_items.list(workspace_slug)
        assert isinstance(templates, list)

    def test_create_update_delete_work_item_template(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test create, update, and delete of a workspace work item template."""
        name = f"test-wi-tpl-{uuid4().hex[:8]}"
        data = CreateWorkItemTemplate(name=name, description="Test work item template")
        created = client.workspace_templates.work_items.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        try:
            updated = client.workspace_templates.work_items.update(
                workspace_slug,
                created.id,
                UpdateWorkItemTemplate(description="Updated description"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated description"
        finally:
            try:
                client.workspace_templates.work_items.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for work item template {created.id}: {exc}",
                    stacklevel=1,
                )


class TestWorkspaceProjectTemplates:
    """Test WorkspaceTemplates.projects sub-resource."""

    def test_list_project_templates(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace project templates."""
        templates = client.workspace_templates.projects.list(workspace_slug)
        assert isinstance(templates, list)

    def test_create_update_delete_project_template(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test create, update, and delete of a workspace project template."""
        name = f"test-proj-tpl-{uuid4().hex[:8]}"
        data = CreateProjectTemplate(name=name, description="Test project template")
        created = client.workspace_templates.projects.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        try:
            updated = client.workspace_templates.projects.update(
                workspace_slug,
                created.id,
                UpdateProjectTemplate(description="Updated description"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated description"
        finally:
            try:
                client.workspace_templates.projects.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for project template {created.id}: {exc}",
                    stacklevel=1,
                )


class TestWorkspacePageTemplates:
    """Test WorkspaceTemplates.pages sub-resource."""

    def test_list_page_templates(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace page templates."""
        templates = client.workspace_templates.pages.list(workspace_slug)
        assert isinstance(templates, list)

    def test_create_update_delete_page_template(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test create, update, and delete of a workspace page template."""
        name = f"test-page-tpl-{uuid4().hex[:8]}"
        data = CreatePageTemplate(name=name, description="Test page template")
        created = client.workspace_templates.pages.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        try:
            updated = client.workspace_templates.pages.update(
                workspace_slug,
                created.id,
                UpdatePageTemplate(description="Updated description"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated description"
        finally:
            try:
                client.workspace_templates.pages.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for page template {created.id}: {exc}",
                    stacklevel=1,
                )
