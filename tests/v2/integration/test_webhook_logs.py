"""Live coverage for `client.v2.workspaces.webhooks.logs`. A `webhooks_create`
403 may mean the fixture's token lacks admin scope, failing every test here at
fixture setup rather than at the assertion."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2._kernel.errors import PlaneAPIError
from plane.api.v2.webhook_logs import WebhookLogs
from plane.client import PlaneClient
from plane.models.v2.webhooks import CreateWebhook


@pytest.fixture
def webhook_logs(client: PlaneClient) -> WebhookLogs:
    return client.v2.workspaces.webhooks.logs


@pytest.fixture
def webhook(client: PlaneClient, workspace_slug: str) -> Iterator[Any]:
    """A throwaway webhook, through `Webhooks.create` -- it used to hand-roll
    `transport.request`, which skipped the kernel's query validation and left this
    fixture's request path untested along with everything else here."""
    webhooks = client.v2.workspaces.webhooks
    created = webhooks.create(
        workspace_slug,
        # Scopes are "<entity>.<action>"; a bare entity like "work_item" 400s
        # "Invalid scopes" -- the work-item entity's scope key is "workitem"
        # (no underscore), confirmed live.
        CreateWebhook(
            url="https://example.com/plane-webhook-sink",
            scopes=["workitem.created"],
        ),
    )
    yield created
    try:
        webhooks.delete(workspace_slug, created.id)
    except Exception:
        pass


class TestWebhookLogs:
    def test_list_on_a_fresh_webhook_is_empty(
        self, webhook_logs: WebhookLogs, webhook: dict[str, Any], workspace_slug: str
    ) -> None:
        """No deliveries have happened yet -- an empty page, not an error."""
        page = webhook_logs.list(workspace_slug, str(webhook["id"]))
        assert page.data == []

    def test_list_for_a_webhook_in_another_workspace_is_404(
        self, webhook_logs: WebhookLogs, workspace_slug: str
    ) -> None:
        with pytest.raises(PlaneAPIError) as exc_info:
            webhook_logs.list(workspace_slug, "00000000-0000-0000-0000-000000000000")
        assert exc_info.value.status == 404
