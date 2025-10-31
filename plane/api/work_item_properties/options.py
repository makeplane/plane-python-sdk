from collections.abc import Mapping
from typing import Any

from ...models.work_item_properties import (
    CreateWorkItemPropertyOption,
    UpdateWorkItemPropertyOption,
    WorkItemPropertyOption,
)
from ..base_resource import BaseResource


class WorkItemPropertyOptions(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        project_id: str,
        property_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[WorkItemPropertyOption]:
        """List work item property options.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the work item property
            params: Optional query parameters
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}/options",
            params=params,
        )
        return [WorkItemPropertyOption.model_validate(item) for item in response]

    def retrieve(
        self, workspace_slug: str, project_id: str, property_id: str, option_id: str
    ) -> WorkItemPropertyOption:
        """Retrieve a work item property option.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the work item property
            option_id: UUID of the option
        """
        response = self._get(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}/options/{option_id}"
        )
        return WorkItemPropertyOption.model_validate(response)

    def create(
        self,
        workspace_slug: str,
        project_id: str,
        property_id: str,
        data: CreateWorkItemPropertyOption,
    ) -> WorkItemPropertyOption:
        """Create a new work item property option.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the work item property
            data: Option data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}/options",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyOption.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        project_id: str,
        property_id: str,
        option_id: str,
        data: UpdateWorkItemPropertyOption,
    ) -> WorkItemPropertyOption:
        """Update a work item property option.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the work item property
            option_id: UUID of the option
            data: Updated option data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}/options/{option_id}",
            data.model_dump(exclude_none=True),
        )
        return WorkItemPropertyOption.model_validate(response)

    def delete(
        self, workspace_slug: str, project_id: str, property_id: str, option_id: str
    ) -> None:
        """Delete a work item property option.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            property_id: UUID of the work item property
            option_id: UUID of the option
        """
        return self._delete(
            f"{workspace_slug}/projects/{project_id}/work-item-properties/{property_id}/options/{option_id}"
        )
