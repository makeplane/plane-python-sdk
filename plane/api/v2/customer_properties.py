"""Customer properties (api_v2) -- custom-field definitions on the Customer object.
Flat CRUD; no bulk or upsert (the golden offers neither for this resource)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.customer_properties import (
    CreateCustomerProperty,
    CustomerProperty,
    UpdateCustomerProperty,
)
from ._generated.constants import (
    CustomerPropertiesCreateField,
    CustomerPropertiesListField,
    CustomerPropertiesListFilters,
    CustomerPropertiesListOrderBy,
    CustomerPropertiesPartialUpdateField,
    CustomerPropertiesRetrieveField,
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
        slug: str,
        *,
        fields: Sequence[CustomerPropertiesListField] | None = None,
        order_by: CustomerPropertiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[CustomerPropertiesListFilters],
    ) -> Page[CustomerProperty]:
        """One page of customer properties. `**filters` covers the golden's query
        filters directly, e.g. `is_active=True`, `property_type="OPTION"`,
        `name="Tier"`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[CustomerPropertiesListField] | None = None,
        order_by: CustomerPropertiesListOrderBy | None = None,
        **filters: Unpack[CustomerPropertiesListFilters],
    ) -> Iterator[CustomerProperty]:
        """Every customer property, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        property_id: str,
        *,
        fields: Sequence[CustomerPropertiesRetrieveField] | None = None,
    ) -> CustomerProperty:
        return self._retrieve(pk=property_id, params={"fields": fields}, slug=slug)

    def find_by_name(self, slug: str, name: str) -> CustomerProperty:
        """The one customer property with this name; raises if none or several
        match. `name` is the slugified machine key."""
        return self._find_one(filters={"name": name}, slug=slug)

    def find_by_display_name(self, slug: str, display_name: str) -> CustomerProperty:
        """The one customer property with this display name; raises if none or
        several match. `display_name` is the label a user sees in the UI."""
        return self._find_one(filters={"display_name": display_name}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateCustomerProperty,
        *,
        fields: Sequence[CustomerPropertiesCreateField] | None = None,
    ) -> CustomerProperty:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        property_id: str,
        data: UpdateCustomerProperty,
        *,
        fields: Sequence[CustomerPropertiesPartialUpdateField] | None = None,
    ) -> CustomerProperty:
        return self._update(data, pk=property_id, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, property_id: str) -> None:
        return self._delete(pk=property_id, slug=slug)
