"""Work items (api_v2) -- the hardest, and largest, api_v2 resource family.
Project-scoped, with `archive`/`unarchive` plus nested `.comments`/`.attachments`/
`.links`/`.worklogs`/`.activities`/`.relations`/`.dependencies`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ....models.v2.common import BulkWriteResponse
from ....models.v2.work_items import CreateWorkItem, UpdateWorkItem, WorkItem
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .activities import WorkItemActivities
from .attachments import WorkItemAttachments
from .comments import WorkItemComments
from .dependencies import WorkItemDependencies
from .links import WorkItemLinks
from .relations import WorkItemRelations
from .worklogs import WorkItemWorklogs
from .workspace import WorkspaceWorkItems

__all__ = [
    "WorkItemActivities",
    "WorkItemAttachments",
    "WorkItemComments",
    "WorkItemDependencies",
    "WorkItemLinks",
    "WorkItemRelations",
    "WorkItemWorklogs",
    "WorkItems",
    "WorkspaceWorkItems",
]


class WorkItems(V2Resource[WorkItem, CreateWorkItem, UpdateWorkItem]):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/"
    model = WorkItem
    operations = {
        "list": "work_items_list",
        "retrieve": "work_items_retrieve",
        "create": "work_items_create",
        "update": "work_items_partial_update",
        "upsert": "work_items_upsert",
        "archive": "work_items_archive",
        "unarchive": "work_items_unarchive",
        "delete": "work_items_destroy",
        "bulk_create": "work_items_bulk_create",
        "bulk_update": "work_items_bulk_update",
        "bulk_delete": "work_items_bulk_delete",
    }

    def __init__(self, transport: V2Transport, **scope: Any) -> None:
        super().__init__(transport, **scope)
        self.comments = WorkItemComments(transport, **self._scope)
        self.attachments = WorkItemAttachments(transport, **self._scope)
        self.links = WorkItemLinks(transport, **self._scope)
        self.worklogs = WorkItemWorklogs(transport, **self._scope)
        self.activities = WorkItemActivities(transport, **self._scope)
        self.relations = WorkItemRelations(transport, **self._scope)
        self.dependencies = WorkItemDependencies(transport, **self._scope)

    # -- CRUD ---------------------------------------------------------------

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItem]:
        """One page of work items in this project.

        `**filters` covers `state_id`, `priority`, `assignee_id__in`, `state_group`, `search`."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItem]:
        """Every work item in this project, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItem:
        """Fetch by UUID. Prefer `ws.work_items.retrieve_by_identifier` when you
        have the human-readable key (e.g. `"ENG-12"`) instead."""
        return self._retrieve(pk=work_item_id, params={"fields": fields, "expand": expand})

    def create(self, data: CreateWorkItem) -> WorkItem:
        """Create a work item. Prefer readable fields over ids where you have them
        (e.g. `CreateWorkItem(name=..., state="Todo", labels=["bug"])`)."""
        return self._create(data)

    def update(self, work_item_id: str, data: UpdateWorkItem) -> WorkItem:
        return self._update(data, pk=work_item_id)

    def delete(self, work_item_id: str) -> None:
        return self._delete(pk=work_item_id)

    def upsert(self, data: CreateWorkItem) -> WorkItem:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data)

    def bulk_create(
        self, items: builtins.list[CreateWorkItem], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none)

    def bulk_update(
        self, items: builtins.list[Mapping[str, Any]], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none)

    def bulk_delete(
        self, ids: builtins.list[str], *, all_or_none: bool = False
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none)

    # -- Custom verb actions ------------------------------------------------------

    def archive(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItem:
        """Archive a work item, returning it. Only work items in a completed or
        cancelled state can be archived (server-enforced)."""
        return self._action(
            "archive", pk=work_item_id, params={"fields": fields, "expand": expand}
        )

    def unarchive(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItem:
        """Restore an archived work item to active status, returning it."""
        return self._action(
            "unarchive", pk=work_item_id, params={"fields": fields, "expand": expand}
        )
