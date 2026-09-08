"""Workspace-wide work item listing (api_v2). No project id in the path, unlike
`proj.work_items`. Also carries `retrieve_by_identifier` (by human-readable key,
e.g. `"ENG-12"`); list-only, no create/update/delete."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_items import CreateWorkItem, UpdateWorkItem, WorkItem
from .._generated.constants import (
    WorkItemsRetrieveByIdentifierField,
    WorkspaceWorkItemsListField,
    WorkspaceWorkItemsListFilters,
    WorkspaceWorkItemsListOrderBy,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource

__all__ = ["WorkspaceWorkItems"]


class WorkspaceWorkItems(V2Resource[WorkItem, CreateWorkItem, UpdateWorkItem]):
    path = "/workspaces/{slug}/work-items/"
    extra_paths = {"retrieve_by_identifier": "/workspaces/{slug}/work-items/{identifier}/"}
    model = WorkItem
    operations = {
        "list": "workspace_work_items_list",
        "retrieve_by_identifier": "work_items_retrieve_by_identifier",
    }

    def list(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceWorkItemsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceWorkItemsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[WorkspaceWorkItemsListFilters],
    ) -> Page[WorkItem]:
        """One page of work items across every project in the workspace the caller
        can view. Same filters as `WorkItems.list`, plus `project_id`/`project_id__in`."""
        return self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                **filters,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[WorkspaceWorkItemsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorkspaceWorkItemsListOrderBy | None = None,
        **filters: Unpack[WorkspaceWorkItemsListFilters],
    ) -> Iterator[WorkItem]:
        """Every work item across the workspace, following pages automatically."""
        return self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
        )

    def retrieve_by_identifier(
        self,
        slug: str,
        identifier: str,
        *,
        fields: Sequence[WorkItemsRetrieveByIdentifierField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItem:
        """Fetch a work item by its human-readable key (e.g. `"ENG-12"`), with no
        project id needed -- the readable-identifier flagship of api_v2. Hits a
        different URL template than `list` -- `extra_paths["retrieve_by_identifier"]`
        (`.../work-items/{identifier}/`), not `path` -- reached via `url_for`."""
        payload = self.transport.request(
            "GET",
            self.url_for("retrieve_by_identifier", slug=slug, identifier=identifier),
            params=self._query(
                {"fields": fields, "expand": expand}, action="retrieve_by_identifier"
            ),
        )
        return self.model.model_validate(payload)
