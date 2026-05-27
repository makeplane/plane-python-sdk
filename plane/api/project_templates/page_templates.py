from typing import Any

from ...models.project_templates import (
    CreatePageTemplate,
    PageTemplate,
    UpdatePageTemplate,
)
from ..base_resource import BaseResource


class ProjectPageTemplates(BaseResource):
    """API client for managing page templates within a project."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, project_id: str) -> list[PageTemplate]:
        """List all page templates for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project

        Returns:
            List of page templates
        """
        data = self._get(f"{workspace_slug}/projects/{project_id}/pages/templates")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [PageTemplate.model_validate(item) for item in items]

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        data: CreatePageTemplate,
    ) -> PageTemplate:
        """Create a new page template for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Template data

        Returns:
            The created page template
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/pages/templates",
            data.model_dump(exclude_none=True),
        )
        return PageTemplate.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        template_id: str,
        data: UpdatePageTemplate,
    ) -> PageTemplate:
        """Update a page template by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            template_id: UUID of the template
            data: Updated template data

        Returns:
            The updated page template
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/pages/templates/{template_id}",
            data.model_dump(exclude_none=True),
        )
        return PageTemplate.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
        template_id: str,
    ) -> None:
        """Delete a page template by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            template_id: UUID of the template
        """
        self._delete(f"{workspace_slug}/projects/{project_id}/pages/templates/{template_id}")
