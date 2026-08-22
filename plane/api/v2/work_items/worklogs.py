"""Work item worklogs (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_items import CreateWorkItemWorklog, UpdateWorkItemWorklog, WorkItemWorklog
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemWorklogs(V2Resource[WorkItemWorklog, CreateWorkItemWorklog, UpdateWorkItemWorklog]):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/worklogs/"
    model = WorkItemWorklog
    operations = {
        "list": "worklogs_list",
        "retrieve": "worklogs_retrieve",
        "create": "worklogs_create",
        "update": "worklogs_partial_update",
        "delete": "worklogs_destroy",
    }

    def list(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemWorklog]:
        """One page of worklogs on a work item."""
        return self._list(
            work_item_id=work_item_id,
            params={"fields": fields, "expand": expand, **filters},
        )

    def iterate(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItemWorklog]:
        """Every worklog on a work item, following pages automatically."""
        return self._iter(
            work_item_id=work_item_id,
            params={"fields": fields, "expand": expand, **filters},
        )

    def retrieve(
        self,
        work_item_id: str,
        worklog_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemWorklog:
        return self._retrieve(
            pk=worklog_id,
            work_item_id=work_item_id,
            params={"fields": fields, "expand": expand},
        )

    def create(self, work_item_id: str, data: CreateWorkItemWorklog) -> WorkItemWorklog:
        return self._create(data, work_item_id=work_item_id)

    def update(
        self, work_item_id: str, worklog_id: str, data: UpdateWorkItemWorklog
    ) -> WorkItemWorklog:
        return self._update(data, pk=worklog_id, work_item_id=work_item_id)

    def delete(self, work_item_id: str, worklog_id: str) -> None:
        return self._delete(pk=worklog_id, work_item_id=work_item_id)
