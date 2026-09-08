"""Group sync workspace mappings (api_v2): IdP group -> workspace role."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.group_sync import (
    CreateWorkspaceGroupMapping,
    UpdateWorkspaceGroupMapping,
    WorkspaceGroupMapping,
)
from .._generated.constants import (
    GroupSyncWorkspaceMappingsCreateField,
    GroupSyncWorkspaceMappingsListField,
    GroupSyncWorkspaceMappingsListFilters,
    GroupSyncWorkspaceMappingsListOrderBy,
    GroupSyncWorkspaceMappingsRetrieveField,
    GroupSyncWorkspaceMappingsUpdateField,
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
        slug: str,
        *,
        fields: Sequence[GroupSyncWorkspaceMappingsListField] | None = None,
        order_by: GroupSyncWorkspaceMappingsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[GroupSyncWorkspaceMappingsListFilters],
    ) -> Page[WorkspaceGroupMapping]:
        """One page of workspace mappings in the workspace."""
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
        fields: Sequence[GroupSyncWorkspaceMappingsListField] | None = None,
        order_by: GroupSyncWorkspaceMappingsListOrderBy | None = None,
        **filters: Unpack[GroupSyncWorkspaceMappingsListFilters],
    ) -> Iterator[WorkspaceGroupMapping]:
        """Every workspace mapping, following pages automatically."""
        return self._iter(params={"fields": fields, "order_by": order_by, **filters}, slug=slug)

    def retrieve(
        self,
        slug: str,
        mapping_id: str,
        *,
        fields: Sequence[GroupSyncWorkspaceMappingsRetrieveField] | None = None,
    ) -> WorkspaceGroupMapping:
        return self._retrieve(pk=mapping_id, params={"fields": fields}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateWorkspaceGroupMapping,
        *,
        fields: Sequence[GroupSyncWorkspaceMappingsCreateField] | None = None,
    ) -> WorkspaceGroupMapping:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        mapping_id: str,
        data: UpdateWorkspaceGroupMapping,
        *,
        fields: Sequence[GroupSyncWorkspaceMappingsUpdateField] | None = None,
    ) -> WorkspaceGroupMapping:
        return self._update(data, pk=mapping_id, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, mapping_id: str) -> None:
        return self._delete(pk=mapping_id, slug=slug)
