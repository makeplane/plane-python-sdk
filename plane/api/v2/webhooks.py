"""Webhooks (api_v2) -- workspace outbound webhook subscriptions. `create`/
`regenerate` return `WebhookCreateResult` (carries `secret_key` once; see that
model's docstring for the golden mismatch) -- neither exposes a `fields` param,
since a sparse response could drop it. Delivery history is `webhooks.logs`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ...models.v2.webhooks import CreateWebhook, UpdateWebhook, Webhook, WebhookCreateResult
from ._generated.constants import (
    WebhooksListField,
    WebhooksListFilters,
    WebhooksListOrderBy,
    WebhooksPartialUpdateField,
    WebhooksRetrieveField,
)
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

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.logs = WebhookLogs(transport)

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WebhooksListField] | None = None,
        order_by: WebhooksListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WebhooksListFilters],
    ) -> Page[Webhook]:
        """One page of the workspace's webhooks."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WebhooksListField] | None = None,
        order_by: WebhooksListOrderBy | None = None,
        **filters: Unpack[WebhooksListFilters],
    ) -> Iterator[Webhook]:
        """Every webhook in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "order_by": order_by, **filters}, slug=slug)

    def retrieve(
        self, slug: str, webhook: str, *, fields: Sequence[WebhooksRetrieveField] | None = None
    ) -> Webhook:
        return self._retrieve(pk=webhook, params={"fields": fields}, slug=slug)

    def find_by_name(self, slug: str, name: str) -> Webhook:
        """The one webhook with this name; raises if none or several match."""
        return self._find_one(filters={"name": name}, slug=slug)

    def create(self, slug: str, data: CreateWebhook) -> WebhookCreateResult:
        """Create a webhook. The response carries `secret_key` once -- store
        it; it cannot be retrieved again (only regenerated, which mints a new
        one). See the module docstring for why no `fields` param is exposed."""
        return self._custom_action("create", model=WebhookCreateResult, data=data, slug=slug)

    def update(
        self,
        slug: str,
        webhook: str,
        data: UpdateWebhook,
        *,
        fields: Sequence[WebhooksPartialUpdateField] | None = None,
    ) -> Webhook:
        return self._update(data, pk=webhook, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, webhook: str) -> None:
        return self._delete(pk=webhook, slug=slug)

    def regenerate(self, slug: str, webhook: str) -> WebhookCreateResult:
        """Mint a new secret for this webhook, returning it once (see
        `create`)."""
        return self._custom_action("regenerate", model=WebhookCreateResult, pk=webhook, slug=slug)
