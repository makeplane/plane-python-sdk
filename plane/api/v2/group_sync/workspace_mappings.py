"""Group sync workspace mappings (api_v2): IdP group -> workspace role."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.group_sync import (
    CreateWorkspaceGroupMapping,
    UpdateWorkspaceGroupMapping,
    WorkspaceGroupMapping,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class GroupSyncWorkspaceMappings(
    V2Resource[WorkspaceGroupMapping, CreateWorkspaceGroupMapping, UpdateWorkspaceGroupMapping]
):
    path = "/workspaces/{slug}/group-sync/workspace-mappings/"
    model = WorkspaceGroupMapping
    operations = {
        "list": "group_sync_workspace_mappings_list",
        "retrieve": "group_sync_workspace_mappings_retrieve",
        "create": "group_sync_workspace_mappings_create",
        "update": "group_sync_workspace_mappings_update",
        "delete": "group_sync_workspace_mappings_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkspaceGroupMapping]:
        """One page of workspace mappings in the workspace."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkspaceGroupMapping]:
        """Every workspace mapping, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        mapping_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkspaceGroupMapping:
        return self._retrieve(pk=mapping_id, params={"fields": fields})

    def create(self, data: CreateWorkspaceGroupMapping) -> WorkspaceGroupMapping:
        return self._create(data)

    def update(
        self, mapping_id: str, data: UpdateWorkspaceGroupMapping
    ) -> WorkspaceGroupMapping:
        return self._update(data, pk=mapping_id)

    def delete(self, mapping_id: str) -> None:
        return self._delete(pk=mapping_id)
