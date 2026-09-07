"""Webhooks (api_v2) -- workspace outbound webhook subscriptions. `create`/
`regenerate` return `WebhookCreateResult` (carries `secret_key` once; see that
model's docstring for the golden mismatch). Delivery history is `webhooks.logs`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.webhooks import CreateWebhook, UpdateWebhook, Webhook, WebhookCreateResult
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from .webhook_logs import WebhookLogs

__all__ = ["Webhooks"]


class Webhooks(V2Resource[Webhook, CreateWebhook, UpdateWebhook]):
    path = "/workspaces/{slug}/webhooks/"
    model = Webhook
    operations = {
        "list": "webhooks_list",
        "retrieve": "webhooks_retrieve",
        "create": "webhooks_create",
        "update": "webhooks_partial_update",
        "regenerate": "webhooks_regenerate",
        "delete": "webhooks_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.logs = WebhookLogs(transport, **self._scope)

    def list(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Page[Webhook]:
        """One page of the workspace's webhooks."""
        return self._list(params={"fields": fields, **filters})

    def iterate(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Iterator[Webhook]:
        """Every webhook in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, webhook_id: str, *, fields: Sequence[str] | None = None) -> Webhook:
        return self._retrieve(pk=webhook_id, params={"fields": fields})

    def find_by_name(self, name: str) -> Webhook:
        """The one webhook with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateWebhook) -> WebhookCreateResult:
        """Create a webhook. The response carries `secret_key` once -- store
        it; it cannot be retrieved again (only regenerated, which mints a new
        one). See the module docstring for why no `fields` param is exposed."""
        payload = self.transport.request(
            "POST",
            self._collection_url(),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return WebhookCreateResult.model_validate(payload)

    def update(self, webhook_id: str, data: UpdateWebhook) -> Webhook:
        return self._update(data, pk=webhook_id)

    def delete(self, webhook_id: str) -> None:
        return self._delete(pk=webhook_id)

    def regenerate(self, webhook_id: str) -> WebhookCreateResult:
        """Mint a new secret for this webhook, returning it once (see
        `create`)."""
        payload = self.transport.request("POST", f"{self._detail_url(webhook_id)}regenerate/")
        return WebhookCreateResult.model_validate(payload)
