from collections.abc import Mapping
from typing import Any

from ..base_resource import BaseResource
from .properties import CustomerProperties
from .requests import CustomerRequests


class Customers(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.properties = CustomerProperties(config)
        self.requests = CustomerRequests(config)

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        """List customers in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customers", params=params)
        return response if isinstance(response, list) else []

    def retrieve(
        self, workspace_slug: str, customer_id: str, params: Mapping[str, Any] | None = None
    ) -> dict[str, Any]:
        """Retrieve a customer by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}", params=params)
        return response if isinstance(response, dict) else {}

    def create(self, workspace_slug: str, data: Mapping[str, Any]) -> dict[str, Any]:
        """Create a new customer.

        Args:
            workspace_slug: The workspace slug identifier
            data: Customer data
        """
        response = self._post(f"{workspace_slug}/customers", data)
        return response if isinstance(response, dict) else {}

    def update(
        self, workspace_slug: str, customer_id: str, data: Mapping[str, Any]
    ) -> dict[str, Any]:
        """Update a customer by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            data: Updated customer data
        """
        response = self._patch(f"{workspace_slug}/customers/{customer_id}", data)
        return response if isinstance(response, dict) else {}

    def delete(self, workspace_slug: str, customer_id: str) -> None:
        """Delete a customer by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
        """
        return self._delete(f"{workspace_slug}/customers/{customer_id}")
