"""Work item activities (api_v2). Read-only -- the API never lets a caller write
an activity row directly; they are generated as a side effect of other writes."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_items import WorkItemActivity
from .._kernel.pagination import Page
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
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemActivity]:
        """One page of activity entries on a work item."""
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
    ) -> Iterator[WorkItemActivity]:
        """Every activity entry on a work item, following pages automatically."""
        return self._iter(
            work_item_id=work_item_id,
            params={"fields": fields, "expand": expand, **filters},
        )

    def retrieve(
        self,
        work_item_id: str,
        activity_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemActivity:
        return self._retrieve(
            pk=activity_id,
            work_item_id=work_item_id,
            params={"fields": fields, "expand": expand},
        )
