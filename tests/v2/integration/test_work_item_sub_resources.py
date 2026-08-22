"""Every work-item sub-resource against a real server: comments, attachments,
links, worklogs, activities (read-only), relations, and dependencies."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.work_items import (
    CreateWorkItem,
    CreateWorkItemAttachment,
    CreateWorkItemComment,
    CreateWorkItemLink,
    CreateWorkItemWorklog,
    UpdateWorkItem,
    UpdateWorkItemComment,
    UpdateWorkItemLink,
    UpdateWorkItemWorklog,
    WorkItemAttachmentConfirm,
    WorkItemDependencyCreate,
    WorkItemRelationCreate,
)

from .helpers import unique_name


@pytest.fixture(scope="module")
def work_item(client: PlaneClient, workspace_slug: str, project_id: str) -> Iterator[Any]:
    """One work item shared by every test in this module -- sub-resources hang off
    it and clean up their own rows, so nothing here depends on test order."""
    proj = client.v2.workspace(workspace_slug).project(project_id)
    created = proj.work_items.create(CreateWorkItem(name=unique_name("wi-subresources")))
    yield created
    try:
        proj.work_items.delete(created.id)
    except Exception:
        pass


@pytest.fixture(scope="module")
def other_work_item(client: PlaneClient, workspace_slug: str, project_id: str) -> Iterator[Any]:
    """A second work item to relate/depend the first one on."""
    proj = client.v2.workspace(workspace_slug).project(project_id)
    created = proj.work_items.create(CreateWorkItem(name=unique_name("wi-subresources-other")))
    yield created
    try:
        proj.work_items.delete(created.id)
    except Exception:
        pass


class TestComments:
    def test_crud(
        self, client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        created = proj.work_items.comments.create(
            work_item.id, CreateWorkItemComment(comment_html="<p>hi</p>")
        )
        try:
            assert created.work_item_id == work_item.id

            fetched = proj.work_items.comments.retrieve(work_item.id, created.id)
            assert fetched.id == created.id

            page = proj.work_items.comments.list(work_item.id)
            assert any(c.id == created.id for c in page.data)

            updated = proj.work_items.comments.update(
                work_item.id, created.id, UpdateWorkItemComment(comment_html="<p>bye</p>")
            )
            assert updated.comment_html == "<p>bye</p>"
        finally:
            proj.work_items.comments.delete(work_item.id, created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            proj.work_items.comments.retrieve(work_item.id, created.id)
        assert exc_info.value.status == 404

    def test_upsert_creates_then_reconciles(
        self, client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        marker = unique_name("comment-upsert")
        first = proj.work_items.comments.upsert(
            work_item.id,
            CreateWorkItemComment(
                comment_html="<p>v1</p>", external_source=marker, external_id="1"
            ),
        )
        try:
            second = proj.work_items.comments.upsert(
                work_item.id,
                CreateWorkItemComment(
                    comment_html="<p>v2</p>", external_source=marker, external_id="1"
                ),
            )
            assert second.id == first.id
            assert second.comment_html == "<p>v2</p>"
        finally:
            proj.work_items.comments.delete(work_item.id, first.id)

    def test_bulk_create_update_delete(
        self, client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        items = [CreateWorkItemComment(comment_html=f"<p>{i}</p>") for i in range(2)]
        created = proj.work_items.comments.bulk_create(work_item.id, items)
        created.raise_for_failures()
        ids = [row.id for row in created.results]
        try:
            updated = proj.work_items.comments.bulk_update(
                work_item.id,
                [{"id": pk, "comment_html": "<p>updated</p>"} for pk in ids],
            )
            assert updated.succeeded == 2
        finally:
            deleted = proj.work_items.comments.bulk_delete(work_item.id, ids)
            assert deleted.succeeded == 2


class TestAttachments:
    def test_create_then_confirm_then_delete(
        self, client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        created = proj.work_items.attachments.create(
            work_item.id,
            CreateWorkItemAttachment(name="log.txt", size=42, type="text/plain"),
        )
        # The golden documents a bare `WorkItemAttachment` for this operation, but
        # the live server returns a richer envelope -- verified here against a real
        # plane-dev instance; see `WorkItemAttachmentUploadResult`'s docstring.
        assert created.asset_id
        assert created.upload_data  # presigned S3 POST fields to upload the bytes to
        attachment_id = created.attachment.id
        try:
            fetched = proj.work_items.attachments.retrieve(work_item.id, attachment_id)
            assert fetched.id == attachment_id

            page = proj.work_items.attachments.list(work_item.id)
            assert any(a.id == attachment_id for a in page.data)

            confirmed = proj.work_items.attachments.update(
                work_item.id, attachment_id, WorkItemAttachmentConfirm(is_uploaded=True)
            )
            assert confirmed.is_uploaded is True
        finally:
            proj.work_items.attachments.delete(work_item.id, attachment_id)


class TestLinks:
    def test_crud(
        self, client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        created = proj.work_items.links.create(
            work_item.id, CreateWorkItemLink(url="https://example.com/a")
        )
        try:
            assert created.url == "https://example.com/a"

            updated = proj.work_items.links.update(
                work_item.id, created.id, UpdateWorkItemLink(url="https://example.com/b")
            )
            assert updated.url == "https://example.com/b"

            page = proj.work_items.links.list(work_item.id)
            assert any(link.id == created.id for link in page.data)
        finally:
            proj.work_items.links.delete(work_item.id, created.id)


class TestWorklogs:
    def test_crud(
        self, client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        created = proj.work_items.worklogs.create(
            work_item.id,
            CreateWorkItemWorklog(duration=30, description="investigating"),
        )
        try:
            assert created.duration == 30

            updated = proj.work_items.worklogs.update(
                work_item.id, created.id, UpdateWorkItemWorklog(duration=45)
            )
            assert updated.duration == 45

            page = proj.work_items.worklogs.list(work_item.id)
            assert any(w.id == created.id for w in page.data)
        finally:
            proj.work_items.worklogs.delete(work_item.id, created.id)


class TestActivities:
    def test_list_and_retrieve_after_a_write(
        self, client: PlaneClient, workspace_slug: str, project_id: str, work_item: Any
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        # Renaming generates an activity row -- read-only, so this is the only way
        # to guarantee at least one exists.
        proj.work_items.update(work_item.id, UpdateWorkItem(name=unique_name("wi-activity")))

        page = proj.work_items.activities.list(work_item.id)
        assert len(page.data) > 0

        first = page.data[0]
        fetched = proj.work_items.activities.retrieve(work_item.id, first.id)
        assert fetched.id == first.id


@pytest.fixture(scope="module")
def relation_definition_id(client: PlaneClient, workspace_slug: str) -> str:
    try:
        payload = client.v2.transport.request(
            "GET",
            f"/workspaces/{workspace_slug}/work-item-relation-definitions/",
            params={"per_page": 5},
        )
    except PlaneAPIError as exc:
        if exc.status == 402:
            pytest.skip("CUSTOM_RELATIONS not enabled on this workspace")
        raise
    data = payload.get("data", [])
    if not data:
        pytest.skip("workspace has no relation definitions seeded")
    return str(data[0]["id"])


class TestRelations:
    def test_create_list_and_delete_by_related_id(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        work_item: Any,
        other_work_item: Any,
        relation_definition_id: str,
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        payload = client.v2.transport.request(
            "GET",
            f"/workspaces/{workspace_slug}/work-item-relation-definitions/{relation_definition_id}/",
        )
        direction = payload["outward"]

        proj.work_items.relations.create(
            work_item.id,
            WorkItemRelationCreate(
                direction=direction,
                relation_definition_id=relation_definition_id,
                work_item_ids=[other_work_item.id],
            ),
        )
        try:
            result = proj.work_items.relations.list(work_item.id)
            all_related_ids = {rid for ids in result.model_extra.values() for rid in ids}
            assert other_work_item.id in all_related_ids
        finally:
            proj.work_items.relations.delete(work_item.id, other_work_item.id)

        result_after = proj.work_items.relations.list(work_item.id)
        all_related_ids_after = {rid for ids in result_after.model_extra.values() for rid in ids}
        assert other_work_item.id not in all_related_ids_after


class TestDependencies:
    def test_create_list_and_delete_by_related_id(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        work_item: Any,
        other_work_item: Any,
    ) -> None:
        proj = client.v2.workspace(workspace_slug).project(project_id)
        proj.work_items.dependencies.create(
            work_item.id,
            WorkItemDependencyCreate(
                relation_type="blocked_by", work_item_ids=[other_work_item.id]
            ),
        )
        try:
            result = proj.work_items.dependencies.list(work_item.id)
            assert other_work_item.id in result.blocked_by
        finally:
            proj.work_items.dependencies.delete(work_item.id, other_work_item.id)

        result_after = proj.work_items.dependencies.list(work_item.id)
        assert other_work_item.id not in result_after.blocked_by
