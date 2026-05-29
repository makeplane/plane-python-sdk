from typing import Any

from ...models.workspace_templates import (
    CreatePageTemplate,
    PageTemplate,
    UpdatePageTemplate,
)
from ..base_resource import BaseResource


class WorkspacePageTemplates(BaseResource):
    """API client for managing workspace-level page templates."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str) -> list[PageTemplate]:
        """List all page templates in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
        """
        response = self._get(f"{workspace_slug}/pages/templates/")
        return [PageTemplate.model_validate(item) for item in response]

    def create(self, workspace_slug: str, data: CreatePageTemplate) -> PageTemplate:
        """Create a new page template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Page template data
        """
        response = self._post(
            f"{workspace_slug}/pages/templates/",
            data.model_dump(exclude_none=True),
        )
        return PageTemplate.model_validate(response)

    def update(
        self, workspace_slug: str, template_id: str, data: UpdatePageTemplate
    ) -> PageTemplate:
        """Update a page template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            template_id: UUID of the template
            data: Updated template data
        """
        response = self._patch(
            f"{workspace_slug}/pages/templates/{template_id}/",
            data.model_dump(exclude_none=True),
        )
        return PageTemplate.model_validate(response)

    def delete(self, workspace_slug: str, template_id: str) -> None:
        """Delete a page template in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            template_id: UUID of the template
        """
        return self._delete(f"{workspace_slug}/pages/templates/{template_id}/")
