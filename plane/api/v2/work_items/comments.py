"""Work item comments (api_v2)."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence
from typing import Any

from ....models.v2.common import BulkWriteResponse
from ....models.v2.work_items import CreateWorkItemComment, UpdateWorkItemComment, WorkItemComment
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemComments(V2Resource[WorkItemComment, CreateWorkItemComment, UpdateWorkItemComment]):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/comments/"
    model = WorkItemComment
    operations = {
        "list": "comments_list",
        "retrieve": "comments_retrieve",
        "create": "comments_create",
        "update": "comments_partial_update",
        "upsert": "work_item_comments_upsert",
        "delete": "comments_destroy",
        "bulk_create": "work_item_comments_bulk_create",
        "bulk_update": "work_item_comments_bulk_update",
        "bulk_delete": "work_item_comments_bulk_delete",
    }

    def list(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemComment]:
        """One page of comments on a work item."""
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
    ) -> Iterator[WorkItemComment]:
        """Every comment on a work item, following pages automatically."""
        return self._iter(
            work_item_id=work_item_id,
            params={"fields": fields, "expand": expand, **filters},
        )

    def retrieve(
        self,
        work_item_id: str,
        comment_id: str,
        *,
        fields: Sequence[str] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemComment:
        return self._retrieve(
            pk=comment_id,
            work_item_id=work_item_id,
            params={"fields": fields, "expand": expand},
        )

    def create(self, work_item_id: str, data: CreateWorkItemComment) -> WorkItemComment:
        return self._create(data, work_item_id=work_item_id)

    def update(
        self, work_item_id: str, comment_id: str, data: UpdateWorkItemComment
    ) -> WorkItemComment:
        return self._update(data, pk=comment_id, work_item_id=work_item_id)

    def delete(self, work_item_id: str, comment_id: str) -> None:
        return self._delete(pk=comment_id, work_item_id=work_item_id)

    def upsert(self, work_item_id: str, data: CreateWorkItemComment) -> WorkItemComment:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(data, work_item_id=work_item_id)

    def bulk_create(
        self,
        work_item_id: str,
        items: builtins.list[CreateWorkItemComment],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(items, all_or_none=all_or_none, work_item_id=work_item_id)

    def bulk_update(
        self,
        work_item_id: str,
        items: builtins.list[Mapping[str, Any]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(items, all_or_none=all_or_none, work_item_id=work_item_id)

    def bulk_delete(
        self,
        work_item_id: str,
        ids: builtins.list[str],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_delete(ids, all_or_none=all_or_none, work_item_id=work_item_id)
