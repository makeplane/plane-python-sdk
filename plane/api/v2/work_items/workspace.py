"""Workspace-wide work item listing (api_v2). No project id in the path, unlike
`proj.work_items`. Also carries `retrieve_by_identifier` (by human-readable key,
e.g. `"ENG-12"`); list-only, no create/update/delete."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_items import CreateWorkItem, UpdateWorkItem, WorkItem
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource

__all__ = ["WorkspaceWorkItems"]


class WorkspaceWorkItems(V2Resource[WorkItem, CreateWorkItem, UpdateWorkItem]):
    path = "/workspaces/{slug}/work-items/"
    model = WorkItem
    operations = {
        "list": "workspace_work_items_list",
        "retrieve_by_identifier": "work_items_retrieve_by_identifier",
    }

    def list(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItem]:
        """One page of work items across every project in the workspace the caller
        can view. Same filters as `WorkItems.list`, plus `project_id`/`project_id__in`."""
        return self._list(params={"fields": fields, "expand": expand, **filters})

    def iterate(
        self,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItem]:
        """Every work item across the workspace, following pages automatically."""
        return self._iter(params={"fields": fields, "expand": expand, **filters})

    def retrieve_by_identifier(
        self,
        identifier: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItem:
        """Fetch a work item by its human-readable key (e.g. `"ENG-12"`), with no
        project id needed -- the readable-identifier flagship of api_v2."""
        payload = self.transport.request(
            "GET",
            self._detail_url(identifier),
            params=self._query(
                {"fields": fields, "expand": expand}, action="retrieve_by_identifier"
            ),
        )
        return self.model.model_validate(payload)
