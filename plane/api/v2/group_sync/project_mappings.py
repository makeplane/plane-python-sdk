"""Group sync project mappings (api_v2): IdP group -> project (or every
project) + role."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.group_sync import CreateGroupMapping, GroupMapping, UpdateGroupMapping
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class GroupSyncProjectMappings(V2Resource[GroupMapping, CreateGroupMapping, UpdateGroupMapping]):
    path = "/workspaces/{slug}/group-sync/project-mappings/"
    model = GroupMapping
    operations = {
        "list": "group_sync_project_mappings_list",
        "retrieve": "group_sync_project_mappings_retrieve",
        "create": "group_sync_project_mappings_create",
        "update": "group_sync_project_mappings_update",
        "delete": "group_sync_project_mappings_destroy",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[GroupMapping]:
        """One page of project mappings in the workspace."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[GroupMapping]:
        """Every project mapping in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self,
        mapping_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> GroupMapping:
        return self._retrieve(pk=mapping_id, params={"fields": fields})

    def create(self, data: CreateGroupMapping) -> GroupMapping:
        return self._create(data)

    def update(self, mapping_id: str, data: UpdateGroupMapping) -> GroupMapping:
        return self._update(data, pk=mapping_id)

    def delete(self, mapping_id: str) -> None:
        return self._delete(pk=mapping_id)
