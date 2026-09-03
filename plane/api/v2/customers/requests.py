"""Customer requests (api_v2). `work_item_ids` on `CreateCustomerRequest`/
`UpdateCustomerRequest` links the request to work items but is write-only,
not echoed back on `CustomerRequest`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.customers import CreateCustomerRequest, CustomerRequest, UpdateCustomerRequest
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class CustomerRequests(V2Resource[CustomerRequest, CreateCustomerRequest, UpdateCustomerRequest]):
    path = "/workspaces/{slug}/customers/{customer_id}/requests/"
    model = CustomerRequest
    operations = {
        "list": "customer_requests_list",
        "retrieve": "customer_requests_retrieve",
        "create": "customer_requests_create",
        "update": "customer_requests_partial_update",
        "delete": "customer_requests_destroy",
    }

    def list(
        self,
        customer_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[CustomerRequest]:
        """One page of requests raised by a customer."""
        return self._list(customer_id=customer_id, params={"fields": fields, **filters})

    def iterate(
        self,
        customer_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[CustomerRequest]:
        """Every request raised by a customer, following pages automatically."""
        return self._iter(customer_id=customer_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        customer_id: str,
        pk: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> CustomerRequest:
        return self._retrieve(pk=pk, customer_id=customer_id, params={"fields": fields})

    def create(self, customer_id: str, data: CreateCustomerRequest) -> CustomerRequest:
        return self._create(data, customer_id=customer_id)

    def update(self, customer_id: str, pk: str, data: UpdateCustomerRequest) -> CustomerRequest:
        return self._update(data, pk=pk, customer_id=customer_id)

    def delete(self, customer_id: str, pk: str) -> None:
        return self._delete(pk=pk, customer_id=customer_id)
