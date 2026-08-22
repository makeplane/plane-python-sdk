"""Offline coverage for `WebhookLogs`: a read-only delivery log nested under a webhook id (list,
retrieve, `iterate`)."""

from __future__ import annotations

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.webhook_logs import WebhookLogs
from plane.config import Configuration

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def webhook_logs(config: Configuration) -> WebhookLogs:
    return WebhookLogs(V2Transport(config), slug="acme")


@responses.activate
def test_webhook_logs_list(webhook_logs: WebhookLogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/webhook-logs/wh-1/",
        json={
            "data": [{"id": "log-1", "webhook_id": "wh-1", "response_status": "200"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = webhook_logs.list("wh-1")

    assert page.data[0].response_status == "200"


@responses.activate
def test_webhook_logs_retrieve(webhook_logs: WebhookLogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/webhook-logs/wh-1/log-1/",
        json={"id": "log-1", "webhook_id": "wh-1", "request_method": "POST"},
    )

    log = webhook_logs.retrieve("wh-1", "log-1")

    assert log.request_method == "POST"


@responses.activate
def test_webhook_logs_iter_follows_pages(webhook_logs: WebhookLogs) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/webhook-logs/wh-1/",
        json={
            "data": [{"id": "1"}],
            "pagination": {"style": "offset"},
            "next": 1,
        },
    )
    responses.get(
        f"{BASE}/workspaces/acme/webhook-logs/wh-1/",
        json={"data": [{"id": "2"}], "pagination": {"style": "offset"}, "next": None},
    )

    ids = [row.id for row in webhook_logs.iterate("wh-1")]

    assert ids == ["1", "2"]
