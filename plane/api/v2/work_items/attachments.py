"""Work item attachments (api_v2). `create` returns presigned upload instructions;
`update(..., WorkItemAttachmentConfirm(is_uploaded=True))` marks it uploaded.
This resource only covers the metadata lifecycle, not the upload itself."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

from typing_extensions import Unpack

from ....models.v2.work_items import (
    CreateWorkItemAttachment,
    WorkItemAttachment,
    WorkItemAttachmentConfirm,
    WorkItemAttachmentUploadResult,
)
from .._generated.constants import (
    AttachmentsListField,
    AttachmentsListFilters,
    AttachmentsListOrderBy,
    AttachmentsPartialUpdateField,
    AttachmentsRetrieveField,
)
from .._kernel.pagination import Page
from .._kernel.resource import V2Resource


class WorkItemAttachments(
    V2Resource[WorkItemAttachment, CreateWorkItemAttachment, WorkItemAttachmentConfirm]
):
    path = "/workspaces/{slug}/projects/{project_id}/work-items/{work_item_id}/attachments/"
    model = WorkItemAttachment
    operations = {
        "list": "attachments_list",
        "retrieve": "attachments_retrieve",
        "create": "attachments_create",
        "update": "attachments_partial_update",
        "delete": "attachments_destroy",
    }

    def list(
        self,
        slug: str,
        project: str,
        work_item: str,
        *,
        fields: Sequence[AttachmentsListField] | None = None,
        order_by: AttachmentsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
        **filters: Unpack[AttachmentsListFilters],
    ) -> Page[WorkItemAttachment]:
        """One page of attachments on a work item."""
        return self._list(
            params={
                "fields": fields,
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
        fields: Sequence[AttachmentsListField] | None = None,
        order_by: AttachmentsListOrderBy | None = None,
        **filters: Unpack[AttachmentsListFilters],
    ) -> Iterator[WorkItemAttachment]:
        """Every attachment on a work item, following pages automatically."""
        return self._iter(
            params={"fields": fields, "order_by": order_by, **filters},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def retrieve(
        self,
        slug: str,
        project: str,
        work_item: str,
        attachment: str,
        *,
        fields: Sequence[AttachmentsRetrieveField] | None = None,
    ) -> WorkItemAttachment:
        return self._retrieve(
            pk=attachment,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def create(
        self, slug: str, project: str, work_item: str, data: CreateWorkItemAttachment
    ) -> WorkItemAttachmentUploadResult:
        """Registers the metadata and returns presigned upload instructions.
        Golden documents a bare `WorkItemAttachment`; live server returns this richer
        envelope -- no `fields` param, since a sparse response could drop data the
        caller needs to complete the upload."""
        return self._custom_action(
            "create",
            model=WorkItemAttachmentUploadResult,
            data=data,
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def update(
        self,
        slug: str,
        project: str,
        work_item: str,
        attachment: str,
        data: WorkItemAttachmentConfirm,
        *,
        fields: Sequence[AttachmentsPartialUpdateField] | None = None,
    ) -> WorkItemAttachment:
        return self._update(
            data,
            pk=attachment,
            params={"fields": fields},
            slug=slug,
            project_id=project,
            work_item_id=work_item,
        )

    def delete(self, slug: str, project: str, work_item: str, attachment: str) -> None:
        return self._delete(pk=attachment, slug=slug, project_id=project, work_item_id=work_item)
