"""Webhook delivery logs (api_v2). Read-only, nested under a webhook -- the
parent webhook must live in the same workspace (404 otherwise)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.webhook_logs import WebhookLog
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource


# No write/patch DTO exists for webhook logs -- the type parameters are filled
# with the read model itself as an unused placeholder (see PermissionSchemes).
class WebhookLogs(V2Resource[WebhookLog, WebhookLog, WebhookLog]):
    path = "/workspaces/{slug}/webhook-logs/{webhook_id}/"
    model = WebhookLog
    operations = {
        "list": "webhook_logs_list",
        "retrieve": "webhook_logs_retrieve",
    }

    def list(
        self,
        webhook_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WebhookLog]:
        """One page of delivery logs for a webhook."""
        return self._list(webhook_id=webhook_id, params={"fields": fields, **filters})

    def iterate(
        self,
        webhook_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WebhookLog]:
        """Every delivery log for a webhook, following pages automatically."""
        return self._iter(webhook_id=webhook_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        webhook_id: str,
        log_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WebhookLog:
        return self._retrieve(pk=log_id, webhook_id=webhook_id, params={"fields": fields})
