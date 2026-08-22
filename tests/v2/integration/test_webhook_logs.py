"""Live coverage for `client.v2.workspace(slug).webhooks.logs`. A `webhooks_create`
403 may mean the fixture's token lacks admin scope, failing every test here at
fixture setup rather than at the assertion."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2._kernel.errors import PlaneAPIError
from plane.api.v2.webhook_logs import WebhookLogs
from plane.client import PlaneClient


@pytest.fixture
def webhook_logs(client: PlaneClient, workspace_slug: str) -> WebhookLogs:
    return client.v2.workspace(workspace_slug).webhooks.logs


@pytest.fixture
def webhook(client: PlaneClient, workspace_slug: str) -> Iterator[dict[str, Any]]:
    """A throwaway webhook, created straight through the transport the same
    way `conftest.py`'s `project` fixture bootstraps a project."""
    created: dict[str, Any] = client.v2.transport.request(
        "POST",
        f"/workspaces/{workspace_slug}/webhooks/",
        # Scopes are "<entity>.<action>"; a bare entity like "work_item" 400s
        # "Invalid scopes" -- the work-item entity's scope key is "workitem"
        # (no underscore), confirmed live.
        json={
            "url": "https://example.com/plane-webhook-sink",
            "scopes": ["workitem.created"],
        },
    )
    yield created
    try:
        client.v2.transport.request(
            "DELETE", f"/workspaces/{workspace_slug}/webhooks/{created['id']}/"
        )
    except Exception:
        pass


class TestWebhookLogs:
    def test_list_on_a_fresh_webhook_is_empty(
        self, webhook_logs: WebhookLogs, webhook: dict[str, Any]
    ) -> None:
        """No deliveries have happened yet -- an empty page, not an error."""
        page = webhook_logs.list(str(webhook["id"]))
        assert page.data == []

    def test_list_for_a_webhook_in_another_workspace_is_404(
        self, webhook_logs: WebhookLogs
    ) -> None:
        with pytest.raises(PlaneAPIError) as exc_info:
            webhook_logs.list("00000000-0000-0000-0000-000000000000")
        assert exc_info.value.status == 404
