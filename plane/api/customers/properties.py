from collections.abc import Mapping
from typing import Any

from ..base_resource import BaseResource


class CustomerProperties(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """List customer properties in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customer-properties", params=params)
        return response if isinstance(response, list) else []

    def retrieve(self, workspace_slug: str, property_id: str) -> dict[str, Any]:
        """Retrieve a customer property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the customer property
        """
        response = self._get(f"{workspace_slug}/customer-properties/{property_id}")
        return response if isinstance(response, dict) else {}

    def create(self, workspace_slug: str, data: Mapping[str, Any]) -> dict[str, Any]:
        """Create a new customer property.

        Args:
            workspace_slug: The workspace slug identifier
            data: Customer property data
        """
        response = self._post(f"{workspace_slug}/customer-properties", data)
        return response if isinstance(response, dict) else {}

    def update(
        self, workspace_slug: str, property_id: str, data: Mapping[str, Any]
    ) -> dict[str, Any]:
        """Update a customer property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the customer property
            data: Updated property data
        """
        response = self._patch(f"{workspace_slug}/customer-properties/{property_id}", data)
        return response if isinstance(response, dict) else {}

    def delete(self, workspace_slug: str, property_id: str) -> None:
        """Delete a customer property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the customer property
        """
        return self._delete(f"{workspace_slug}/customer-properties/{property_id}")
