"""Customers (api_v2) -- workspace-scoped, unlike states/labels/work items.
Customer/work-item membership is the `.work_items` bridge (`add`/`remove`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.customers import CreateCustomer, Customer, UpdateCustomer
from .._generated.constants import (
    CustomersCreateField,
    CustomersListField,
    CustomersListFilters,
    CustomersListOrderBy,
    CustomersPartialUpdateField,
    CustomersRetrieveField,
    CustomersUpsertField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.customer import LoadedCustomer
from .property_values import CustomerPropertyValues
from .requests import CustomerRequests
from .work_items import CustomerWorkItems

__all__ = ["Customers", "CustomerPropertyValues", "CustomerRequests", "CustomerWorkItems"]


class Customers(
    V2Resource[Customer, CreateCustomer, UpdateCustomer], LoadsNavigableRows[LoadedCustomer]
):
    path = "/workspaces/{slug}/customers/"
    model = Customer
    loaded_model = LoadedCustomer
    loaded_names = ("slug", "customer")
    operations = {
        "list": "customers_list",
        "retrieve": "customers_retrieve",
        "create": "customers_create",
        "update": "customers_partial_update",
        "upsert": "customers_upsert",
        "delete": "customers_destroy",
    }

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.requests = CustomerRequests(transport)
        self.property_values = CustomerPropertyValues(transport)
        self.work_items = CustomerWorkItems(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[CustomersListField] | None = None,
        order_by: CustomersListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[CustomersListFilters],
    ) -> Page[LoadedCustomer]:
        """One page of customers in a workspace.

        `**filters` covers `name`, `domain`, `stage`, `contract_status`, `search`."""
        page = self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[CustomersListField] | None = None,
        order_by: CustomersListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[CustomersListFilters],
    ) -> Iterator[LoadedCustomer]:
        """Every customer in a workspace, following pages automatically."""
        rows = self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        customer: str,
        *,
        fields: Sequence[CustomersRetrieveField] | None = None,
    ) -> LoadedCustomer:
        row = self._retrieve(pk=customer, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedCustomer:
        """The one customer with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def create(
        self,
        slug: str,
        data: CreateCustomer,
        *,
        fields: Sequence[CustomersCreateField] | None = None,
    ) -> LoadedCustomer:
        row = self._create(data, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def update(
        self,
        slug: str,
        customer: str,
        data: UpdateCustomer,
        *,
        fields: Sequence[CustomersPartialUpdateField] | None = None,
    ) -> LoadedCustomer:
        row = self._update(data, pk=customer, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, customer: str) -> None:
        return self._delete(pk=customer, slug=slug)

    def upsert(
        self,
        slug: str,
        data: CreateCustomer,
        *,
        fields: Sequence[CustomersUpsertField] | None = None,
    ) -> LoadedCustomer:
        """Reconciles on (external_source, external_id) when both are set."""
        row = self._upsert(data, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)
