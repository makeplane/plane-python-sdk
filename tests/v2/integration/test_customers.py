"""Live coverage for `client.v2.workspaces.customers`, plus its nested `requests`,
`work_items` and `property_values` sub-resources.

Loaded rows, two deep: customers off the loaded `workspace`, and each customer's own
requests / linked work items / property values off the loaded *customer* -- so the
customer id is written once, at fetch time, and never again. The nested calls used to
read `workspace.customers.requests.create(customer.id, ...)`, which is not a route;
see `tests/v2/test_owned_sub_resources.py`."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from plane.api.v2 import LoadedCustomer, LoadedWorkspace, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.customers import (
    CreateCustomer,
    CreateCustomerPropertyValues,
    CreateCustomerRequest,
    UpdateCustomer,
    UpdateCustomerRequest,
)
from plane.models.v2.work_items import CreateWorkItem

from ._guard import skip_absent_capability
from .helpers import unique_name


@pytest.fixture(scope="module")
def customer(workspace: LoadedWorkspace) -> Iterator[LoadedCustomer]:
    """One customer shared by every test in this module, as a loaded row -- which is
    what every nested resource below is reached through."""
    created = workspace.customers.create(CreateCustomer(name=unique_name("customer")))
    yield created
    try:
        workspace.customers.delete(created.id)
    except Exception:
        pass


class TestCustomers:
    def test_crud(self, workspace: LoadedWorkspace, customer: LoadedCustomer) -> None:
        fetched = workspace.customers.retrieve(customer.id)
        assert fetched.id == customer.id

        page = workspace.customers.list()
        assert any(c.id == customer.id for c in page.data)

        updated = workspace.customers.update(customer.id, UpdateCustomer(stage="onboarding"))
        assert updated.stage == "onboarding"

    def test_upsert_creates_then_reconciles(self, workspace: LoadedWorkspace) -> None:
        marker = unique_name("customer-upsert")
        first = workspace.customers.upsert(
            CreateCustomer(name=marker, external_id=marker, external_source="sdk-it")
        )
        try:
            second = workspace.customers.upsert(
                CreateCustomer(
                    name=marker, external_id=marker, external_source="sdk-it", stage="active"
                )
            )
            assert second.id == first.id
            assert second.stage == "active"
        finally:
            workspace.customers.delete(first.id)

    def test_find_by_name(self, workspace: LoadedWorkspace, customer: LoadedCustomer) -> None:
        # Read models mark every field but `id` optional (collection reads defer
        # fields), so the name has to be narrowed rather than assumed.
        name = customer.name
        assert name is not None, "the fixture creates this customer with a name"
        assert workspace.customers.find_by_name(name).id == customer.id

    def test_work_items_add_then_remove(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        workspace: LoadedWorkspace,
        customer: LoadedCustomer,
    ) -> None:
        work_items = client.v2.workspaces.projects.work_items
        work_item = work_items.create(
            workspace_slug, project_id, CreateWorkItem(name=unique_name("wi-customer-link"))
        )
        try:
            added = customer.work_items.add([work_item.id])
            assert work_item.id in added

            removed = customer.work_items.remove([work_item.id])
            assert work_item.id in removed
        finally:
            work_items.delete(workspace_slug, project_id, work_item.id)

    def test_requests_crud(self, customer: LoadedCustomer) -> None:
        created = customer.requests.create(CreateCustomerRequest(name=unique_name("request")))
        try:
            fetched = customer.requests.retrieve(created.id)
            assert fetched.id == created.id

            page = customer.requests.list()
            assert any(r.id == created.id for r in page.data)

            updated = customer.requests.update(
                created.id, UpdateCustomerRequest(link="https://x.test")
            )
            assert updated.link == "https://x.test"
        finally:
            customer.requests.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            customer.requests.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_property_values_list_is_empty_map_for_a_fresh_customer(
        self, customer: LoadedCustomer
    ) -> None:
        values = customer.property_values.list()
        assert values.model_dump() == {}

    def test_property_values_create_against_an_existing_customer_property(
        self, workspace: LoadedWorkspace, customer: LoadedCustomer
    ) -> None:
        """Bulk-set requires an existing customer property id; this workspace may
        have none provisioned (customer properties are a separate resource, covered
        by `test_customer_properties.py`) -- a declared server-capability skip.

        The property lookup used to hand-roll `transport.request`, which skipped the
        kernel's own `fields`/`expand` validation; it goes through the resource now."""
        rows = workspace.customer_properties.list().data
        if not rows:
            skip_absent_capability("no customer properties provisioned in this workspace")
        property_id = rows[0].id

        customer.property_values.create(
            CreateCustomerPropertyValues(values={property_id: ["test-value"]})
        )

        values = customer.property_values.list()
        assert values.model_dump().get(property_id) == ["test-value"]
