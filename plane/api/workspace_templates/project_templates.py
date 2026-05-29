from typing import Any

from ...models.workspace_templates import (
    CreateProjectTemplate,
    ProjectTemplate,
    UpdateProjectTemplate,
)
from ..base_resource import BaseResource


class WorkspaceProjectTemplates(BaseResource):
    """API client for managing workspace-level project templates."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str) -> list[ProjectTemplate]:
        """List all project templates in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/projects/templates/")
        return [ProjectTemplate.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreateProjectTemplate) -> ProjectTemplate:
        """Create a new project template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Project template data
        """
        response = self._post(
            f"{workspace_slug}/projects/templates/",
            data.model_dump(exclude_none=True),
        )
        return ProjectTemplate.model_validate(response)

    def update(
        self, workspace_slug: str, template_id: str, data: UpdateProjectTemplate
    ) -> ProjectTemplate:
        """Update a project template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            template_id: UUID of the template
            data: Updated template data
        """
        response = self._patch(
            f"{workspace_slug}/projects/templates/{template_id}/",
            data.model_dump(exclude_none=True),
        )
        return ProjectTemplate.model_validate(response)

    def delete(self, workspace_slug: str, template_id: str) -> None:
        """Delete a project template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            template_id: UUID of the template
        """
        return self._delete(f"{workspace_slug}/projects/templates/{template_id}/")
