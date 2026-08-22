"""Custom properties attached to a work item type (project- and workspace-scoped).
`attach` POSTs to the *collection* URL, returning `{"properties": [...]}`, not a
`WorkItemProperty` row; `detach` is a plain `_delete` by property id."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_item_types import (
    WorkItemProperty,
    WorkItemPropertyAttach,
    WorkItemPropertyAttachResult,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemTypeProperties(
    V2Resource[WorkItemProperty, WorkItemPropertyAttach, WorkItemPropertyAttach]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-item-types/{type_id}/properties/"
    model = WorkItemProperty
    operations = {
        "list": "work_item_type_properties_list",
        "retrieve": "work_item_type_properties_retrieve",
        "attach": "work_item_type_properties_attach",
        "detach": "work_item_type_properties_detach",
    }

    def list(
        self,
        type_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemProperty]:
        """One page of custom properties attached to a work item type."""
        return self._list(type_id=type_id, params={"fields": fields, **filters})

    def iterate(
        self,
        type_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItemProperty]:
        """Every custom property attached to a work item type, following pages
        automatically."""
        return self._iter(type_id=type_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        type_id: str,
        property_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkItemProperty:
        return self._retrieve(pk=property_id, type_id=type_id, params={"fields": fields})

    def attach(
        self, type_id: str, property_ids: Sequence[str]
    ) -> WorkItemPropertyAttachResult:
        """Attach existing property definitions to this work item type."""
        payload = self.transport.request(
            "POST",
            self._collection_url(type_id=type_id),
            json=WorkItemPropertyAttach(properties=list(property_ids)).model_dump(
                exclude_none=True
            ),
        )
        return WorkItemPropertyAttachResult.model_validate(payload)

    def detach(self, type_id: str, property_id: str) -> None:
        """Detach a property definition from this work item type."""
        return self._delete(pk=property_id, type_id=type_id)


class WorkspaceWorkItemTypeProperties(
    V2Resource[WorkItemProperty, WorkItemPropertyAttach, WorkItemPropertyAttach]
):
    path = "/workspaces/{slug}/work-item-types/{type_id}/properties/"
    model = WorkItemProperty
    operations = {
        "list": "workspace_work_item_type_properties_list",
        "retrieve": "workspace_work_item_type_properties_retrieve",
        "attach": "workspace_work_item_type_properties_attach",
        "detach": "workspace_work_item_type_properties_detach",
    }

    def list(
        self,
        type_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemProperty]:
        """One page of custom properties attached to a workspace-level work item
        type."""
        return self._list(type_id=type_id, params={"fields": fields, **filters})

    def iterate(
        self,
        type_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItemProperty]:
        """Every custom property attached to a workspace-level work item type,
        following pages automatically."""
        return self._iter(type_id=type_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        type_id: str,
        property_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkItemProperty:
        return self._retrieve(pk=property_id, type_id=type_id, params={"fields": fields})

    def attach(
        self, type_id: str, property_ids: Sequence[str]
    ) -> WorkItemPropertyAttachResult:
        """Attach existing property definitions to this workspace-level work item
        type."""
        payload = self.transport.request(
            "POST",
            self._collection_url(type_id=type_id),
            json=WorkItemPropertyAttach(properties=list(property_ids)).model_dump(
                exclude_none=True
            ),
        )
        return WorkItemPropertyAttachResult.model_validate(payload)

    def detach(self, type_id: str, property_id: str) -> None:
        """Detach a property definition from this workspace-level work item type."""
        return self._delete(pk=property_id, type_id=type_id)
