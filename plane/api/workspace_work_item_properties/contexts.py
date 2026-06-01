from typing import Any

from ...models.work_item_property_context import (
    CreateWorkItemPropertyContext,
    UpdateWorkItemPropertyContext,
    WorkItemPropertyContext,
)
from ..base_resource import BaseResource


class WorkspaceWorkItemPropertyContexts(BaseResource):
    """API client for managing contexts on workspace-level work item properties."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, property_id: str
    ) -> list[WorkItemPropertyContext]:
        """List all contexts for a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
        """
        response = self._get(
            f"{workspace_slug}/work-item-properties/{property_id}/contexts/"
        )
        return [WorkItemPropertyContext.model_validate(item) for item in response]

    def create(
        self,
        workspace_slug: str,
        property_id: str,
        data: CreateWorkItemPropertyContext,
    ) -> WorkItemPropertyContext:
        """Create a new context for a workspace work item property.

        Non-default contexts must specify at least one project and one issue type
        (unless the corresponding applies_to_all_* flag is set).

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            data: Context data
        """
        response = self._post(
            f"{workspace_slug}/work-item-properties/{property_id}/contexts/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyContext.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        property_id: str,
        context_id: str,
        data: UpdateWorkItemPropertyContext,
    ) -> WorkItemPropertyContext:
        """Update a context for a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            context_id: UUID of the context
            data: Updated context data
        """
        response = self._patch(
            f"{workspace_slug}/work-item-properties/{property_id}/contexts/{context_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyContext.model_validate(response)

    def retrieve(
        self, workspace_slug: str, property_id: str, context_id: str
    ) -> WorkItemPropertyContext:
        """Retrieve a single context for a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            context_id: UUID of the context
        """
        response = self._get(
            f"{workspace_slug}/work-item-properties/{property_id}/contexts/{context_id}/"
        )
        return WorkItemPropertyContext.model_validate(response)

    def delete(
        self, workspace_slug: str, property_id: str, context_id: str
    ) -> None:
        """Delete a context from a workspace work item property.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the work item property
            context_id: UUID of the context
        """
        return self._delete(
            f"{workspace_slug}/work-item-properties/{property_id}/contexts/{context_id}/"
        )
