"""Workspace-wide work item listing (api_v2). No project id in the path, unlike
`proj.work_items` -- which is also why its rows come back as plain `WorkItem`s
rather than the navigable `LoadedWorkItem`s every other work-item fetch answers;
see the class docstring. Also carries `retrieve_by_identifier` (by human-readable
key, e.g. `"ENG-12"`); list-only, no create/update/delete."""

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
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource

__all__ = ["WorkspaceWorkItems"]


class WorkspaceWorkItems(V2Resource[WorkItem, CreateWorkItem, UpdateWorkItem]):
    """The one class in the package that answers a *bare* row of a navigable type.

    Everywhere else, a method returning a row of a type some resource loads returns
    the loaded form -- mixing the two on one class silently drops navigation, which
    is why CLAUDE.md states it as an absolute. This resource is the structural
    exception, not an oversight.

    A `LoadedWorkItem`'s children live at
    `.../projects/{project_id}/work-items/{work_item_id}/comments/` -- three path ids,
    `("slug", "project", "work_item")`. This resource's URL band has two of them: its
    template names `{slug}` only, and the row contributes its own id. The project
    segment is not in the band at all, so there is nothing for `loaded_names` to bind
    it from, and `Owned` would refuse the call outright -- it compares a child
    method's leading parameter names against `loaded_names` literally and raises
    `TypeError` rather than prepending `("slug", "work_item")` into
    `("slug", "project", ...)`.

    The row does carry `project_id` as a *field*, and reading the path id off it is
    the tempting fix. It is the wrong one: `?fields=` and collection deferral can
    both omit a field, so navigation would work or raise `FieldNotRequested`
    depending on the caller's projection -- a path id that exists only sometimes.
    Presence is deliberately not something the tree is allowed to depend on.

    So: rows from here are plain `WorkItem`s. To navigate, go through the
    project-scoped band, which has the full URL: `client.v2.workspaces.projects`
    `.work_items.retrieve(slug, project, work_item)`, or off a loaded row,
    `workspace.projects.retrieve("ENG").work_items.retrieve("ENG-12").comments`.
    """

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
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorkspaceWorkItemsListFilters],
    ) -> Page[WorkItem]:
        """One page of work items across every project in the workspace the caller
        can view. Same filters as `WorkItems.list`, plus `project_id`/`project_id__in`.

        Rows are plain `WorkItem`s, not `LoadedWorkItem`s -- see the class
        docstring for why this route cannot bind the project id its children need."""
        return self._list(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
                "paginate": paginate,
                "cursor": cursor,
                "count": count,
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
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorkspaceWorkItemsListFilters],
    ) -> Iterator[WorkItem]:
        """Every work item across the workspace, following pages automatically.
        Yields plain `WorkItem`s -- see the class docstring."""
        return self._iter(
            params={
                "fields": fields,
                "expand": expand,
                "order_by": order_by,
                "per_page": per_page,
                "paginate": paginate,
                "cursor": cursor,
                **filters,
            },
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
        (`.../work-items/{identifier}/`), not `path` -- reached via `url_for`.

        A plain `WorkItem`, for the same reason as `list`: no project segment to bind."""
        return self._custom_action(
            "retrieve_by_identifier",
            model=WorkItem,
            method="GET",
            params={"fields": fields, "expand": expand},
            slug=slug,
            identifier=identifier,
        )
