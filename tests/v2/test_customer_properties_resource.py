import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.customer_properties import CustomerProperties
from plane.config import Configuration
from plane.models.v2.customer_properties import CreateCustomerProperty, UpdateCustomerProperty

BASE = "https://api.example.com/api/v2/workspaces/acme/customer-properties"


@pytest.fixture
def customer_properties(config: Configuration) -> CustomerProperties:
    return CustomerProperties(V2Transport(config))


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

    page = customer_properties.list("acme")

    assert page.total_count == 1
    assert page.data[0].property_type == "TEXT"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_sparse_response_leaves_absent_fields_none(customer_properties: CustomerProperties) -> None:
    responses.get(f"{BASE}/", json={"data": [{"id": "1"}], "pagination": {"style": "offset"}})

    page = customer_properties.list("acme", fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].display_name is None
    assert "fields=id" in responses.calls[0].request.url


def test_list_rejects_unknown_field_before_the_request(
    customer_properties: CustomerProperties,
) -> None:
    with pytest.raises(ValueError, match="Unknown field"):
        customer_properties.list("acme", fields=["bogus"])  # type: ignore[list-item]


@responses.activate
def test_list_per_page_and_offset_reach_the_query_string(
    customer_properties: CustomerProperties,
) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    customer_properties.list("acme", per_page=8, offset=16)

    request_url = responses.calls[0].request.url
    assert "per_page=8" in request_url
    assert "offset=16" in request_url


@responses.activate
def test_iterate_takes_the_workspace_slug(customer_properties: CustomerProperties) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "display_name": "Tier"}], "pagination": {"style": "offset"}},
    )

    rows = list(customer_properties.iterate("acme"))

    assert rows[0].id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_retrieve(customer_properties: CustomerProperties) -> None:
    responses.get(f"{BASE}/1/", json={"id": "1", "display_name": "Tier"})

    prop = customer_properties.retrieve("acme", "1")

    assert prop.display_name == "Tier"
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_create_then_patch(customer_properties: CustomerProperties) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "display_name": "Tier", "property_type": "TEXT"},
        status=201,
    )
    responses.patch(f"{BASE}/1/", json={"id": "1", "display_name": "Tier (renamed)"})

    created = customer_properties.create(
        "acme", CreateCustomerProperty(display_name="Tier", property_type="TEXT")
    )
    assert responses.calls[0].request.url == f"{BASE}/"

    updated = customer_properties.update(
        "acme", created.id, UpdateCustomerProperty(display_name="Tier (renamed)")
    )

    assert updated.display_name == "Tier (renamed)"
    assert responses.calls[1].request.url == f"{BASE}/1/"


@responses.activate
def test_delete(customer_properties: CustomerProperties) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert customer_properties.delete("acme", "1") is None
    assert responses.calls[0].request.url == f"{BASE}/1/"


@responses.activate
def test_find_by_name(customer_properties: CustomerProperties) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "name": "tier"}], "pagination": {"style": "offset"}},
    )

    found = customer_properties.find_by_name("acme", "tier")

    assert found.id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")


@responses.activate
def test_find_by_display_name(customer_properties: CustomerProperties) -> None:
    """`name` is the slugified machine key; `display_name` is the label a user sees --
    the golden recently gained a `display_name` filter alongside `name`."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "display_name": "Tier"}], "pagination": {"style": "offset"}},
    )

    found = customer_properties.find_by_display_name("acme", "Tier")

    assert found.id == "1"
    assert responses.calls[0].request.url.startswith(f"{BASE}/")
    assert "display_name=Tier" in responses.calls[0].request.url
