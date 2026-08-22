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

    def list(self, customer_id: str) -> CustomerPropertyValueMap:
        """Every property value set on a customer, keyed by property id.
        Properties with no value set are absent from the mapping."""
        payload = self.transport.request(
            "GET", self._collection_url(customer_id=customer_id)
        )
        return self.model.model_validate(payload)

    def create(self, customer_id: str, data: CreateCustomerPropertyValues) -> None:
        """Bulk-set several of a customer's property values at once (upsert;
        properties absent from `data.values` are untouched)."""
        self.transport.request(
            "POST",
            self._collection_url(customer_id=customer_id),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return None
