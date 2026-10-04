"""Unit tests for WorkItemAttachments API resource (smoke tests with real HTTP requests)."""

from collections.abc import Iterator
from contextlib import suppress

import pytest

from plane.client import PlaneClient
from plane.models.projects import Project
from plane.models.work_items import (
    CreateWorkItem,
    UpdateWorkItemAttachment,
    WorkItemAttachmentCreateResponse,
    WorkItemAttachmentUploadRequest,
)


class TestWorkItemAttachmentsAPI:
    """Test WorkItemAttachments API resource."""

    @pytest.fixture
    def work_item_id(
        self, client: PlaneClient, workspace_slug: str, project: Project
    ) -> Iterator[str]:
        """Create a work item for attachment tests and clean it up after."""
        work_item = client.work_items.create(
            workspace_slug,
            project.id,
            CreateWorkItem(name="Attachment test work item"),
        )
        yield work_item.id
        with suppress(Exception):
            client.work_items.delete(workspace_slug, project.id, work_item.id)

    def test_list_empty(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item_id: str
    ) -> None:
        """Newly created work item should have no attachments."""
        attachments = client.work_items.attachments.list(workspace_slug, project.id, work_item_id)
        assert attachments == []

    def test_create_returns_wrapper(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item_id: str
    ) -> None:
        """Create should return wrapper with both attachment record and S3 upload policy."""
        result = client.work_items.attachments.create(
            workspace_slug,
            project.id,
            work_item_id,
            WorkItemAttachmentUploadRequest(name="test.txt", size=12, type="text/plain"),
        )
        try:
            assert isinstance(result, WorkItemAttachmentCreateResponse)
            assert result.attachment.id is not None
            assert result.attachment.asset
            assert not result.attachment.is_uploaded
            assert "url" in result.upload_data
            assert "fields" in result.upload_data
        finally:
            with suppress(Exception):
                client.work_items.attachments.delete(
                    workspace_slug, project.id, work_item_id, result.attachment.id
                )

    def test_full_lifecycle(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item_id: str
    ) -> None:
        """Create -> mark uploaded -> list -> delete."""
        created = client.work_items.attachments.create(
            workspace_slug,
            project.id,
            work_item_id,
            WorkItemAttachmentUploadRequest(name="lifecycle.txt", size=20, type="text/plain"),
        )
        attachment_id = created.attachment.id
        assert attachment_id is not None

        try:
            # Plane filters list to is_uploaded=True only — mark uploaded first.
            updated = client.work_items.attachments.update(
                workspace_slug,
                project.id,
                work_item_id,
                attachment_id,
                UpdateWorkItemAttachment(is_uploaded=True),
            )
            assert updated.id == attachment_id
            assert updated.is_uploaded is True

            listed = client.work_items.attachments.list(workspace_slug, project.id, work_item_id)
            assert any(a.id == attachment_id for a in listed)
        finally:
            with suppress(Exception):
                client.work_items.attachments.delete(
                    workspace_slug, project.id, work_item_id, attachment_id
                )
