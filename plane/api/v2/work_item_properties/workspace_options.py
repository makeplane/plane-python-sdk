"""Options on a workspace-scoped work item property (api_v2). Only meaningful for
OPTION-type properties; like the project-scoped sibling, no `?fields=` here."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

from ....models.v2.work_item_properties import (
    CreateWorkItemPropertyOption,
    UpdateWorkItemPropertyOption,
    WorkItemPropertyOption,
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

    def list(self, property_id: str, **filters: Any) -> Page[WorkItemPropertyOption]:
        """One page of a workspace property's options."""
        return self._list(property_id=property_id, params=filters)

    def iterate(self, property_id: str, **filters: Any) -> Iterator[WorkItemPropertyOption]:
        """Every option on a workspace property, following pages automatically."""
        return self._iter(property_id=property_id, params=filters)

    def retrieve(self, property_id: str, option_id: str) -> WorkItemPropertyOption:
        return self._retrieve(pk=option_id, property_id=property_id)

    def find_by_name(self, property_id: str, name: str) -> WorkItemPropertyOption:
        """The one option on this property with this name; raises if none or
        several match."""
        return self._find_one(filters={"name": name}, property_id=property_id)

    def create(
        self, property_id: str, data: CreateWorkItemPropertyOption
    ) -> WorkItemPropertyOption:
        return self._create(data, property_id=property_id)

    def update(
        self,
        property_id: str,
        option_id: str,
        data: UpdateWorkItemPropertyOption,
    ) -> WorkItemPropertyOption:
        return self._update(data, pk=option_id, property_id=property_id)

    def delete(self, property_id: str, option_id: str) -> None:
        return self._delete(pk=option_id, property_id=property_id)
