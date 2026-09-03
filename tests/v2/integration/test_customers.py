"""Live coverage for `client.v2.workspace(slug).customers`, plus its nested
`requests` and `property_values` sub-resources; skips (never fails) when
required env vars are absent, same convention as every other file here."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.customers import Customers
from plane.client import PlaneClient
from plane.models.v2.customers import (
    CreateCustomer,
    CreateCustomerPropertyValues,
    CreateCustomerRequest,
    UpdateCustomer,
    UpdateCustomerRequest,
)
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name


@pytest.fixture(scope="module")
def customers(client: PlaneClient, workspace_slug: str) -> Customers:
    return client.v2.workspace(workspace_slug).customers


@pytest.fixture(scope="module")
def customer(customers: Customers) -> Iterator[Any]:
    """One customer shared by every test in this module."""
    created = customers.create(CreateCustomer(name=unique_name("customer")))
    yield created
    try:
        customers.delete(created.id)
    except Exception:
        pass


class TestCustomers:
    def test_crud(self, customers: Customers, customer: Any) -> None:
        fetched = customers.retrieve(customer.id)
        assert fetched.id == customer.id

        page = customers.list()
        assert any(c.id == customer.id for c in page.data)

        updated = customers.update(customer.id, UpdateCustomer(stage="onboarding"))
        assert updated.stage == "onboarding"

    def test_upsert_creates_then_reconciles(self, customers: Customers) -> None:
        marker = unique_name("customer-upsert")
        first = customers.upsert(
            CreateCustomer(name=marker, external_id=marker, external_source="sdk-it")
        )
        try:
            second = customers.upsert(
                CreateCustomer(
                    name=marker, external_id=marker, external_source="sdk-it", stage="active"
                )
            )
            assert second.id == first.id
            assert second.stage == "active"
        finally:
            customers.delete(first.id)

    def test_find_by_name(self, customers: Customers, customer: Any) -> None:
        assert customers.find_by_name(customer.name).id == customer.id

    def test_work_items_add_then_remove(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        customers: Customers,
        customer: Any,
    ) -> None:
        work_items = client.v2.workspace(workspace_slug).project(project_id).work_items
        work_item = work_items.create(CreateWorkItem(name=unique_name("wi-customer-link")))
        try:
            added = customers.work_items.add(customer.id, [work_item.id])
            assert work_item.id in added

            removed = customers.work_items.remove(customer.id, [work_item.id])
            assert work_item.id in removed
        finally:
            work_items.delete(work_item.id)

    def test_requests_crud(self, customers: Customers, customer: Any) -> None:
        created = customers.requests.create(
            customer.id, CreateCustomerRequest(name=unique_name("request"))
        )
        try:
            fetched = customers.requests.retrieve(customer.id, created.id)
            assert fetched.id == created.id

            page = customers.requests.list(customer.id)
            assert any(r.id == created.id for r in page.data)

            updated = customers.requests.update(
                customer.id, created.id, UpdateCustomerRequest(link="https://x.test")
            )
            assert updated.link == "https://x.test"
        finally:
            customers.requests.delete(customer.id, created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            customers.requests.retrieve(customer.id, created.id)
        assert exc_info.value.status == 404

    def test_property_values_list_is_empty_map_for_a_fresh_customer(
        self, customers: Customers, customer: Any
    ) -> None:
        values = customers.property_values.list(customer.id)
        assert values.model_dump() == {}

    def test_property_values_create_against_an_existing_customer_property(
        self, client: PlaneClient, workspace_slug: str, customers: Customers, customer: Any
    ) -> None:
        """Bulk-set requires an existing customer property id; this workspace may
        have none provisioned (customer properties are a separate resource, covered
        by `test_customer_properties.py`) -- skip rather than fail if so."""
        properties = client.v2.transport.request(
            "GET", f"/workspaces/{workspace_slug}/customer-properties/"
        )
        rows = properties.get("data", []) if isinstance(properties, dict) else []
        if not rows:
            pytest.skip("no customer properties provisioned in this workspace")
        property_id = rows[0]["id"]

        customers.property_values.create(
            customer.id, CreateCustomerPropertyValues(values={property_id: ["test-value"]})
        )

        values = customers.property_values.list(customer.id)
        assert values.model_dump().get(property_id) == ["test-value"]
