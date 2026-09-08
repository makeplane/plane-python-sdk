"""Work item comments (api_v2) -- the depth-3 exemplar: every method takes
`slug, project, work_item` as its leading path ids."""

from __future__ import annotations

import builtins
from collections.abc import Iterator, Mapping, Sequence

from typing_extensions import Unpack

from ....models.v2.common import BulkWriteResponse
from ....models.v2.work_items import CreateWorkItemComment, UpdateWorkItemComment, WorkItemComment
from .._generated.constants import (
    CommentsCreateField,
    CommentsListField,
    CommentsListFilters,
    CommentsListOrderBy,
    CommentsPartialUpdateField,
    CommentsRetrieveField,
    WorkItemCommentsUpsertField,
)
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
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[CommentsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: CommentsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[CommentsListFilters],
    ) -> Page[WorkItemComment]:
        """One page of comments on a work item."""
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
            project_id=project,
            work_item_id=work_item,
        )

    def iterate(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[CommentsListField] | None = None,
        expand: Sequence[str] | None = None,
        order_by: CommentsListOrderBy | None = None,
        **filters: Unpack[CommentsListFilters],
    ) -> Iterator[WorkItemComment]:
        """Every comment on a work item, following pages automatically."""
        return self._iter(
            params={"fields": fields, "expand": expand, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        work_item: str,
        comment: str,
        *,
        fields: Sequence[CommentsRetrieveField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemComment:
        return self._retrieve(
            pk=comment,
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
        data: CreateWorkItemComment,
        *,
        fields: Sequence[CommentsCreateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemComment:
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
        comment: str,
        data: UpdateWorkItemComment,
        *,
        fields: Sequence[CommentsPartialUpdateField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemComment:
        return self._update(
            data,
            pk=comment,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def delete(self, slug: str, project: str, work_item: str, comment: str) -> None:
        return self._delete(pk=comment, slug=slug, project_id=project, work_item_id=work_item)

    def upsert(
        self,
        slug: str,
        project: str,
        work_item: str,
        data: CreateWorkItemComment,
        *,
        fields: Sequence[WorkItemCommentsUpsertField] | None = None,
        expand: Sequence[str] | None = None,
    ) -> WorkItemComment:
        """Reconciles on (external_source, external_id) when both are set."""
        return self._upsert(
            data,
            params={"fields": fields, "expand": expand},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def bulk_create(
        self,
        slug: str,
        project: str,
        work_item: str,
        items: builtins.list[CreateWorkItemComment],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_create(
            items,
            all_or_none=all_or_none,
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def bulk_update(
        self,
        slug: str,
        project: str,
        work_item: str,
        items: builtins.list[Mapping[str, object]],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        """Each item is `{"id": <uuid>, ...fields to change}`."""
        return self._bulk_update(
            items,
            all_or_none=all_or_none,
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def bulk_delete(
        self,
        slug: str,
        project: str,
        work_item: str,
        ids: builtins.list[str],
        *,
        all_or_none: bool = False,
    ) -> BulkWriteResponse:
        return self._bulk_delete(
            ids,
            all_or_none=all_or_none,
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )
