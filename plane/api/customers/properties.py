from collections.abc import Mapping
from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import (
    CreateCustomerProperty,
    CustomerProperty,
    PaginatedCustomerPropertyResponse,
    UpdateCustomerProperty,
)


class CustomerProperties(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(
        self, workspace_slug: str, params: Mapping[str, Any] | None = None
    ) -> PaginatedCustomerPropertyResponse:
        """List customer properties in a workspace.

        Args:
            workspace_slug: The workspace slug identifier
            params: Optional query parameters
        """
        response = self._get(f"{workspace_slug}/customer-properties", params=params)
        return PaginatedCustomerPropertyResponse.model_validate(response)

    def retrieve(self, workspace_slug: str, property_id: str) -> CustomerProperty:
        """Retrieve a customer property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the customer property
        """
        response = self._get(f"{workspace_slug}/customer-properties/{property_id}")
        return CustomerProperty.model_validate(response)

    def create(self, workspace_slug: str, data: CreateCustomerProperty) -> CustomerProperty:
        """Create a new customer property.

        Args:
            workspace_slug: The workspace slug identifier
            data: Customer property data
        """
        response = self._post(
            f"{workspace_slug}/customer-properties", data.model_dump(exclude_none=True)
        )
        return CustomerProperty.model_validate(response)

    def update(
        self, workspace_slug: str, property_id: str, data: UpdateCustomerProperty
    ) -> CustomerProperty:
        """Update a customer property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the customer property
            data: Updated property data
        """
        response = self._patch(
            f"{workspace_slug}/customer-properties/{property_id}",
            data.model_dump(exclude_none=True),
        )
        return CustomerProperty.model_validate(response)

    def delete(self, workspace_slug: str, property_id: str) -> None:
        """Delete a customer property by ID.

        Args:
            workspace_slug: The workspace slug identifier
            property_id: UUID of the customer property
        """
        return self._delete(f"{workspace_slug}/customer-properties/{property_id}")
