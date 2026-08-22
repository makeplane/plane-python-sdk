import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.customer_properties import CustomerProperties
from plane.config import Configuration
from plane.models.v2.customer_properties import CreateCustomerProperty, UpdateCustomerProperty

BASE = "https://api.example.com/api/v2/workspaces/acme/customer-properties"


@pytest.fixture
def customer_properties(config: Configuration) -> CustomerProperties:
    return CustomerProperties(V2Transport(config), slug="acme")


@responses.activate
def test_list_customer_properties(customer_properties: CustomerProperties) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "display_name": "Tier", "property_type": "TEXT"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = customer_properties.list()

    assert page.total_count == 1
    assert page.data[0].property_type == "TEXT"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(customer_properties: CustomerProperties) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = customer_properties.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].display_name is None


def test_list_rejects_unknown_field_before_the_request(
    customer_properties: CustomerProperties,
) -> None:
    with pytest.raises(ValueError, match="Unknown field"):
        customer_properties.list(fields=["bogus"])


@responses.activate
def test_create_then_patch(customer_properties: CustomerProperties) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "display_name": "Tier", "property_type": "TEXT"},
        status=201,
    )
    responses.patch(f"{BASE}/1/", json={"id": "1", "display_name": "Tier (renamed)"})

    created = customer_properties.create(
        CreateCustomerProperty(display_name="Tier", property_type="TEXT")
    )
    updated = customer_properties.update(
        created.id, UpdateCustomerProperty(display_name="Tier (renamed)")
    )

    assert updated.display_name == "Tier (renamed)"


@responses.activate
def test_delete(customer_properties: CustomerProperties) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert customer_properties.delete("1") is None


@responses.activate
def test_find_by_name(customer_properties: CustomerProperties) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "Tier"}], "pagination": {"style": "offset"}},
    )

    assert customer_properties.find_by_name("Tier").id == "1"
