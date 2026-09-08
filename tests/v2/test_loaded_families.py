"""Navigable rows for the five families migrated in this plan: `Cycle`, `Milestone`,
`Module`, `Estimate` and `Webhook`. Each owns exactly one child.

These resources are not (yet) wired onto the flat tree -- that is a later plan -- so
each is constructed directly through `V2Transport`, the same way every other offline
resource test in this package is, rather than reached through `V2Namespace`."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.cycles import Cycles
from plane.api.v2.estimates import Estimates
from plane.api.v2.milestones import Milestones
from plane.api.v2.modules import Modules
from plane.api.v2.webhooks import Webhooks
from plane.config import Configuration

# -- Cycles: `.work_items` bridge ------------------------------------------------


@responses.activate
def test_fetched_cycle_reaches_its_work_items(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/cycles/c1/", json={"id": "c1", "name": "Sprint 1"})
    responses.post(f"{base}/cycles/c1/work-items/", json={"added": ["w1"]})

    cycle = Cycles(V2Transport(config)).retrieve("acme", "ENG", "c1")
    added = cycle.work_items.add(["w1"])

    assert cycle.name == "Sprint 1"
    assert added == ["w1"]
    assert responses.calls[1].request.url.endswith("/cycles/c1/work-items/")


@responses.activate
def test_listed_and_iterated_cycles_are_both_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    page = {
        "data": [{"id": "c1", "name": "Sprint 1"}],
        "pagination": {"style": "offset"},
        "total_count": 1,
    }
    responses.get(f"{base}/cycles/", json=page)

    cycles = Cycles(V2Transport(config))
    assert hasattr(cycles.list("acme", "ENG").data[0], "work_items")
    assert hasattr(next(iter(cycles.iterate("acme", "ENG"))), "work_items")


@responses.activate
def test_cycle_retrieve_with_fields_raises_on_an_unrequested_field(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/cycles/c1/", json={"id": "c1"})

    cycle = Cycles(V2Transport(config)).retrieve("acme", "ENG", "c1", fields=["id"])

    assert cycle._present == frozenset({"id"})
    with pytest.raises(FieldNotRequested, match="name"):
        _ = cycle.name


# -- Milestones: `.work_items` bridge --------------------------------------------


@responses.activate
def test_fetched_milestone_reaches_its_work_items(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/milestones/m1/", json={"id": "m1", "title": "GA"})
    responses.post(f"{base}/milestones/m1/work-items/", json={"added": ["w1"]})

    milestone = Milestones(V2Transport(config)).retrieve("acme", "ENG", "m1")
    added = milestone.work_items.add(["w1"])

    assert added == ["w1"]
    assert responses.calls[1].request.url.endswith("/milestones/m1/work-items/")


@responses.activate
def test_listed_and_iterated_milestones_are_both_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    page = {
        "data": [{"id": "m1", "title": "GA"}],
        "pagination": {"style": "offset"},
        "total_count": 1,
    }
    responses.get(f"{base}/milestones/", json=page)

    milestones = Milestones(V2Transport(config))
    assert hasattr(milestones.list("acme", "ENG").data[0], "work_items")
    assert hasattr(next(iter(milestones.iterate("acme", "ENG"))), "work_items")


# -- Modules: `.work_items` bridge -----------------------------------------------


@responses.activate
def test_fetched_module_reaches_its_work_items(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/modules/mod1/", json={"id": "mod1", "name": "Auth"})
    responses.post(f"{base}/modules/mod1/work-items/", json={"added": ["w1"]})

    module = Modules(V2Transport(config)).retrieve("acme", "ENG", "mod1")
    added = module.work_items.add(["w1"])

    assert added == ["w1"]
    assert responses.calls[1].request.url.endswith("/modules/mod1/work-items/")


@responses.activate
def test_listed_and_iterated_modules_are_both_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    page = {
        "data": [{"id": "mod1", "name": "Auth"}],
        "pagination": {"style": "offset"},
        "total_count": 1,
    }
    responses.get(f"{base}/modules/", json=page)

    modules = Modules(V2Transport(config))
    assert hasattr(modules.list("acme", "ENG").data[0], "work_items")
    assert hasattr(next(iter(modules.iterate("acme", "ENG"))), "work_items")


# -- Estimates: `.points` -----------------------------------------------------


@responses.activate
def test_fetched_estimate_reaches_its_points(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/estimates/e1/", json={"id": "e1", "name": "T-shirt"})
    responses.get(
        f"{base}/estimates/e1/points/",
        json={
            "data": [{"id": "pt1", "key": 1}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    estimate = Estimates(V2Transport(config)).retrieve("acme", "ENG", "e1")
    page = estimate.estimate_points.list()

    assert estimate.name == "T-shirt"
    assert page.data[0].key == 1
    assert responses.calls[1].request.url.endswith("/estimates/e1/points/")


@responses.activate
def test_estimate_points_field_survives_expand_alongside_navigation(
    config: Configuration,
) -> None:
    """`Estimate.points` is a real API field (inline data from `expand=["points"]`),
    distinct from the `.estimate_points` navigation property -- a fetched row must
    still be able to read it."""
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(
        f"{base}/estimates/e1/",
        json={
            "id": "e1",
            "name": "Fibonacci",
            "points": [{"id": "p1", "key": 0, "value": "1"}],
        },
    )

    estimate = Estimates(V2Transport(config)).retrieve("acme", "ENG", "e1", expand=["points"])

    assert estimate.points is not None
    assert estimate.points[0].value == "1"


@responses.activate
def test_listed_and_iterated_estimates_are_both_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    page = {
        "data": [{"id": "e1", "name": "T-shirt"}],
        "pagination": {"style": "offset"},
        "total_count": 1,
    }
    responses.get(f"{base}/estimates/", json=page)

    estimates = Estimates(V2Transport(config))
    assert hasattr(estimates.list("acme", "ENG").data[0], "estimate_points")
    assert hasattr(next(iter(estimates.iterate("acme", "ENG"))), "estimate_points")


# -- Webhooks: `.logs` ---------------------------------------------------------


@responses.activate
def test_fetched_webhook_reaches_its_logs(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/webhooks/wh1/", json={"id": "wh1", "url": "https://x.example/hook"})
    responses.get(
        f"{base}/webhook-logs/wh1/",
        json={"data": [{"id": "log1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )

    webhook = Webhooks(V2Transport(config)).retrieve("acme", "wh1")
    page = webhook.logs.list()

    assert page.data[0].id == "log1"
    assert responses.calls[1].request.url.endswith("/webhook-logs/wh1/")


@responses.activate
def test_listed_and_iterated_webhooks_are_both_navigable(config: Configuration) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    page = {
        "data": [{"id": "wh1", "url": "https://x.example/hook"}],
        "pagination": {"style": "offset"},
        "total_count": 1,
    }
    responses.get(f"{base}/webhooks/", json=page)

    webhooks = Webhooks(V2Transport(config))
    assert hasattr(webhooks.list("acme").data[0], "logs")
    assert hasattr(next(iter(webhooks.iterate("acme"))), "logs")


@responses.activate
def test_webhook_retrieve_with_fields_raises_on_an_unrequested_field(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme"
    responses.get(f"{base}/webhooks/wh1/", json={"id": "wh1"})

    webhook = Webhooks(V2Transport(config)).retrieve("acme", "wh1", fields=["id"])

    assert webhook._present == frozenset({"id"})
    with pytest.raises(FieldNotRequested, match="url"):
        _ = webhook.url
