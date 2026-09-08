"""Offline coverage for `Estimates`/`EstimatePoints`; project-scoped only, no workspace variant."""

from __future__ import annotations

import json

import pytest
import responses
from responses import matchers

from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.estimates import EstimatePoints, Estimates
from plane.config import Configuration
from plane.models.v2.common import BulkRowSuccess
from plane.models.v2.estimates import (
    CreateEstimate,
    CreateEstimatePoint,
    UpdateEstimate,
    UpdateEstimatePoint,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/estimates"


@pytest.fixture
def estimates(config: Configuration) -> Estimates:
    return Estimates(V2Transport(config))


@pytest.fixture
def points(config: Configuration) -> EstimatePoints:
    return EstimatePoints(V2Transport(config))


# -- Estimates CRUD + upsert --------------------------------------------------------


@responses.activate
def test_list_estimates(estimates: Estimates) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "T-shirt sizes", "type": "categories"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = estimates.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].type == "categories"
    assert responses.calls[0].request.url == f"{BASE}/"


@responses.activate
def test_find_by_name(estimates: Estimates) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "T-shirt sizes", "type": "categories"}],
            "pagination": {"style": "offset"},
        },
        match=[
            matchers.query_param_matcher(
                {"name": "T-shirt sizes", "per_page": "2", "count": "False"}
            )
        ],
    )

    assert estimates.find_by_name("acme", "ENG", "T-shirt sizes").id == "1"


