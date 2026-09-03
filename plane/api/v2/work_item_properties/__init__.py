"""Work item properties (api_v2): custom field definitions on work items.
`WorkItemProperties` (project-scoped) and `WorkspaceWorkItemProperties` are
independent resources, each with its own `.options`; the workspace one also has `.contexts`."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_item_properties import (
    CreateWorkItemProperty,
    UpdateWorkItemProperty,
    WorkItemProperty,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .contexts import WorkItemPropertyContexts
from .options import WorkItemPropertyOptions
from .workspace_options import WorkspaceWorkItemPropertyOptions

__all__ = [
    "WorkItemPropertyContexts",
    "WorkItemPropertyOptions",
    "WorkItemProperties",
    "WorkspaceWorkItemPropertyOptions",
    "WorkspaceWorkItemProperties",
]


class WorkItemProperties(
    V2Resource[WorkItemProperty, CreateWorkItemProperty, UpdateWorkItemProperty]
):
    """Project-scoped property definitions."""

    path = "/workspaces/{slug}/projects/{project_id}/work-item-properties/"
    model = WorkItemProperty
    operations = {
        "list": "work_item_properties_list",
        "retrieve": "work_item_properties_retrieve",
        "create": "work_item_properties_create",
        "update": "work_item_properties_partial_update",
        "delete": "work_item_properties_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.options = WorkItemPropertyOptions(transport, **self._scope)

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[WorkItemProperty]:
        """One page of this project's property definitions."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[WorkItemProperty]:
        """Every property definition in this project, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self, property_id: str, *, fields: Sequence[str] | None = None
    ) -> WorkItemProperty:
        return self._retrieve(pk=property_id, params={"fields": fields})

    def find_by_name(self, name: str) -> WorkItemProperty:
        """The one property definition whose key is `name`; raises if none or
        several match. `name` is the property key (e.g. `story_points`), not the
        label shown in the app (`display_name`) -- the API has no label filter
        yet."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateWorkItemProperty) -> WorkItemProperty:
        return self._create(data)

    def update(self, property_id: str, data: UpdateWorkItemProperty) -> WorkItemProperty:
        return self._update(data, pk=property_id)

    def delete(self, property_id: str) -> None:
        return self._delete(pk=property_id)


class WorkspaceWorkItemProperties(
    V2Resource[WorkItemProperty, CreateWorkItemProperty, UpdateWorkItemProperty]
):
    """Workspace-scoped property definitions -- not project-scoped, distinct from
    `WorkItemProperties` in the golden (own operationIds, own path)."""

    path = "/workspaces/{slug}/work-item-properties/"
    model = WorkItemProperty
    operations = {
        "list": "workspace_work_item_properties_list",
        "retrieve": "workspace_work_item_properties_retrieve",
        "create": "workspace_work_item_properties_create",
        "update": "workspace_work_item_properties_partial_update",
        "delete": "workspace_work_item_properties_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.contexts = WorkItemPropertyContexts(transport, **self._scope)
        self.options = WorkspaceWorkItemPropertyOptions(transport, **self._scope)

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[WorkItemProperty]:
        """One page of this workspace's property definitions."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[WorkItemProperty]:
        """Every property definition in this workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self, property_id: str, *, fields: Sequence[str] | None = None
    ) -> WorkItemProperty:
        return self._retrieve(pk=property_id, params={"fields": fields})

    def find_by_name(self, name: str) -> WorkItemProperty:
        """The one property definition whose key is `name`; raises if none or
        several match. `name` is the property key (e.g. `story_points`), not the
        label shown in the app (`display_name`) -- the API has no label filter
        yet."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateWorkItemProperty) -> WorkItemProperty:
        return self._create(data)

    def update(self, property_id: str, data: UpdateWorkItemProperty) -> WorkItemProperty:
        return self._update(data, pk=property_id)

    def delete(self, property_id: str) -> None:
        return self._delete(pk=property_id)
