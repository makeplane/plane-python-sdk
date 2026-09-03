"""Release work-item membership bridge (api_v2)."""

from __future__ import annotations

import builtins
from collections.abc import Sequence

from ....models.v2.releases import ReleaseChildManageRequest, ReleaseChildManageResult
from .._kernel.resource import V2Resource


class ReleaseWorkItems(
    V2Resource[ReleaseChildManageResult, ReleaseChildManageRequest, ReleaseChildManageRequest]
):
    """Membership bridge between a release and work items: `add` attaches work
    items to the release, `remove` detaches them. Both POST to
    `.../releases/{release_id}/work-items/` and return the ids actually
    changed."""

    path = "/workspaces/{slug}/releases/{release_id}/work-items/"
    model = ReleaseChildManageResult
    operations = {
        "bridge": "releases_work_items",
    }

    def add(self, release_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Attach 1..100 work items to this release; returns the ids actually
        added (already-attached ones are omitted)."""
        return self._bridge(key="add", ids=work_item_ids, release_id=release_id)

    def remove(self, release_id: str, work_item_ids: Sequence[str]) -> builtins.list[str]:
        """Detach 1..100 work items from this release; returns the ids
        actually removed."""
        return self._bridge(key="remove", ids=work_item_ids, release_id=release_id)