@responses.activate
def test_sparse_response_raises_for_a_field_not_requested(estimates: Estimates) -> None:
    """`estimates.list` now returns navigable (`Loaded`) rows: a field neither
    requested nor returned raises `FieldNotRequested` instead of reading as a
    silent `None` -- see `tests/v2/test_loaded_families.py`."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = estimates.list("acme", "ENG", fields=["id"])

    assert page.data[0].id == "1"
    with pytest.raises(FieldNotRequested, match="name"):
        _ = page.data[0].name
    with pytest.raises(FieldNotRequested, match="last_used"):
        _ = page.data[0].last_used


@responses.activate
def test_expand_points_is_encoded_and_parsed(estimates: Estimates) -> None:
    responses.get(
        f"{BASE}/1/",
        json={
            "id": "1",
            "name": "Fibonacci",
            "type": "points",
            "points": [{"id": "p1", "key": 0, "value": "1"}],
        },
    )

    estimate = estimates.retrieve("acme", "ENG", "1", expand=["points"])

    assert "expand=points" in responses.calls[0].request.url
    assert estimate.points is not None
    assert estimate.points[0].value == "1"


@responses.activate
def test_create_then_patch_then_delete(estimates: Estimates) -> None:
    responses.post(f"{BASE}/", json={"id": "1", "name": "Sizes"}, status=201)
    responses.patch(f"{BASE}/1/", json={"id": "1", "name": "T-Shirt Sizes"})
    responses.delete(f"{BASE}/1/", status=204)

    created = estimates.create("acme", "ENG", CreateEstimate(name="Sizes"))
    assert responses.calls[0].request.url == f"{BASE}/"

    updated = estimates.update("acme", "ENG", created.id, UpdateEstimate(name="T-Shirt Sizes"))
    assert updated.name == "T-Shirt Sizes"
    assert responses.calls[1].request.url == f"{BASE}/1/"

    assert estimates.delete("acme", "ENG", created.id) is None
    assert responses.calls[2].request.url == f"{BASE}/1/"


@responses.activate
def test_upsert_reconciles_on_external_id(estimates: Estimates) -> None:
    responses.post(f"{BASE}/upsert/", json={"id": "1", "name": "Imported"})

    result = estimates.upsert(
        "acme",
        "ENG",
        CreateEstimate(name="Imported", external_source="jira", external_id="EST-1"),
    )

    assert result.id == "1"
    assert responses.calls[0].request.url == f"{BASE}/upsert/"


def test_unknown_field_is_rejected_before_the_request(estimates: Estimates) -> None:
    with pytest.raises(ValueError, match="nope"):
        estimates.list("acme", "ENG", fields=["nope"])


def test_unknown_expand_is_rejected_before_the_request(estimates: Estimates) -> None:
    with pytest.raises(ValueError, match="bogus"):
        estimates.list("acme", "ENG", expand=["bogus"])


@responses.activate
def test_bulk_create_update_delete(estimates: Estimates) -> None:
    responses.post(
        f"{BASE}/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )
    responses.post(
        f"{BASE}/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )
    responses.post(
        f"{BASE}/bulk-delete/",
        json={
            "results": [{"index": 0, "result": "deleted", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    created = estimates.bulk_create("acme", "ENG", [CreateEstimate(name="Sizes")])
    assert isinstance(created.results[0], BulkRowSuccess)

    updated = estimates.bulk_update("acme", "ENG", [{"id": "1", "name": "Sizes v2"}])
    assert updated.succeeded == 1

    deleted = estimates.bulk_delete("acme", "ENG", ["1"])
    assert deleted.succeeded == 1
    body = json.loads(responses.calls[2].request.body)
    assert body == {"ids": ["1"], "all_or_none": False}


# -- Nested EstimatePoints -----------------------------------------------------------


@responses.activate
def test_points_list_is_nested_under_the_estimate(points: EstimatePoints) -> None:
    responses.get(
        f"{BASE}/1/points/",
        json={
            "data": [{"id": "p1", "key": 0, "value": "XS"}],
            "pagination": {"style": "offset"},
        },
    )

    page = points.list("acme", "ENG", "1")

    assert page.data[0].value == "XS"
    assert responses.calls[0].request.url.startswith(f"{BASE}/1/points/")


@responses.activate
def test_points_find_by_key(points: EstimatePoints) -> None:
    responses.get(
        f"{BASE}/1/points/",
        json={
            "data": [{"id": "p1", "key": 3, "value": "M"}],
            "pagination": {"style": "offset"},
        },
        match=[matchers.query_param_matcher({"key": "3", "per_page": "2", "count": "False"})],
    )

    assert points.find_by_key("acme", "ENG", "1", 3).id == "p1"


@responses.activate
def test_points_create_retrieve_update_delete(points: EstimatePoints) -> None:
    responses.post(f"{BASE}/1/points/", json={"id": "p1", "value": "XS", "key": 0}, status=201)
    responses.get(f"{BASE}/1/points/p1/", json={"id": "p1", "value": "XS", "key": 0})
    responses.patch(f"{BASE}/1/points/p1/", json={"id": "p1", "value": "Small", "key": 0})
    responses.delete(f"{BASE}/1/points/p1/", status=204)

    created = points.create("acme", "ENG", "1", CreateEstimatePoint(value="XS", key=0))
    assert created.id == "p1"
    assert responses.calls[0].request.url == f"{BASE}/1/points/"

    fetched = points.retrieve("acme", "ENG", "1", created.id)
    assert fetched.value == "XS"
    assert responses.calls[1].request.url == f"{BASE}/1/points/p1/"

    updated = points.update("acme", "ENG", "1", created.id, UpdateEstimatePoint(value="Small"))
    assert updated.value == "Small"
    assert responses.calls[2].request.url == f"{BASE}/1/points/p1/"

    assert points.delete("acme", "ENG", "1", created.id) is None
    assert responses.calls[3].request.url == f"{BASE}/1/points/p1/"


@responses.activate
def test_points_upsert(points: EstimatePoints) -> None:
    responses.post(f"{BASE}/1/points/upsert/", json={"id": "p1", "value": "XS", "key": 0})

    result = points.upsert(
        "acme", "ENG", "1", CreateEstimatePoint(value="XS", external_source="x", external_id="1")
    )

    assert result.id == "p1"


@responses.activate
def test_points_bulk_create_update_delete(points: EstimatePoints) -> None:
    responses.post(
        f"{BASE}/1/points/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "p1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )
    responses.post(
        f"{BASE}/1/points/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "p1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )
    responses.post(
        f"{BASE}/1/points/bulk-delete/",
        json={
            "results": [{"index": 0, "result": "deleted", "id": "p1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    created = points.bulk_create("acme", "ENG", "1", [CreateEstimatePoint(value="XS")])
    assert created.succeeded == 1

    updated = points.bulk_update("acme", "ENG", "1", [{"id": "p1", "value": "Small"}])
    assert updated.succeeded == 1

    deleted = points.bulk_delete("acme", "ENG", "1", ["p1"])
    assert deleted.succeeded == 1


def test_points_batch_cap_is_enforced_client_side(points: EstimatePoints) -> None:
    with pytest.raises(ValueError, match="At most 50"):
        points.bulk_delete("acme", "ENG", "1", [str(n) for n in range(51)])
