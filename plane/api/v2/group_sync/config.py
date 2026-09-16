"""IdP group-sync configuration (api_v2). Workspace-wide singleton -- one row per
workspace, no `id` of its own in the URL, so this goes through the kernel's
`_retrieve_singleton`/`_update_singleton` pair (matching `WorkspaceFeatures`)
rather than `_retrieve`/`_update`, which would append a spurious pk segment."""

from __future__ import annotations

from ....models.v2.group_sync import GroupSyncConfig, UpdateGroupSyncConfig
from .._kernel.resource import V2Resource


class GroupSyncConfigResource(
    V2Resource[GroupSyncConfig, UpdateGroupSyncConfig, UpdateGroupSyncConfig]
):
    """One row per workspace, no create/delete/list -- only `retrieve`/`update` against
    a fixed path, so both hit the collection URL directly, not `_retrieve`/`_update`."""

    path = "/workspaces/{slug}/group-sync/config/"
    model = GroupSyncConfig
    operations = {
        "retrieve": "group_sync_config_retrieve",
        "update": "group_sync_config_update",
    }

    def retrieve(self, slug: str) -> GroupSyncConfig:
        return self._retrieve_singleton(action="retrieve", slug=slug)

    def update(self, slug: str, data: UpdateGroupSyncConfig) -> GroupSyncConfig:
        return self._update_singleton(data, action="update", slug=slug)
