"""Webhook delivery logs (api_v2). Read-only, nested under a webhook -- the
parent webhook must live in the same workspace (404 otherwise). The parent
webhook id lives in the *collection* path itself, not after a pk."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from ...models.v2.webhook_logs import WebhookLog
from ._generated.constants import (
    WebhookLogsListField,
    WebhookLogsListOrderBy,
    WebhookLogsRetrieveField,
)
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
        slug: str,
        webhook: str,
        *,
        fields: Sequence[WebhookLogsListField] | None = None,
        order_by: WebhookLogsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
    ) -> Page[WebhookLog]:
        """One page of delivery logs for a webhook. The golden offers no query
        filters on this operation."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
            },
            slug=slug,
            webhook_id=webhook,
        )

    def iterate(
        self,
        slug: str,
        webhook: str,
        *,
        fields: Sequence[WebhookLogsListField] | None = None,
        order_by: WebhookLogsListOrderBy | None = None,
    ) -> Iterator[WebhookLog]:
        """Every delivery log for a webhook, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by}, slug=slug, webhook_id=webhook
        )

    def retrieve(
        self,
        slug: str,
        webhook: str,
        log: str,
        *,
        fields: Sequence[WebhookLogsRetrieveField] | None = None,
    ) -> WebhookLog:
        return self._retrieve(pk=log, params={"fields": fields}, slug=slug, webhook_id=webhook)
