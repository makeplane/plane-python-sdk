"""Customer properties (api_v2) -- custom-field definitions on the Customer object.
Flat CRUD; no bulk or upsert (the golden offers neither for this resource)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.customer_properties import (
    CreateCustomerProperty,
    CustomerProperty,
    UpdateCustomerProperty,
)
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


class CustomerProperties(
    V2Resource[CustomerProperty, CreateCustomerProperty, UpdateCustomerProperty]
):
    path = "/workspaces/{slug}/customer-properties/"
    model = CustomerProperty
    operations = {
        "list": "customer_properties_list",
        "retrieve": "customer_properties_retrieve",
        "create": "customer_properties_create",
        "update": "customer_properties_partial_update",
        "delete": "customer_properties_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[CustomerProperty]:
        """One page of customer properties. `**filters` covers the golden's query
        filters directly, e.g. `is_active=True`, `property_type="OPTION"`,
        `name="Tier"`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[CustomerProperty]:
        """Every customer property, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        property_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> CustomerProperty:
        return self._retrieve(pk=property_id, params={"fields": fields})

    def find_by_name(self, name: str) -> CustomerProperty:
        """The one customer property with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateCustomerProperty) -> CustomerProperty:
        return self._create(data)

    def update(self, property_id: str, data: UpdateCustomerProperty) -> CustomerProperty:
        return self._update(data, pk=property_id)

    def delete(self, property_id: str) -> None:
        return self._delete(pk=property_id)
