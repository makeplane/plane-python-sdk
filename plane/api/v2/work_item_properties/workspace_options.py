"""Options on a workspace-scoped work item property (api_v2). Only meaningful for
OPTION-type properties; like the project-scoped sibling, no `?fields=` here."""

from __future__ import annotations

from collections.abc import Iterator

from typing_extensions import Unpack

from ....models.v2.work_item_properties import (
    CreateWorkItemPropertyOption,
    UpdateWorkItemPropertyOption,
    WorkItemPropertyOption,
)
from .._generated.constants import (
    WorkspaceWorkItemPropertyOptionsListFilters,
    WorkspaceWorkItemPropertyOptionsListOrderBy,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkspaceWorkItemPropertyOptions(
    V2Resource[WorkItemPropertyOption, CreateWorkItemPropertyOption, UpdateWorkItemPropertyOption]
):
    path = "/workspaces/{slug}/work-item-properties/{property_id}/options/"
    model = WorkItemPropertyOption
    operations = {
        "list": "workspace_work_item_property_options_list",
        "retrieve": "workspace_work_item_property_options_retrieve",
        "create": "workspace_work_item_property_options_create",
        "update": "workspace_work_item_property_options_partial_update",
        "delete": "workspace_work_item_property_options_destroy",
    }

    def list(
        self,
        slug: str,
        property: str,
        *,
        order_by: WorkspaceWorkItemPropertyOptionsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkspaceWorkItemPropertyOptionsListFilters],
    ) -> Page[WorkItemPropertyOption]:
        """One page of a workspace property's options."""
        return self._list(
            params={"order_by": order_by, "per_page": per_page, "offset": offset, **filters},
            slug=slug,
            property_id=property,
        )

    def iterate(
        self,
        slug: str,
        property: str,
        *,
        order_by: WorkspaceWorkItemPropertyOptionsListOrderBy | None = None,
        **filters: Unpack[WorkspaceWorkItemPropertyOptionsListFilters],
    ) -> Iterator[WorkItemPropertyOption]:
        """Every option on a workspace property, following pages automatically."""
        return self._iter(params={"order_by": order_by, **filters}, slug=slug, property_id=property)

    def retrieve(self, slug: str, property: str, option: str) -> WorkItemPropertyOption:
        return self._retrieve(pk=option, slug=slug, property_id=property)

    def find_by_name(self, slug: str, property: str, name: str) -> WorkItemPropertyOption:
        """The one option on this property with this name; raises if none or
        several match."""
        return self._find_one(filters={"name": name}, slug=slug, property_id=property)

    def create(
        self, slug: str, property: str, data: CreateWorkItemPropertyOption
    ) -> WorkItemPropertyOption:
        return self._create(data, slug=slug, property_id=property)

    def update(
        self, slug: str, property: str, option: str, data: UpdateWorkItemPropertyOption
    ) -> WorkItemPropertyOption:
        return self._update(data, pk=option, slug=slug, property_id=property)

    def delete(self, slug: str, property: str, option: str) -> None:
        return self._delete(pk=option, slug=slug, property_id=property)
