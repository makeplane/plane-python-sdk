from collections.abc import Mapping
from typing import Any

from ..models.labels import CreateLabel, Label, PaginatedLabelResponse, UpdateLabel
from .base_resource import BaseResource


class Labels(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, project_id: str, data: CreateLabel) -> Label:
        """Create a new label.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            data: Label data
        """
        response = self._post(
            f"{workspace_slug}/projects/{project_id}/labels",
            data.model_dump(exclude_none=True),
        )
        return Label.model_validate(response)

    def retrieve(self, workspace_slug: str, project_id: str, label_id: str) -> Label:
        """Retrieve a label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            label_id: UUID of the label
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/labels/{label_id}")
        return Label.model_validate(response)

    def update(
        self, workspace_slug: str, project_id: str, label_id: str, data: UpdateLabel
    ) -> Label:
        """Update a label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            label_id: UUID of the label
            data: Updated label data
        """
        response = self._patch(
            f"{workspace_slug}/projects/{project_id}/labels/{label_id}",
            data.model_dump(exclude_none=True),
        )
        return Label.model_validate(response)

    def delete(self, workspace_slug: str, project_id: str, label_id: str) -> None:
        """Delete a label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            label_id: UUID of the label
        """
        return self._delete(f"{workspace_slug}/projects/{project_id}/labels/{label_id}")

    def list(
        self, workspace_slug: str, project_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedLabelResponse:
        """List labels with optional filtering parameters.

        Args:
            workspace_slug: The workspace slug identifier
            project_id: UUID of the project
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/projects/{project_id}/labels", params=params)
        return PaginatedLabelResponse.model_validate(response)
