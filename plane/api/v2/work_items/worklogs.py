"""Work item worklogs (api_v2)."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_items import CreateWorkItemWorklog, UpdateWorkItemWorklog, WorkItemWorklog
from .._generated.constants import (
    WorklogsCreateField,
    WorklogsListField,
    WorklogsListFilters,
    WorklogsListOrderBy,
    WorklogsPartialUpdateField,
    WorklogsRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
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
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[WorklogsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorklogsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[WorklogsListFilters],
    ) -> Page[WorkItemWorklog]:
        """One page of worklogs on a work item."""
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
            project_id=project,
            work_item_id=work_item,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[WorklogsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: WorklogsListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[WorklogsListFilters],
    ) -> Iterator[WorkItemWorklog]:
        """Every worklog on a work item, following pages automatically."""
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
            project_id=project,
            work_item_id=work_item,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        work_item: str,
        worklog: str,
        *,
        fields: Sequence[WorklogsRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemWorklog:
        return self._retrieve(
            pk=worklog,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def create(
        self,
        slug: str,
        project: str,
        work_item: str,
        data: CreateWorkItemWorklog,
        *,
        fields: Sequence[WorklogsCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemWorklog:
        return self._create(
            data,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def update(
        self,
        slug: str,
        project: str,
        work_item: str,
        worklog: str,
        data: UpdateWorkItemWorklog,
        *,
        fields: Sequence[WorklogsPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemWorklog:
        return self._update(
            data,
            pk=worklog,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def delete(self, slug: str, project: str, work_item: str, worklog: str) -> None:
        return self._delete(pk=worklog, slug=slug, project_id=project, work_item_id=work_item)
