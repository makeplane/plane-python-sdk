from collections.abc import Iterable, Mapping
from typing import Any

from ...models.initiatives import (
    CreateInitiativeLabel,
    InitiativeLabel,
    PaginatedInitiativeLabelResponse,
    UpdateInitiativeLabel,
)
from ..base_resource import BaseResource


class InitiativeLabels(BaseResource):
    """API client for managing labels associated with initiatives."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def create(self, workspace_slug: str, data: CreateInitiativeLabel) -> InitiativeLabel:
        """Create a new initiative label in the workspace.

        Args:
            workspace_slug: The workspace slug identifier
            data: Initiative label data

        Returns:
            The created initiative label
        """
        response = self._post(
            f"{workspace_slug}/initiatives/labels",
            data.model_dump(exclude_none=True),
        )
        return InitiativeLabel.model_validate(response)

    def retrieve(self, workspace_slug: str, label_id: str) -> InitiativeLabel:
        """Retrieve an initiative label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the initiative label

        Returns:
            The requested initiative label
        """
        response = self._get(f"{workspace_slug}/initiatives/labels/{label_id}")
        return InitiativeLabel.model_validate(response)

    def update(
        self, workspace_slug: str, label_id: str, data: UpdateInitiativeLabel
    ) -> InitiativeLabel:
        """Update an initiative label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the initiative label
            data: Updated initiative label data

        Returns:
            The updated initiative label
        """
        response = self._patch(
            f"{workspace_slug}/initiatives/labels/{label_id}",
            data.model_dump(exclude_none=True),
        )
        return InitiativeLabel.model_validate(response)

    def delete(self, workspace_slug: str, label_id: str) -> None:
        """Delete an initiative label by ID.

        Args:
            workspace_slug: The workspace slug identifier
            label_id: UUID of the initiative label
        """
        return self._delete(f"{workspace_slug}/initiatives/labels/{label_id}")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedInitiativeLabelResponse:
        """List initiative labels in the workspace with optional filtering.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters (e.g., per_page, cursor)

        Returns:
            Paginated list of initiative labels
        """
        response = self._get(f"{workspace_slug}/initiatives/labels", params=params)
        return PaginatedInitiativeLabelResponse.model_validate(response)

    def list_labels(
        self, workspace_slug: str, initiative_id: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedInitiativeLabelResponse:
        """List labels associated with an initiative.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            params: Optional query parameters (e.g., per_page, cursor)

        Returns:
            Paginated list of initiative labels
        """
        response = self._get(f"{workspace_slug}/initiatives/{initiative_id}/labels", params=params)
        return PaginatedInitiativeLabelResponse.model_validate(response)

    def add_labels(
        self, workspace_slug: str, initiative_id: str, label_ids: Iterable[str]
    ) -> Iterable[InitiativeLabel]:
        """Add labels to an initiative.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            label_ids: List of label UUIDs to add

        Returns:
            List of added initiative labels
        """
        response = self._post(
            f"{workspace_slug}/initiatives/{initiative_id}/labels",
            {"label_ids": label_ids},
        )
        return [InitiativeLabel.model_validate(label) for label in response]

    def remove_labels(
        self, workspace_slug: str, initiative_id: str, label_ids: Iterable[str]
    ) -> None:
        """Remove labels from an initiative.

        Args:
            workspace_slug: The workspace slug identifier
            initiative_id: UUID of the initiative
            label_ids: List of label UUIDs to remove
        """
        return self._delete(
            f"{workspace_slug}/initiatives/{initiative_id}/labels",
            {"label_ids": label_ids},
        )
