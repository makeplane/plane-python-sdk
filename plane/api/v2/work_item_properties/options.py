"""Options on a project-scoped work item property (api_v2). Only meaningful for
OPTION-type properties. No `?fields=` here -- options always return in full."""

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


class WorkItemPropertyOptions(
    V2Resource[WorkItemPropertyOption, CreateWorkItemPropertyOption, UpdateWorkItemPropertyOption]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-item-properties/{property_id}/options/"
    model = WorkItemPropertyOption
    operations = {
        "list": "work_item_property_options_list",
        "retrieve": "work_item_property_options_retrieve",
        "create": "work_item_property_options_create",
        "update": "work_item_property_options_partial_update",
        "delete": "work_item_property_options_destroy",
    }

    def list(self, property_id: str, **filters: Any) -> Page[WorkItemPropertyOption]:
        """One page of a property's options."""
        return self._list(property_id=property_id, params=filters)

    def iterate(self, property_id: str, **filters: Any) -> Iterator[WorkItemPropertyOption]:
        """Every option on a property, following pages automatically."""
        return self._iter(property_id=property_id, params=filters)

    def retrieve(self, property_id: str, option_id: str) -> WorkItemPropertyOption:
        return self._retrieve(pk=option_id, property_id=property_id)

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
