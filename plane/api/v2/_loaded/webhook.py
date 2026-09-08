"""A fetched webhook row that is also the place its delivery logs live."""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.webhooks import Webhook
from .._kernel.loaded import Loaded, Owned, bind2

if TYPE_CHECKING:
    from ..webhook_logs import WebhookLogs
    from ..webhooks import Webhooks

    # Typed view on `Owned`: `WebhookLogs`' own methods with `slug` and `webhook`
    # already supplied -- `bind2`, because two path ids are bound (webhooks are
    # workspace-scoped, with no project ancestor). Evaluated only by a type
    # checker -- at runtime this property returns a plain `Owned`.

    class _OwnedWebhookLogs(Owned["WebhookLogs"]):
        list = staticmethod(bind2(WebhookLogs.list))
        iterate = staticmethod(bind2(WebhookLogs.iterate))
        retrieve = staticmethod(bind2(WebhookLogs.retrieve))


class LoadedWebhook(Loaded, Webhook):
    """A webhook row that is also the place its delivery logs live."""

    model_config = {**Webhook.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Webhooks._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Webhooks

    @property
    def logs(self) -> _OwnedWebhookLogs:
        return cast("_OwnedWebhookLogs", Owned(self._resources.logs, self._ids, self._id_names))
