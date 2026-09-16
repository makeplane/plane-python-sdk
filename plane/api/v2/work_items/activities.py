"""Work item activities (api_v2). Read-only -- the API never lets a caller write
an activity row directly; they are generated as a side effect of other writes."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_items import WorkItemActivity
from .._generated.constants import (
    ActivitiesListField,
    ActivitiesListFilters,
    ActivitiesListOrderBy,
    ActivitiesRetrieveField,
)
from .._kernel.pagination import Page, PaginateStyle
from .._kernel.resource import V2Resource


# No write/patch DTO exists for activities -- the type parameters are filled with
# the read model itself as an unused placeholder: the kernel has no read-only
# resource shape.
class WorkItemActivities(V2Resource[WorkItemActivity, WorkItemActivity, WorkItemActivity]):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/activities/"
    model = WorkItemActivity
    operations = {
        "list": "activities_list",
        "retrieve": "activities_retrieve",
    }

    def list(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[ActivitiesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        count: bool | None = None,
        **filters: Unpack[ActivitiesListFilters],
    ) -> Page[WorkItemActivity]:
        """One page of activity entries on a work item."""
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
        fields: Sequence[ActivitiesListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: ActivitiesListOrderBy | None = None,
        per_page: int | None = None,
        paginate: PaginateStyle | None = None,
        cursor: str | None = None,
        **filters: Unpack[ActivitiesListFilters],
    ) -> Iterator[WorkItemActivity]:
        """Every activity entry on a work item, following pages automatically."""
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
        activity: str,
        *,
        fields: Sequence[ActivitiesRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemActivity:
        return self._retrieve(
            pk=activity,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )
