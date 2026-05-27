from typing import Any

from ..models.work_item_relation_definitions import (
    CreateWorkItemRelationDefinition,
    UpdateWorkItemRelationDefinition,
    WorkItemRelationDefinition,
)
from .base_resource import BaseResource


class WorkItemRelationDefinitions(BaseResource):
    """API client for managing workspace-level work item relation definitions."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        is_default: bool | None = None,
        is_active: bool | None = None,
    ) -> list[WorkItemRelationDefinition]:
        """List all work item relation definitions in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            is_default: Optional filter by default status
            is_active: Optional filter by active status
        """
        params: dict[str, Any] = {}
        if is_default is not None:
            params["is_default"] = str(is_default).lower()
        if is_active is not None:
            params["is_active"] = str(is_active).lower()

        response = self._get(
            f"{workspace_slug}/work-item-relation-definitions/",
            params=params if params else None,
        )
        return [WorkItemRelationDefinition.model_validate(item) for item in response]

    def create(
        self, workspace_slug: str, data: CreateWorkItemRelationDefinition
    ) -> WorkItemRelationDefinition:
        """Create a new work item relation definition in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Relation definition data
        """
        response = self._post(
            f"{workspace_slug}/work-item-relation-definitions/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemRelationDefinition.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        definition_id: str,
        data: UpdateWorkItemRelationDefinition,
    ) -> WorkItemRelationDefinition:
        """Update a work item relation definition in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            definition_id: UUID of the relation definition
            data: Updated relation definition data
        """
        response = self._patch(
            f"{workspace_slug}/work-item-relation-definitions/{definition_id}/",
            data.model_dump(exclude_none=True),
        )
        return WorkItemRelationDefinition.model_validate(response)

    def delete(self, workspace_slug: str, definition_id: str) -> None:
        """Delete a work item relation definition in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            definition_id: UUID of the relation definition
        """
        return self._delete(
            f"{workspace_slug}/work-item-relation-definitions/{definition_id}/"
        )
