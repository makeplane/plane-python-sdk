"""Offline coverage for `Customers`: CRUD, `upsert`, the `requests` sub-resource, dict-shaped
`property_values`, and the `.work_items` membership bridge (`add`/`remove`)."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.customers import Customers
from plane.config import Configuration
from plane.models.v2.customers import (
    CreateCustomer,
    CreateCustomerPropertyValues,
    CreateCustomerRequest,
    UpdateCustomer,
    UpdateCustomerRequest,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/customers"


@pytest.fixture
def customers(config: Configuration) -> Customers:
    return Customers(V2Transport(config), slug="acme")


@responses.activate
def test_list_customers_is_workspace_scoped_not_project_scoped(customers: Customers) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "cu1", "name": "Acme Inc"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = customers.list()

    assert page.data[0].name == "Acme Inc"
    assert "projects" not in responses.calls[0].request.url


@responses.activate
def test_create_then_patch_then_delete_customer(customers: Customers) -> None:
    responses.post(f"{BASE}/", json={"id": "cu1", "name": "Acme Inc"}, status=201)
    responses.patch(f"{BASE}/cu1/", json={"id": "cu1", "stage": "onboarding"})
    responses.delete(f"{BASE}/cu1/", status=204)

    created = customers.create(CreateCustomer(name="Acme Inc"))
    updated = customers.update(created.id, UpdateCustomer(stage="onboarding"))

    assert updated.stage == "onboarding"
    assert customers.delete("cu1") is None


@responses.activate
def test_upsert_customer(customers: Customers) -> None:
    responses.post(f"{BASE}/upsert/", json={"id": "cu1", "name": "Acme Inc"})

    assert customers.upsert(CreateCustomer(name="Acme Inc")).id == "cu1"


@responses.activate
def test_find_customer_by_name(customers: Customers) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "cu1", "name": "Acme Inc"}], "pagination": {"style": "offset"}},
    )

    assert customers.find_by_name("Acme Inc").id == "cu1"


@responses.activate
def test_work_items_add_sends_add_body_and_returns_added(customers: Customers) -> None:
    responses.post(
        f"{BASE}/cu1/work-items/",
        json={"added": ["wi-1"], "removed": []},
    )

    result = customers.work_items.add("cu1", ["wi-1"])

    assert result == ["wi-1"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"add": ["wi-1"]}
    assert responses.calls[0].request.url == f"{BASE}/cu1/work-items/"


@responses.activate
def test_work_items_remove_sends_remove_body_and_returns_removed(customers: Customers) -> None:
    responses.post(
        f"{BASE}/cu1/work-items/",
        json={"added": [], "removed": ["wi-2"]},
    )

    result = customers.work_items.remove("cu1", ["wi-2"])

    assert result == ["wi-2"]
    body = json.loads(responses.calls[0].request.body)
    assert body == {"remove": ["wi-2"]}
    assert responses.calls[0].request.url == f"{BASE}/cu1/work-items/"


@responses.activate
def test_work_items_bridge_rejects_empty_or_oversized_ids(customers: Customers) -> None:
    with pytest.raises(ValueError):
        customers.work_items.add("cu1", [])
    with pytest.raises(ValueError):
        customers.work_items.add("cu1", [f"wi-{i}" for i in range(101)])
    with pytest.raises(ValueError):
        customers.work_items.remove("cu1", [])
    with pytest.raises(ValueError):
        customers.work_items.remove("cu1", [f"wi-{i}" for i in range(101)])

    assert len(responses.calls) == 0


# -- Nested: requests -------------------------------------------------------------


@responses.activate
def test_customer_requests_crud(customers: Customers) -> None:
    responses.get(
        f"{BASE}/cu1/requests/",
        json={"data": [{"id": "cr1", "name": "Need SSO"}], "pagination": {"style": "offset"}},
    )
    responses.post(f"{BASE}/cu1/requests/", json={"id": "cr1", "name": "Need SSO"}, status=201)
    responses.get(f"{BASE}/cu1/requests/cr1/", json={"id": "cr1", "name": "Need SSO"})
    responses.patch(f"{BASE}/cu1/requests/cr1/", json={"id": "cr1", "name": "Need SSO + SCIM"})
    responses.delete(f"{BASE}/cu1/requests/cr1/", status=204)

    page = customers.requests.list("cu1")
    assert page.data[0].name == "Need SSO"

    created = customers.requests.create(
        "cu1", CreateCustomerRequest(name="Need SSO", work_item_ids=["wi-1"])
    )
    assert created.id == "cr1"
    body = json.loads(responses.calls[1].request.body)
    assert body == {"name": "Need SSO", "work_item_ids": ["wi-1"]}

    fetched = customers.requests.retrieve("cu1", "cr1")
    assert fetched.id == "cr1"

    updated = customers.requests.update("cu1", "cr1", UpdateCustomerRequest(name="Need SSO + SCIM"))
    assert updated.name == "Need SSO + SCIM"

    assert customers.requests.delete("cu1", "cr1") is None


# -- Nested: property_values (dict-shaped, no pagination) ------------------------


@responses.activate
def test_property_values_list_returns_dynamic_mapping(customers: Customers) -> None:
    responses.get(
        f"{BASE}/cu1/property-values/",
        json={"prop-1": ["Enterprise"], "prop-2": ["true"]},
    )

    values = customers.property_values.list("cu1")

    assert values.model_dump() == {"prop-1": ["Enterprise"], "prop-2": ["true"]}


@responses.activate
def test_property_values_create_bulk_sets_and_returns_none(customers: Customers) -> None:
    responses.post(f"{BASE}/cu1/property-values/", json=None, status=204)

    result = customers.property_values.create(
        "cu1", CreateCustomerPropertyValues(values={"prop-1": ["Enterprise"]})
    )

    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body == {"values": {"prop-1": ["Enterprise"]}}
