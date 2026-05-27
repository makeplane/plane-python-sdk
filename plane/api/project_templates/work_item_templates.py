from typing import Any

from ...models.project_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplate,
)
from ..base_resource import BaseResource


class ProjectWorkItemTemplates(BaseResource):
    """API client for managing work item templates within a project."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, project_id: str) -> list[WorkItemTemplate]:
        """List all work item templates for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project

        Returns:
            List of work item templates
        """
        data = self._get(f"{workspace_slug}/projects/{project_id}/workitems/templates")
        items = data.get("results", data) if isinstance(data, dict) else data
        return [WorkItemTemplate.model_validate(item) for item in items]

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        data: CreateWorkItemTemplate,
    ) -> WorkItemTemplate:
        """Create a new work item template for a project.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Template data

        Returns:
            The created work item template
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/workitems/templates",
            data.model_dump(exclude_none=True),
        )
        return WorkItemTemplate.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        template_id: str,
        data: UpdateWorkItemTemplate,
    ) -> WorkItemTemplate:
        """Update a work item template by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            template_id: UUID of the template
            data: Updated template data

        Returns:
            The updated work item template
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/workitems/templates/{template_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemTemplate.model_validate(response)

    def delete(
        self,
        workspace_slug: str,
        project_id: str,
        template_id: str,
    ) -> None:
        """Delete a work item template by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            template_id: UUID of the template
        """
        self._delete(f"{workspace_slug}/projects/{project_id}/workitems/templates/{template_id}")
