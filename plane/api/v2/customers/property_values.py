"""Customer property values (api_v2). `list`/`create` return a mapping keyed by
customer property id, not a paginated collection; no per-row retrieve/update/delete
exists (golden exposes only bulk list/set). See `WorkItemRelations` for the same shape."""

from __future__ import annotations

from ....models.v2.customers import CreateCustomerPropertyValues, CustomerPropertyValueMap
from .._kernel.resource import V2Resource


class CustomerPropertyValues(
    V2Resource[CustomerPropertyValueMap, CreateCustomerPropertyValues, CreateCustomerPropertyValues]
):
    path = "/workspaces/{slug}/customers/{customer_id}/property-values/"
    model = CustomerPropertyValueMap
    operations = {
        "list": "customer_property_values_list",
        "create": "customer_property_values_create",
    }

    def list(self, slug: str, customer: str) -> CustomerPropertyValueMap:
        """Every property value set on a customer, keyed by property id.
        Properties with no value set are absent from the mapping. GETs the
        collection URL directly -- `_retrieve_singleton` under a `list` action,
        the same URL a hand-rolled `transport.request` built, plus `_query`'s
        validation of anything the golden declares on
        `customer_property_values_list` (see `WorkItemRelations.list`)."""
        return self._retrieve_singleton(action="list", slug=slug, customer_id=customer)

    def create(self, slug: str, customer: str, data: CreateCustomerPropertyValues) -> None:
        """Bulk-set several of a customer's property values at once (upsert;
        properties absent from `data.values` are untouched). POSTs the
        collection URL directly through `_custom_request`, whose response
        envelope here is discarded rather than parsed as `self.model`."""
        self._custom_request("create", data=data, slug=slug, customer_id=customer)
        return None
