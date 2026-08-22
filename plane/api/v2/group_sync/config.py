"""IdP group-sync configuration (api_v2). Workspace-wide singleton."""

from __future__ import annotations

from ....models.v2.group_sync import GroupSyncConfig, UpdateGroupSyncConfig
from .._kernel.resource import V2Resource


class GroupSyncConfigResource(
    V2Resource[GroupSyncConfig, UpdateGroupSyncConfig, UpdateGroupSyncConfig]
):
    """One row per workspace, no create/delete/list -- only `get`/`update` against
    a fixed path, so both hit the collection URL directly, not `_retrieve`/`_update`."""

    path = "/workspaces/{slug}/group-sync/config/"
    model = GroupSyncConfig
    operations = {
        "retrieve": "group_sync_config_retrieve",
        "update": "group_sync_config_update",
    }

    def get(self) -> GroupSyncConfig:
        payload = self.transport.request("GET", self._collection_url())
        return self.model.model_validate(payload)

    def update(self, data: UpdateGroupSyncConfig) -> GroupSyncConfig:
        payload = self.transport.request(
            "PATCH",
            self._collection_url(),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return self.model.model_validate(payload)
