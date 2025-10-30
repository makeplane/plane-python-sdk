from collections.abc import Mapping
from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import (
    CustomerRequest,
    UpdateCustomerRequest,
)


class CustomerRequests(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self,
        workspace_slug: str,
        customer_id: str,
        params: Mapping[str, Any] | None = None,
    ) -> list[CustomerRequest]:
        """List customer requests.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}/requests", params=params)
        if isinstance(response, list):
            return [CustomerRequest.model_validate(item) for item in response]
        return []

    def retrieve(self, workspace_slug: str, customer_id: str, request_id: str) -> CustomerRequest:
        """Retrieve a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}/requests/{request_id}")
        return CustomerRequest.model_validate(response)

    def create(
        self, workspace_slug: str, customer_id: str, data: CustomerRequest
    ) -> CustomerRequest:
        """Create a new customer request.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            data: Customer request data
        """
        response = self._post(
            f"{workspace_slug}/customers/{customer_id}/requests",
            data.model_dump(exclude_none=True),
        )
        return CustomerRequest.model_validate(response)

    def update(
        self,
        workspace_slug: str,
        customer_id: str,
        request_id: str,
        data: UpdateCustomerRequest,
    ) -> CustomerRequest:
        """Update a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
            data: Updated request data
        """
        response = self._patch(
            f"{workspace_slug}/customers/{customer_id}/requests/{request_id}",
            data.model_dump(exclude_none=True),
        )
        return CustomerRequest.model_validate(response)

    def delete(self, workspace_slug: str, customer_id: str, request_id: str) -> None:
        """Delete a customer request by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            request_id: UUID of the customer request
        """
        return self._delete(f"{workspace_slug}/customers/{customer_id}/requests/{request_id}")
