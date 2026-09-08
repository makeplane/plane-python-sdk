"""Contexts on a workspace-scoped work item property (api_v2). A context is a
per-scope override: which projects/work item types it applies to, and its
default value/requiredness there."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_item_properties import (
    CreateWorkItemPropertyContext,
    UpdateWorkItemPropertyContext,
    WorkItemPropertyContext,
)
from .._generated.constants import (
    WorkItemPropertyContextsCreateField,
    WorkItemPropertyContextsListField,
    WorkItemPropertyContextsListFilters,
    WorkItemPropertyContextsListOrderBy,
    WorkItemPropertyContextsPartialUpdateField,
    WorkItemPropertyContextsRetrieveField,
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
        slug: str,
        property: str,
        *,
        fields: Sequence[WorkItemPropertyContextsListField] | None = None,
        order_by: WorkItemPropertyContextsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkItemPropertyContextsListFilters],
    ) -> Page[WorkItemPropertyContext]:
        """One page of a workspace property's contexts."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            property_id=property,
        )

    def iterate(
        self,
        slug: str,
        property: str,
        *,
        fields: Sequence[WorkItemPropertyContextsListField] | None = None,
        order_by: WorkItemPropertyContextsListOrderBy | None = None,
        **filters: Unpack[WorkItemPropertyContextsListFilters],
    ) -> Iterator[WorkItemPropertyContext]:
        """Every context on a workspace property, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            property_id=property,
        )

    def retrieve(
        self,
        slug: str,
        property: str,
        context: str,
        *,
        fields: Sequence[WorkItemPropertyContextsRetrieveField] | None = None,
    ) -> WorkItemPropertyContext:
        return self._retrieve(
            pk=context, params={"fields": fields}, slug=slug, property_id=property
        )

    def find_by_name(self, slug: str, property: str, name: str) -> WorkItemPropertyContext:
        """The one context on this property with this name; raises if none or
        several match."""
        return self._find_one(filters={"name": name}, slug=slug, property_id=property)

    def create(
        self,
        slug: str,
        property: str,
        data: CreateWorkItemPropertyContext,
        *,
        fields: Sequence[WorkItemPropertyContextsCreateField] | None = None,
    ) -> WorkItemPropertyContext:
        return self._create(data, params={"fields": fields}, slug=slug, property_id=property)

    def update(
        self,
        slug: str,
        property: str,
        context: str,
        data: UpdateWorkItemPropertyContext,
        *,
        fields: Sequence[WorkItemPropertyContextsPartialUpdateField] | None = None,
    ) -> WorkItemPropertyContext:
        return self._update(
            data, pk=context, params={"fields": fields}, slug=slug, property_id=property
        )

    def delete(self, slug: str, property: str, context: str) -> None:
        return self._delete(pk=context, slug=slug, property_id=property)
