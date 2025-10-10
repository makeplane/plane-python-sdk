from collections.abc import Mapping
from typing import Any

from ..base_resource import BaseResource


class CustomerRequests(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        customer_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """List customer requests.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}/requests", params=params)
        return response if isinstance(response, list) else []

    def retrieve(self, workspace_slug: str, customer_id: str, request_id: str) -> dict[str, Any]:
        """Retrieve a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}/requests/{request_id}")
        return response if isinstance(response, dict) else {}

    def create(
        self, workspace_slug: str, customer_id: str, data: Mapping[str, Any]
    ) -> dict[str, Any]:
        """Create a new customer request.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            data: Customer request data
        """
        response = self._post(f"{workspace_slug}/customers/{customer_id}/requests", data)
        return response if isinstance(response, dict) else {}

    def update(
        self,
        workspace_slug: str,
        customer_id: str,
        request_id: str,
        data: Mapping[str, Any],
    ) -> dict[str, Any]:
        """Update a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
            data: Updated request data
        """
        response = self._patch(
            f"{workspace_slug}/customers/{customer_id}/requests/{request_id}", data
        )
        return response if isinstance(response, dict) else {}

    def delete(self, workspace_slug: str, customer_id: str, request_id: str) -> None:
        """Delete a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
        """
        return self._delete(f"{workspace_slug}/customers/{customer_id}/requests/{request_id}")
