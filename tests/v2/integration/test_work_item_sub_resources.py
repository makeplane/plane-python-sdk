"""All seven of a work item's children against a real server -- comments,
attachments, links, worklogs, activities, relations and dependencies.

The file the loaded-row design exists for: every one of these is reached off the
loaded `work_item`, so the work item id is written once, when it is fetched, and
never again. It reads the way the README claims the surface reads."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
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

from ._guard import skip_absent_capability
from .helpers import unique_name


@pytest.fixture(scope="module")
def work_item(project: LoadedProject) -> Iterator[Any]:
    """One work item shared by every test in this module, as a loaded row -- every
    child below hangs off it and cleans up its own rows, so nothing here depends on
    test order."""
    created = project.work_items.create(CreateWorkItem(name=unique_name("wi-subresources")))
    yield created
    try:
        project.work_items.delete(created.id)
    except Exception:
        pass


@pytest.fixture(scope="module")
def other_work_item(project: LoadedProject) -> Iterator[Any]:
    """A second work item to relate/depend the first one on."""
    created = project.work_items.create(CreateWorkItem(name=unique_name("wi-subresources-other")))
    yield created
    try:
        project.work_items.delete(created.id)
    except Exception:
        pass


class TestComments:
    def test_crud(self, project: LoadedProject, work_item: Any) -> None:
        created = work_item.comments.create(CreateWorkItemComment(comment_html="<p>hi</p>"))
        try:
            assert created.work_item_id == work_item.id

            fetched = work_item.comments.retrieve(created.id)
            assert fetched.id == created.id

            page = work_item.comments.list()
            assert any(c.id == created.id for c in page.data)

            updated = work_item.comments.update(
                created.id, UpdateWorkItemComment(comment_html="<p>bye</p>")
            )
            assert updated.comment_html == "<p>bye</p>"
        finally:
            work_item.comments.delete(created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            work_item.comments.retrieve(created.id)
        assert exc_info.value.status == 404

    def test_upsert_creates_then_reconciles(self, project: LoadedProject, work_item: Any) -> None:
        marker = unique_name("comment-upsert")
        first = work_item.comments.upsert(
            CreateWorkItemComment(
                comment_html="<p>v1</p>", external_source=marker, external_id="1"
            ),
        )
        try:
            second = work_item.comments.upsert(
                CreateWorkItemComment(
                    comment_html="<p>v2</p>", external_source=marker, external_id="1"
                ),
            )
            assert second.id == first.id
            assert second.comment_html == "<p>v2</p>"
        finally:
            work_item.comments.delete(first.id)

    def test_bulk_create_update_delete(self, project: LoadedProject, work_item: Any) -> None:
        items = [CreateWorkItemComment(comment_html=f"<p>{i}</p>") for i in range(2)]
        created = work_item.comments.bulk_create(items)
        created.raise_for_failures()
        ids = [row.id for row in created.results]
        try:
            updated = work_item.comments.bulk_update(
                [{"id": pk, "comment_html": "<p>updated</p>"} for pk in ids],
            )
            assert updated.succeeded == 2
        finally:
            deleted = work_item.comments.bulk_delete(ids)
            assert deleted.succeeded == 2


class TestAttachments:
    def test_create_then_confirm_then_delete(self, project: LoadedProject, work_item: Any) -> None:
        created = work_item.attachments.create(
            CreateWorkItemAttachment(name="log.txt", size=42, type="text/plain"),
        )
        # The golden documents a bare `WorkItemAttachment` for this operation, but
        # the live server returns a richer envelope -- verified here against a real
        # plane-dev instance; see `WorkItemAttachmentUploadResult`'s docstring.
        assert created.asset_id
        assert created.upload_data  # presigned S3 POST fields to upload the bytes to
        attachment_id = created.attachment.id
        try:
            fetched = work_item.attachments.retrieve(attachment_id)
            assert fetched.id == attachment_id

            page = work_item.attachments.list()
            assert any(a.id == attachment_id for a in page.data)

            confirmed = work_item.attachments.update(
                attachment_id, WorkItemAttachmentConfirm(is_uploaded=True)
            )
            assert confirmed.is_uploaded is True
        finally:
            work_item.attachments.delete(attachment_id)


class TestLinks:
    def test_crud(self, project: LoadedProject, work_item: Any) -> None:
        created = work_item.links.create(CreateWorkItemLink(url="https://example.com/a"))
        try:
            assert created.url == "https://example.com/a"

            updated = work_item.links.update(
                created.id, UpdateWorkItemLink(url="https://example.com/b")
            )
            assert updated.url == "https://example.com/b"

            page = work_item.links.list()
            assert any(link.id == created.id for link in page.data)
        finally:
            work_item.links.delete(created.id)


class TestWorklogs:
    def test_crud(self, project: LoadedProject, work_item: Any) -> None:
        created = work_item.worklogs.create(
            CreateWorkItemWorklog(duration=30, description="investigating"),
        )
        try:
            assert created.duration == 30

            updated = work_item.worklogs.update(created.id, UpdateWorkItemWorklog(duration=45))
            assert updated.duration == 45

            page = work_item.worklogs.list()
            assert any(w.id == created.id for w in page.data)
        finally:
            work_item.worklogs.delete(created.id)


class TestActivities:
    def test_list_and_retrieve_after_a_write(self, project: LoadedProject, work_item: Any) -> None:
        # Renaming generates an activity row -- read-only, so this is the only way
        # to guarantee at least one exists.
        project.work_items.update(work_item.id, UpdateWorkItem(name=unique_name("wi-activity")))

        page = work_item.activities.list()
        assert len(page.data) > 0

        first = page.data[0]
        fetched = work_item.activities.retrieve(first.id)
        assert fetched.id == first.id


@pytest.fixture(scope="module")
def relation_definition_id(client: PlaneClient, workspace_slug: str) -> str:
    try:
        # Through the resource, not `transport.request`: hand-rolling the request
        # skips `_query`'s validation and hand-parses the envelope.
        rows = client.v2.workspaces.work_item_relation_definitions.list(
            workspace_slug, per_page=5
        ).data
    except PlaneAPIError as exc:
        if exc.status == 402:
            skip_absent_capability("CUSTOM_RELATIONS is not enabled on this workspace")
        raise
    if not rows:
        skip_absent_capability("workspace has no relation definitions seeded")
    return str(rows[0].id)


class TestRelations:
    def test_create_list_and_delete_by_related_id(
        self,
        client: PlaneClient,
        workspace_slug: str,
        work_item: Any,
        other_work_item: Any,
        relation_definition_id: str,
    ) -> None:
        # Through the resource rather than `transport.request`: a hand-rolled request
        # skips `_query`'s validation and is exactly the bypass CLAUDE.md rules out.
        definition = client.v2.workspaces.work_item_relation_definitions.retrieve(
            workspace_slug, relation_definition_id
        )
        direction = definition.outward
        assert direction is not None

        work_item.relations.create(
            WorkItemRelationCreate(
                direction=direction,
                relation_definition_id=relation_definition_id,
                work_item_ids=[other_work_item.id],
            ),
        )
        try:
            result = work_item.relations.list()
            all_related_ids = {rid for ids in result.model_extra.values() for rid in ids}
            assert other_work_item.id in all_related_ids
        finally:
            work_item.relations.delete(other_work_item.id)

        result_after = work_item.relations.list()
        all_related_ids_after = {rid for ids in result_after.model_extra.values() for rid in ids}
        assert other_work_item.id not in all_related_ids_after


class TestDependencies:
    def test_create_list_and_delete_by_related_id(
        self,
        work_item: Any,
        other_work_item: Any,
    ) -> None:
        work_item.dependencies.create(
            WorkItemDependencyCreate(
                relation_type="blocked_by", work_item_ids=[other_work_item.id]
            ),
        )
        try:
            result = work_item.dependencies.list()
            assert other_work_item.id in result.blocked_by
        finally:
            work_item.dependencies.delete(other_work_item.id)

        result_after = work_item.dependencies.list()
        assert other_work_item.id not in result_after.blocked_by
