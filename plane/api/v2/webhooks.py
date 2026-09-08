"""Webhooks (api_v2) -- workspace outbound webhook subscriptions. `create`/
`regenerate` return `WebhookCreateResult` (carries `secret_key` once; see that
model's docstring for the golden mismatch) -- neither exposes a `fields` param,
since a sparse response could drop it. Delivery history is `webhooks.logs`.

A fetched row (`retrieve`, and every row in a `list` page) comes back as a
`LoadedWebhook`: it carries the row's data and can reach `.logs.list()` etc.
without the caller repeating `slug`/`webhook`. `create`/`regenerate` answer with
`WebhookCreateResult`, not a `Webhook` row, so they are not navigable."""

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
from ._kernel.loaded import LoadsNavigableRows
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from ._loaded.webhook import LoadedWebhook
from .webhook_logs import WebhookLogs

__all__ = ["Webhooks"]


class Webhooks(
    V2Resource[Webhook, CreateWebhook, UpdateWebhook], LoadsNavigableRows[LoadedWebhook]
):
    path = "/workspaces/{slug}/webhooks/"
    model = Webhook
    loaded_model = LoadedWebhook
    loaded_names = ("slug", "webhook")
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
    ) -> Page[LoadedWebhook]:
        """One page of the workspace's webhooks."""
        page = self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
        )
        return self._load_page(page, slug, fields=fields)

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WebhooksListField] | None = None,
        order_by: WebhooksListOrderBy | None = None,
        **filters: Unpack[WebhooksListFilters],
    ) -> Iterator[LoadedWebhook]:
        """Every webhook in the workspace, following pages automatically."""
        rows = self._iter(params={"fields": fields, "order_by": order_by, **filters}, slug=slug)
        return (self._load(row, slug, fields=fields) for row in rows)

    def retrieve(
        self, slug: str, webhook: str, *, fields: Sequence[WebhooksRetrieveField] | None = None
    ) -> LoadedWebhook:
        row = self._retrieve(pk=webhook, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def find_by_name(self, slug: str, name: str) -> LoadedWebhook:
        """The one webhook with this name; raises if none or several match."""
        row = self._find_one(filters={"name": name}, slug=slug)
        return self._load(row, slug)

    def create(self, slug: str, data: CreateWebhook) -> WebhookCreateResult:
        """Create a webhook. The response carries `secret_key` once -- store
        it; it cannot be retrieved again (only regenerated, which mints a new
        one). See the module docstring for why no `fields` param is exposed.

        Answers with `WebhookCreateResult`, not a `Webhook` row -- not
        navigable; `retrieve` the webhook afterwards to reach `.logs`."""
        return self._custom_action("create", model=WebhookCreateResult, data=data, slug=slug)

    def update(
        self,
        slug: str,
        webhook: str,
        data: UpdateWebhook,
        *,
        fields: Sequence[WebhooksPartialUpdateField] | None = None,
    ) -> LoadedWebhook:
        row = self._update(data, pk=webhook, params={"fields": fields}, slug=slug)
        return self._load(row, slug, fields=fields)

    def delete(self, slug: str, webhook: str) -> None:
        return self._delete(pk=webhook, slug=slug)

    def regenerate(self, slug: str, webhook: str) -> WebhookCreateResult:
        """Mint a new secret for this webhook, returning it once (see
        `create`)."""
        return self._custom_action("regenerate", model=WebhookCreateResult, pk=webhook, slug=slug)
