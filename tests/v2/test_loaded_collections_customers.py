"""Navigable rows for the two families migrated in this plan: `Collection` (children
`members`, `pages`) and `Customer` (children `requests`, `property_values`,
`work_items`).

Neither family is wired onto the flat tree yet -- that is a later plan -- so each is
constructed directly through `V2Transport`, the same way every other offline resource
test in this package is, rather than reached through `V2Namespace`."""

from __future__ import annotations

import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.collections import Collections
from plane.api.v2.customers import Customers
from plane.config import Configuration


@responses.activate
def test_fetched_customer_reaches_its_requests(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/customers/c1/", json={"id": "c1", "name": "Acme Ltd"})
    responses.get(
        f"{base}/customers/c1/requests/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    customer = Customers(V2Transport(config)).retrieve("acme", "c1")
    customer.requests.list()

    assert customer.name == "Acme Ltd"
    assert responses.calls[1].request.url == f"{base}/customers/c1/requests/"


@responses.activate
def test_fetched_customer_reaches_its_work_items(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/customers/c1/", json={"id": "c1", "name": "Acme Ltd"})
    responses.post(f"{base}/customers/c1/work-items/", json={"added": ["w1"], "removed": []})

    customer = Customers(V2Transport(config)).retrieve("acme", "c1")
    added = customer.work_items.add(["w1"])

    assert added == ["w1"]
    assert responses.calls[1].request.url == f"{base}/customers/c1/work-items/"


@responses.activate
def test_fetched_customer_reaches_its_property_values(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/customers/c1/", json={"id": "c1", "name": "Acme Ltd"})
    responses.get(f"{base}/customers/c1/property-values/", json={"prop-1": ["Enterprise"]})

    customer = Customers(V2Transport(config)).retrieve("acme", "c1")
    values = customer.property_values.list()

    assert values.model_dump() == {"prop-1": ["Enterprise"]}
    assert responses.calls[1].request.url == f"{base}/customers/c1/property-values/"


@responses.activate
def test_listed_customers_are_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(
        f"{base}/customers/",
        json={
            "data": [{"id": "c1", "name": "Acme Ltd"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )
    responses.get(
        f"{base}/customers/c1/requests/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    page = Customers(V2Transport(config)).list("acme")
    page.data[0].requests.list()

    assert responses.calls[1].request.url == f"{base}/customers/c1/requests/"


@responses.activate
def test_fetched_collection_reaches_its_members_and_pages(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/collections"
    responses.get(f"{base}/co1/", json={"id": "co1", "name": "Runbooks"})
    responses.get(f"{base}/co1/members/", json=[{"id": "m1", "member_id": "u1"}])
    responses.post(f"{base}/co1/pages/", json={"added": ["p1"], "removed": []})

    collection = Collections(V2Transport(config)).retrieve("acme", "co1")
    members = collection.members.list()
    added = collection.pages.add(["p1"])

    assert collection.name == "Runbooks"
    assert [m.member_id for m in members] == ["u1"]
    assert added == ["p1"]
    assert responses.calls[1].request.url == f"{base}/co1/members/"
    assert responses.calls[2].request.url == f"{base}/co1/pages/"


@responses.activate
def test_default_collection_is_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/collections"
    responses.get(
        f"{base}/",
        json={
            "data": [{"id": "co1", "name": "General", "is_default": True}],
            "pagination": {"style": "offset"},
        },
    )
    responses.get(f"{base}/co1/members/", json=[])

    default = Collections(V2Transport(config)).default("acme")
    default.members.list()

    assert default.id == "co1"
    assert responses.calls[1].request.url == f"{base}/co1/members/"
