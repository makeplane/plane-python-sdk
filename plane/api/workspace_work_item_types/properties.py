from typing import Any

from ...models.work_item_properties import WorkItemProperty
from ...models.work_item_types import WorkspaceWorkItemTypePropertyLink
from ..base_resource import BaseResource


class WorkspaceWorkItemTypeProperties(BaseResource):
    """API client for managing property links on workspace-level work item types."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, type_id: str) -> list[str]:
        """List property UUIDs linked to a workspace work item type.

        The API returns a flat list of UUID strings, not full property objects.
        To get full WorkItemProperty objects, resolve these UUIDs via
        workspace_work_item_properties.list() or .retrieve().

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the work item type
        """
        response = self._get(
            f"{workspace_slug}/work-item-types/{type_id}/properties/"
        )
        return list(response)

    def create(
        self, workspace_slug: str, type_id: str, data: WorkspaceWorkItemTypePropertyLink
    ) -> None:
        """Link one or more properties to a workspace work item type.
        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the work item type
            data: DTO containing properties (list of UUIDs) to link
        """
        self._post(
            f"{workspace_slug}/work-item-types/{type_id}/properties/",
            data.model_dump(exclude_none=True),
        )

    def delete(self, workspace_slug: str, type_id: str, property_id: str) -> None:
        """Unlink a property from a workspace work item type.

        Args:
            workspace_slug: The workspace slug identifier
            type_id: UUID of the work item type
            property_id: UUID of the property to unlink
        """
        return self._delete(
            f"{workspace_slug}/work-item-types/{type_id}/properties/{property_id}/"
        )
