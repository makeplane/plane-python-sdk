"""Initiative work items (api_v2) -- membership bridge between an initiative and
work items."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.initiatives import InitiativeChildManageRequest, InitiativeChildManageResponse
from .._kernel.resource import V2Resource

__all__ = ["InitiativeWorkItems"]


class InitiativeWorkItems(
    V2Resource[
        InitiativeChildManageResponse, InitiativeChildManageRequest, InitiativeChildManageRequest
    ]
):
    """Membership bridge between an initiative and work items: `add` links work
    items to the initiative, `remove` unlinks them. Both POST to
    `.../initiatives/{initiative_id}/work-items/` and return the ids actually
    changed."""

    path = "/workspaces/{slug}/initiatives/{initiative_id}/work-items/"
    model = InitiativeChildManageResponse
    operations = {
        "bridge": "initiatives_work_items",
    }

    def add(self, slug: str, initiative: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Link 1..100 work items to this initiative; returns the ids actually
        added (already-linked ones are omitted)."""
        return self._bridge(key="add", ids=work_item_ids, slug=slug, initiative_id=initiative)

    def remove(
        self, slug: str, initiative: str, work_item_ids: Sequence[str]
    ) -> builtins.list[str]:
        """Unlink 1..100 work items from this initiative; returns the ids
        actually removed."""
        return self._bridge(key="remove", ids=work_item_ids, slug=slug, initiative_id=initiative)
