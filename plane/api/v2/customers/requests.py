"""Customer requests (api_v2). `work_item_ids` on `CreateCustomerRequest`/
`UpdateCustomerRequest` links the request to work items but is write-only,
not echoed back on `CustomerRequest`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.customers import CreateCustomerRequest, CustomerRequest, UpdateCustomerRequest
from .._generated.constants import (
    CustomerRequestsCreateField,
    CustomerRequestsListField,
    CustomerRequestsListFilters,
    CustomerRequestsListOrderBy,
    CustomerRequestsPartialUpdateField,
    CustomerRequestsRetrieveField,
)
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
        slug: str,
        customer: str,
        *,
        fields: Sequence[CustomerRequestsListField] | None = None,
        order_by: CustomerRequestsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[CustomerRequestsListFilters],
    ) -> Page[CustomerRequest]:
        """One page of requests raised by a customer."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            customer_id=customer,
        )

    def iterate(
        self,
        slug: str,
        customer: str,
        *,
        fields: Sequence[CustomerRequestsListField] | None = None,
        order_by: CustomerRequestsListOrderBy | None = None,
        **filters: Unpack[CustomerRequestsListFilters],
    ) -> Iterator[CustomerRequest]:
        """Every request raised by a customer, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            customer_id=customer,
        )

    def retrieve(
        self,
        slug: str,
        customer: str,
        request: str,
        *,
        fields: Sequence[CustomerRequestsRetrieveField] | None = None,
    ) -> CustomerRequest:
        return self._retrieve(
            pk=request, params={"fields": fields}, slug=slug, customer_id=customer
        )

    def create(
        self,
        slug: str,
        customer: str,
        data: CreateCustomerRequest,
        *,
        fields: Sequence[CustomerRequestsCreateField] | None = None,
    ) -> CustomerRequest:
        return self._create(data, params={"fields": fields}, slug=slug, customer_id=customer)

    def update(
        self,
        slug: str,
        customer: str,
        request: str,
        data: UpdateCustomerRequest,
        *,
        fields: Sequence[CustomerRequestsPartialUpdateField] | None = None,
    ) -> CustomerRequest:
        return self._update(
            data,
            pk=request,
            params={"fields": fields},
            slug=slug,
            customer_id=customer,
        )

    def delete(self, slug: str, customer: str, request: str) -> None:
        return self._delete(pk=request, slug=slug, customer_id=customer)
