"""Work items (api_v2) -- the hardest, and largest, api_v2 resource family.
Project-scoped, with `archive`/`unarchive` plus nested `.comments`/`.attachments`/
`.links`/`.worklogs`/`.activities`/`.relations`/`.dependencies`.

A fetched row (`retrieve`/`create`, and every row in a `list` page) comes back as
a `LoadedWorkItem`: it carries the row's data and can reach every child -- `.comments`,
`.attachments`, `.links`, `.worklogs`, `.activities`, `.relations`, `.dependencies` --
without the caller repeating `slug`/`project`/`work_item`."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ....models.v2.common import BulkWriteResponse
from ....models.v2.work_items import CreateWorkItem, UpdateWorkItem, WorkItem
from .._generated.constants import (
    WorkItemsArchiveField,
    WorkItemsCreateField,
    WorkItemsListField,
    WorkItemsListFilters,
    WorkItemsListOrderBy,
    WorkItemsPartialUpdateField,
    WorkItemsRetrieveField,
    WorkItemsUnarchiveField,
    WorkItemsUpsertField,
)
from .._kernel.loaded import LoadsNavigableRows
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource
from .._kernel.transport import V2Transport
from .._loaded.work_item import LoadedWorkItem
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


class WorkItems(
    V2Resource[WorkItem, CreateWorkItem, UpdateWorkItem], LoadsNavigableRows[LoadedWorkItem]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/"
    model = WorkItem
    loaded_model = LoadedWorkItem
    loaded_names = ("slug", "project", "work_item")
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

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.comments = WorkItemComments(transport)
        self.attachments = WorkItemAttachments(transport)
        self.links = WorkItemLinks(transport)
        self.worklogs = WorkItemWorklogs(transport)
        self.activities = WorkItemActivities(transport)
        self.relations = WorkItemRelations(transport)
        self.dependencies = WorkItemDependencies(transport)

    # -- CRUD ---------------------------------------------------------------

    def list(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[WorkItemsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkItemsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkItemsListFilters],
    ) -> Page[LoadedWorkItem]:
        """One page of work items in this project.

        `**filters` covers `state_id`, `priority`, `assignee_id__in`, `state_group`, `search`."""
        page = self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
            project_id=project,
        )
        return self._load_page(page, slug, project, fields=fields)

    def iterate(
        self,
        slug: str,
        project: str,
        *,
        fields: Sequence[WorkItemsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkItemsListOrderBy | None = None,
        **filters: Unpack[WorkItemsListFilters],
    ) -> Iterator[LoadedWorkItem]:
        """Every work item in this project, following pages automatically."""
        rows = self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
        )
        return (self._load(row, slug, project, fields=fields) for row in rows)

    def retrieve(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[WorkItemsRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedWorkItem:
        """Fetch by UUID. Prefer `ws.work_items.retrieve_by_identifier` when you
        have the human-readable key (e.g. `"ENG-12"`) instead."""
        row = self._retrieve(
            pk=work_item,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
        return self._load(row, slug, project, fields=fields)

    def create(
        self,
        slug: str,
        project: str,
        data: CreateWorkItem,
        *,
        fields: Sequence[WorkItemsCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedWorkItem:
        """Create a work item. Prefer readable fields over ids where you have them
        (e.g. `CreateWorkItem(name=..., state="Todo", labels=["bug"])`)."""
        row = self._create(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def update(
        self,
        slug: str,
        project: str,
        work_item: str,
        data: UpdateWorkItem,
        *,
        fields: Sequence[WorkItemsPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedWorkItem:
        row = self._update(
            data,
            pk=work_item,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
        return self._load(row, slug, project, fields=fields)

    def delete(self, slug: str, project: str, work_item: str) -> None:
        return self._delete(pk=work_item, slug=slug, project_id=project)

    def upsert(
        self,
        slug: str,
        project: str,
        data: CreateWorkItem,
        *,
        fields: Sequence[WorkItemsUpsertField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedWorkItem:
        """Reconciles on (external_source, external_id) when both are set."""
        row = self._upsert(
            data, params={"fields": fields, "expand": expand}, slug=slug, project_id=project
        )
        return self._load(row, slug, project, fields=fields)

    def bulk_create(
        self,
        slug: str,
        project: str,
        items: builtins.list[CreateWorkItem],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none, slug=slug, project_id=project)

    def bulk_update(
        self,
        slug: str,
        project: str,
        items: builtins.list[Mapping[str, object]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none, slug=slug, project_id=project)

    def bulk_delete(
        self,
        slug: str,
        project: str,
        ids: builtins.list[str],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none, slug=slug, project_id=project)

    # -- Custom verb actions ------------------------------------------------------

    def archive(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[WorkItemsArchiveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedWorkItem:
        """Archive a work item, returning it. Only work items in a completed or
        cancelled state can be archived (server-enforced).

        Returns a loaded row, like every other method here that answers with a work
        item -- an archived row still navigates to its own children."""
        row = self._action(
            "archive",
            pk=work_item,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
        return self._load(row, slug, project, fields=fields)

    def unarchive(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[WorkItemsUnarchiveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> LoadedWorkItem:
        """Restore an archived work item to active status, returning it."""
        row = self._action(
            "unarchive",
            pk=work_item,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
        )
        return self._load(row, slug, project, fields=fields)
