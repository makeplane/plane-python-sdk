from __future__ import annotations

from typing import Any

from plane.api.base_resource import BaseResource
from plane.models.customers import (
    SetCustomerPropertyValue,
    SetCustomerPropertyValues,
)


class CustomerPropertyValues(BaseResource):
    """API resource for the values a customer holds for its properties.

    Values are addressed as a mapping of property id to a list of strings, for
    every property type — dates as ``YYYY-MM-DD``, booleans as ``"True"`` /
    ``"False"``, options and relations as UUIDs. Properties that are not
    ``is_active`` are left out of reads.

    Writes replace the values of the properties they name, rather than merging
    into them. Properties absent from the payload keep their current values.
    """

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

    def list(self, workspace_slug: str, customer_id: str) -> dict[str, list[str]]:
        """Retrieve every property value set on a customer.

        Properties that have no value set are absent from the mapping.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer

        Returns:
            Property id mapped to that property's values
        """
        response = self._get(f"{workspace_slug}/customers/{customer_id}/property-values")
        return response or {}

    def set(
        self,
        workspace_slug: str,
        customer_id: str,
        data: SetCustomerPropertyValues,
    ) -> None:
        """Set several of a customer's property values at once.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            data: Property ids mapped to their new values

        Raises:
            HttpError: 400 if a value fails its property's validation
        """
        self._post(
            f"{workspace_slug}/customers/{customer_id}/property-values",
            data.model_dump(exclude_none=True),
        )

    def retrieve(self, workspace_slug: str, customer_id: str, property_id: str) -> list[str]:
        """Retrieve the values a customer holds for one property.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            property_id: UUID of the customer property

        Returns:
            The property's values, empty when none are set

        Raises:
            HttpError: 404 if the customer or property does not exist
        """
        response = self._get(
            f"{workspace_slug}/customers/{customer_id}/property-values/{property_id}"
        )
        return (response or {}).get(str(property_id), [])

    def update(
        self,
        workspace_slug: str,
        customer_id: str,
        property_id: str,
        data: SetCustomerPropertyValue,
    ) -> None:
        """Replace the values a customer holds for one property.

        Args:
            workspace_slug: The workspace slug identifier
            customer_id: UUID of the customer
            property_id: UUID of the customer property
            data: The property's new values

        Raises:
            HttpError: 400 if the property is required and the values are empty,
                or if a value fails the property's validation
            HttpError: 404 if the customer or property does not exist
        """
        self._patch(
            f"{workspace_slug}/customers/{customer_id}/property-values/{property_id}",
            data.model_dump(exclude_none=True),
        )
