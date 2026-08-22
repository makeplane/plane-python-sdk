"""Work item attachments (api_v2). `create` returns presigned upload instructions;
`update(..., WorkItemAttachmentConfirm(is_uploaded=True))` marks it uploaded.
This resource only covers the metadata lifecycle, not the upload itself."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ....models.v2.work_items import (
    CreateWorkItemAttachment,
    WorkItemAttachment,
    WorkItemAttachmentConfirm,
    WorkItemAttachmentUploadResult,
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
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Page[WorkItemAttachment]:
        """One page of attachments on a work item."""
        return self._list(work_item_id=work_item_id, params={"fields": fields, **filters})

    def iterate(
        self,
        work_item_id: str,
        *,
        fields: Sequence[str] | None = None,
        **filters: Any,
    ) -> Iterator[WorkItemAttachment]:
        """Every attachment on a work item, following pages automatically."""
        return self._iter(work_item_id=work_item_id, params={"fields": fields, **filters})

    def retrieve(
        self,
        work_item_id: str,
        attachment_id: str,
        *,
        fields: Sequence[str] | None = None,
    ) -> WorkItemAttachment:
        return self._retrieve(
            pk=attachment_id, work_item_id=work_item_id, params={"fields": fields}
        )

    def create(
        self, work_item_id: str, data: CreateWorkItemAttachment
    ) -> WorkItemAttachmentUploadResult:
        """Registers the metadata and returns presigned upload instructions.
        Golden documents a bare `WorkItemAttachment`; live server returns this richer envelope."""
        payload = self.transport.request(
            "POST",
            self._collection_url(work_item_id=work_item_id),
            params=self._query(None, action="create"),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return WorkItemAttachmentUploadResult.model_validate(payload)

    def update(
        self, work_item_id: str, attachment_id: str, data: WorkItemAttachmentConfirm
    ) -> WorkItemAttachment:
        return self._update(data, pk=attachment_id, work_item_id=work_item_id)

    def delete(self, work_item_id: str, attachment_id: str) -> None:
        return self._delete(pk=attachment_id, work_item_id=work_item_id)
