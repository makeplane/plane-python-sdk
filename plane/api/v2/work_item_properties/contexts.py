"""Contexts on a workspace-scoped work item property (api_v2). A context is a
per-scope override: which projects/work item types it applies to, and its
default value/requiredness there."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_item_properties import (
    CreateWorkItemPropertyContext,
    UpdateWorkItemPropertyContext,
    WorkItemPropertyContext,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemPropertyContexts(
    V2Resource[
        WorkItemPropertyContext, CreateWorkItemPropertyContext, UpdateWorkItemPropertyContext
    ]
):
    path = "/workspaces/{slug}/work-item-properties/{property_id}/contexts/"
    model = WorkItemPropertyContext
    operations = {
        "list": "work_item_property_contexts_list",
        "retrieve": "work_item_property_contexts_retrieve",
        "create": "work_item_property_contexts_create",
        "update": "work_item_property_contexts_partial_update",
        "delete": "work_item_property_contexts_destroy",
    }

    def list(
        self,
        property_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemPropertyContext]:
        """One page of a workspace property's contexts."""
        return self._list(property_id=property_id, params={"fields": fields, **filters})

    def iterate(
        self,
        property_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItemPropertyContext]:
        """Every context on a workspace property, following pages automatically."""
        return self._iter(property_id=property_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        property_id: str,
        context_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkItemPropertyContext:
        return self._retrieve(pk=context_id, property_id=property_id, params={"fields": fields})

    def find_by_name(self, property_id: str, name: str) -> WorkItemPropertyContext:
        """The one context on this property with this name; raises if none or
        several match."""
        return self._find_one(filters={"name": name}, property_id=property_id)

    def create(
        self, property_id: str, data: CreateWorkItemPropertyContext
    ) -> WorkItemPropertyContext:
        return self._create(data, property_id=property_id)

    def update(
        self,
        property_id: str,
        context_id: str,
        data: UpdateWorkItemPropertyContext,
    ) -> WorkItemPropertyContext:
        return self._update(data, pk=context_id, property_id=property_id)

    def delete(self, property_id: str, context_id: str) -> None:
        return self._delete(pk=context_id, property_id=property_id)
