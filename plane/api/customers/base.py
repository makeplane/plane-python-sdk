from collections.abc import Mapping
from typing import Any

from plane.api.base_resource import BaseResource
from plane.api.customers.properties import CustomerProperties
from plane.api.customers.requests import CustomerRequests
from plane.models.customers import (
    CreateCustomer,
    Customer,
    PaginatedCustomerResponse,
    UpdateCustomer,
)


class Customers(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.properties = CustomerProperties(config)
        self.requests = CustomerRequests(config)

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedCustomerResponse:
        """List customers in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customers", params=params)
        return PaginatedCustomerResponse.model_validate(response)

    def retrieve(
        self, workspace_slug: str, customer_id: str, params: Mapping[str, Any] | None = None
    ) -> Customer:
        """Retrieve a customer by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}", params=params)
        return Customer.model_validate(response)

    def create(self, workspace_slug: str, data: CreateCustomer) -> Customer:
        """Create a new customer.

        Args:
            workspace_slug: The workspace slug identifier
            data: Customer data
        """
        response = self._post(f"{workspace_slug}/customers", data.model_dump(exclude_none=True))
        return Customer.model_validate(response)

    def update(self, workspace_slug: str, customer_id: str, data: UpdateCustomer) -> Customer:
        """Update a customer by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            data: Updated customer data
        """
        response = self._patch(
            f"{workspace_slug}/customers/{customer_id}", data.model_dump(exclude_none=True)
        )
        return Customer.model_validate(response)

    def delete(self, workspace_slug: str, customer_id: str) -> None:
        """Delete a customer by ID.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
        """
        return self._delete(f"{workspace_slug}/customers/{customer_id}")
