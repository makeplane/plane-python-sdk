"""Work item types (api_v2) -- `WorkItemTypes` (project-scoped) and
`WorkspaceWorkItemTypes` are a different path template, not a filtered view of
each other. Both expose `.properties`; `enable`/`import_types`/`schema` are project-only."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_item_types import (
    CreateWorkItemType,
    UpdateWorkItemType,
    WorkItemType,
    WorkItemTypeImport,
    WorkItemTypeSchema,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .properties import WorkItemTypeProperties, WorkspaceWorkItemTypeProperties

__all__ = [
    "WorkItemTypeProperties",
    "WorkItemTypes",
    "WorkspaceWorkItemTypeProperties",
    "WorkspaceWorkItemTypes",
]


class WorkItemTypes(V2Resource[WorkItemType, CreateWorkItemType, UpdateWorkItemType]):
    path = "/workspaces/{slug}/projects/{project_id}/work-item-types/"
    model = WorkItemType
    operations = {
        "list": "work_item_types_list",
        "retrieve": "work_item_types_retrieve",
        "create": "work_item_types_create",
        "update": "work_item_types_partial_update",
        "enable": "work_item_types_enable",
        "mark-default": "work_item_types_mark_default",
        "delete": "work_item_types_destroy",
        "import_types": "work_item_types_import",
        "schema": "work_item_types_schema",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.properties = WorkItemTypeProperties(transport, **self._scope)

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[WorkItemType]:
        """One page of work item types in this project."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[WorkItemType]:
        """Every work item type in this project, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self, type_id: str, *, fields: Sequence[str] | None = None
    ) -> WorkItemType:
        return self._retrieve(pk=type_id, params={"fields": fields})

    def find_by_name(self, name: str) -> WorkItemType:
        """The one work item type with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateWorkItemType) -> WorkItemType:
        return self._create(data)

    def update(self, type_id: str, data: UpdateWorkItemType) -> WorkItemType:
        return self._update(data, pk=type_id)

    def delete(self, type_id: str) -> None:
        return self._delete(pk=type_id)

    def enable(self, *, fields: Sequence[str] | None = None) -> WorkItemType:
        """Enable this project's epic/system work item type (idempotent).
        Collection-level, not per-row -- there is no `{pk}` in
        `.../work-item-types/enable/`."""
        payload = self.transport.request(
            "POST",
            f"{self._collection_url()}enable/",
            params=self._query({"fields": fields}, action="enable"),
        )
        return self.model.model_validate(payload)

    def import_types(self, type_ids: builtins.list[str]) -> None:
        """Import the given (global/system) work item type ids into this project."""
        self.transport.request(
            "POST",
            f"{self._collection_url()}import/",
            json=WorkItemTypeImport(work_item_types=list(type_ids)).model_dump(
                mode="json", exclude_none=True
            ),
        )
        return None

    def mark_default(
        self, type_id: str, *, fields: Sequence[str] | None = None
    ) -> WorkItemType:
        """Make this the project's default work item type for new work items."""
        return self._action("mark-default", pk=type_id, params={"fields": fields})

    def schema(self, type_id: str, *, include: str | None = None) -> WorkItemTypeSchema:
        """The type's writable standard fields (with options inline) plus its
        custom properties -- what a client needs to build a create/update form."""
        params = {"include": include} if include is not None else None
        payload = self.transport.request(
            "GET", f"{self._detail_url(type_id)}schema/", params=params
        )
        return WorkItemTypeSchema.model_validate(payload)


class WorkspaceWorkItemTypes(V2Resource[WorkItemType, CreateWorkItemType, UpdateWorkItemType]):
    path = "/workspaces/{slug}/work-item-types/"
    model = WorkItemType
    operations = {
        "list": "workspace_work_item_types_list",
        "retrieve": "workspace_work_item_types_retrieve",
        "create": "workspace_work_item_types_create",
        "update": "workspace_work_item_types_partial_update",
        "mark-default": "workspace_work_item_types_mark_default",
        "delete": "workspace_work_item_types_destroy",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.properties = WorkspaceWorkItemTypeProperties(transport, **self._scope)

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[WorkItemType]:
        """One page of work item types across the whole workspace."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[WorkItemType]:
        """Every work item type in the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, type_id: str, *, fields: Sequence[str] | None = None) -> WorkItemType:
        return self._retrieve(pk=type_id, params={"fields": fields})

    def find_by_name(self, name: str) -> WorkItemType:
        """The one workspace-level type with this name; raises if none or several match."""
        return self._find_one(filters={"name": name})

    def create(self, data: CreateWorkItemType) -> WorkItemType:
        return self._create(data)

    def update(self, type_id: str, data: UpdateWorkItemType) -> WorkItemType:
        return self._update(data, pk=type_id)

    def delete(self, type_id: str) -> None:
        return self._delete(pk=type_id)

    def mark_default(
        self, type_id: str, *, fields: Sequence[str] | None = None
    ) -> WorkItemType:
        """Make this the workspace's default work item type."""
        return self._action("mark-default", pk=type_id, params={"fields": fields})
