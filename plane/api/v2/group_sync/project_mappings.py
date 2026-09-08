"""Group sync project mappings (api_v2): IdP group -> project (or every
project) + role. Workspace-level despite the name -- the path carries no
`{project_id}`, only the workspace `slug`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.group_sync import CreateGroupMapping, GroupMapping, UpdateGroupMapping
from .._generated.constants import (
    GroupSyncProjectMappingsCreateField,
    GroupSyncProjectMappingsListField,
    GroupSyncProjectMappingsListFilters,
    GroupSyncProjectMappingsListOrderBy,
    GroupSyncProjectMappingsRetrieveField,
    GroupSyncProjectMappingsUpdateField,
)
from .._kernel.pagination import Page, PaginateStyle
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
        slug: str,
        *,
        fields: Sequence[GroupSyncProjectMappingsListField] | None = None,
        order_by: GroupSyncProjectMappingsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[GroupSyncProjectMappingsListFilters],
    ) -> Page[GroupMapping]:
        """One page of project mappings in the workspace."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[GroupSyncProjectMappingsListField] | None = None,
        order_by: GroupSyncProjectMappingsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[GroupSyncProjectMappingsListFilters],
    ) -> Iterator[GroupMapping]:
        """Every project mapping in the workspace, following pages automatically."""
        return self._iter(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
            slug=slug,
        )

    def retrieve(
        self,
        slug: str,
        mapping: str,
        *,
        fields: Sequence[GroupSyncProjectMappingsRetrieveField] | None = None,
    ) -> GroupMapping:
        return self._retrieve(pk=mapping, params={"fields": fields}, slug=slug)

    def create(
        self,
        slug: str,
        data: CreateGroupMapping,
        *,
        fields: Sequence[GroupSyncProjectMappingsCreateField] | None = None,
    ) -> GroupMapping:
        return self._create(data, params={"fields": fields}, slug=slug)

    def update(
        self,
        slug: str,
        mapping: str,
        data: UpdateGroupMapping,
        *,
        fields: Sequence[GroupSyncProjectMappingsUpdateField] | None = None,
    ) -> GroupMapping:
        return self._update(data, pk=mapping, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, mapping: str) -> None:
        return self._delete(pk=mapping, slug=slug)
