"""Customers (api_v2) -- workspace-scoped, unlike states/labels/work items.
Customer/work-item membership is the `.work_items` bridge (`add`/`remove`)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.customers import CreateCustomer, Customer, UpdateCustomer
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .property_values import CustomerPropertyValues
from .requests import CustomerRequests
from .work_items import CustomerWorkItems

__all__ = ["Customers", "CustomerPropertyValues", "CustomerRequests", "CustomerWorkItems"]


class Customers(V2Resource[Customer, CreateCustomer, UpdateCustomer]):
    path = "/workspaces/{slug}/customers/"
    model = Customer
    operations = {
        "list": "customers_list",
        "retrieve": "customers_retrieve",
        "create": "customers_create",
        "update": "customers_partial_update",
        "upsert": "customers_upsert",
        "delete": "customers_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.requests = CustomerRequests(transport, **self._scope)
        self.property_values = CustomerPropertyValues(transport, **self._scope)
        self.work_items = CustomerWorkItems(transport, **self._scope)

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[Customer]:
        """One page of customers in a workspace.

        `**filters` covers `name`, `domain`, `stage`, `contract_status`, `search`."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[Customer]:
        """Every customer in a workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, customer_id: str, *, fields: Sequence[str] | None = None) -> Customer:
        return self._retrieve(pk=customer_id, params={"fields": fields})

    def find_by_name(self, name: str) -> Customer:
        """The one customer with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateCustomer) -> Customer:
        return self._create(data)

    def update(self, customer_id: str, data: UpdateCustomer) -> Customer:
        return self._update(data, pk=customer_id)

    def delete(self, customer_id: str) -> None:
        return self._delete(pk=customer_id)

    def upsert(self, data: CreateCustomer) -> Customer:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)
