"""Offline coverage for `work_items`; exercises the `_action` verb helper and the non-paginated
relations/dependencies shape."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_items import WorkItems
from plane.config import Configuration
from plane.models.v2.work_items import (
    CreateWorkItem,
    CreateWorkItemComment,
    UpdateWorkItem,
    UpdateWorkItemComment,
    WorkItemDependencyCreate,
    WorkItemRelationCreate,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items"


@pytest.fixture
def work_items(config: Configuration) -> WorkItems:
    return WorkItems(V2Transport(config), slug="acme", project_id="ENG")


# -- CRUD -------------------------------------------------------------------


@responses.activate
def test_list_work_items(work_items: WorkItems) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "name": "Fix bug", "identifier": "ENG-1"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = work_items.list()

    assert page.total_count == 1
    assert page.data[0].identifier == "ENG-1"


@responses.activate
def test_list_passes_expand_and_filters(work_items: WorkItems) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    work_items.list(expand=["state", "labels"], priority="urgent")

    query = responses.calls[0].request.url
    assert "expand=state%2Clabels" in query
    assert "priority=urgent" in query


def test_list_rejects_unknown_expand_before_the_request(work_items: WorkItems) -> None:
    with pytest.raises(ValueError, match="bogus"):
        work_items.list(expand=["bogus"])


@responses.activate
def test_retrieve_work_item(work_items: WorkItems) -> None:
    responses.get(f"{BASE}/wi-1/", json={"id": "wi-1", "name": "Fix bug"})

    row = work_items.retrieve("wi-1")

    assert row.id == "wi-1"


@responses.activate
def test_create_prefers_readable_fields(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/", json={"id": "wi-1", "name": "Fix bug"}, status=201)

    work_items.create(
        CreateWorkItem(name="Fix bug", state="Todo", labels=["bug"], assignees=["a@b.com"]),
    )

    body = json.loads(responses.calls[0].request.body)
    assert body == {
        "name": "Fix bug",
        "state": "Todo",
        "labels": ["bug"],
        "assignees": ["a@b.com"],
    }


@responses.activate
def test_update_uses_patch(work_items: WorkItems) -> None:
    responses.patch(f"{BASE}/wi-1/", json={"id": "wi-1", "name": "Renamed"})

    updated = work_items.update("wi-1", UpdateWorkItem(name="Renamed"))

    assert updated.name == "Renamed"


@responses.activate
def test_delete_returns_none(work_items: WorkItems) -> None:
    responses.delete(f"{BASE}/wi-1/", status=204)

    assert work_items.delete("wi-1") is None


@responses.activate
def test_upsert(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/upsert/", json={"id": "wi-1", "name": "Fix bug"})

    assert work_items.upsert(CreateWorkItem(name="Fix bug")).id == "wi-1"


@responses.activate
def test_bulk_create(work_items: WorkItems) -> None:
    responses.post(
        f"{BASE}/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = work_items.bulk_create([CreateWorkItem(name="A")])

    assert result.succeeded == 1


@responses.activate
def test_bulk_update(work_items: WorkItems) -> None:
    responses.post(
        f"{BASE}/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = work_items.bulk_update([{"id": "1", "name": "B"}])

    assert result.succeeded == 1


@responses.activate
def test_bulk_delete(work_items: WorkItems) -> None:
    responses.post(
        f"{BASE}/bulk-delete/",
        json={
            "results": [{"index": 0, "result": "deleted", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = work_items.bulk_delete(["1"])

    assert result.succeeded == 1


# -- archive/unarchive (_action) ------------------------------------------------


@responses.activate
def test_archive_posts_to_archive_sub_path_and_returns_the_row(work_items: WorkItems) -> None:
    responses.post(
        f"{BASE}/wi-1/archive/", json={"id": "wi-1", "archived_at": "2026-01-01T00:00:00Z"}
    )

    row = work_items.archive("wi-1")

    assert row.id == "wi-1"
    assert row.archived_at is not None


@responses.activate
def test_unarchive_posts_to_unarchive_sub_path(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/wi-1/unarchive/", json={"id": "wi-1", "archived_at": None})

    row = work_items.unarchive("wi-1")

    assert row.id == "wi-1"
    assert row.archived_at is None


# -- Sub-resources: comments (full CRUD + its own upsert/bulk) -----------------


@responses.activate
def test_comments_crud(work_items: WorkItems) -> None:
    responses.get(
        f"{BASE}/wi-1/comments/",
        json={
            "data": [{"id": "c1", "comment_html": "<p>hi</p>"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{BASE}/wi-1/comments/", json={"id": "c1", "comment_html": "<p>hi</p>"}, status=201
    )
    responses.get(f"{BASE}/wi-1/comments/c1/", json={"id": "c1", "comment_html": "<p>hi</p>"})
    responses.patch(f"{BASE}/wi-1/comments/c1/", json={"id": "c1", "comment_html": "<p>bye</p>"})
    responses.delete(f"{BASE}/wi-1/comments/c1/", status=204)

    page = work_items.comments.list("wi-1")
    assert page.data[0].id == "c1"

    created = work_items.comments.create("wi-1", CreateWorkItemComment(comment_html="<p>hi</p>"))
    assert created.id == "c1"

    fetched = work_items.comments.retrieve("wi-1", "c1")
    assert fetched.id == "c1"

    updated = work_items.comments.update(
        "wi-1", "c1", UpdateWorkItemComment(comment_html="<p>bye</p>")
    )
    assert updated.comment_html == "<p>bye</p>"

    assert work_items.comments.delete("wi-1", "c1") is None


@responses.activate
def test_comments_upsert(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/wi-1/comments/upsert/", json={"id": "c1", "comment_html": "<p>hi</p>"})

    result = work_items.comments.upsert("wi-1", CreateWorkItemComment(comment_html="<p>hi</p>"))

    assert result.id == "c1"


@responses.activate
def test_comments_have_their_own_bulk_operations(work_items: WorkItems) -> None:
    """Comments' bulk ops (`work_item_comments_bulk_*`) are distinct operationIds
    from the parent work item's own bulk ops -- this hits the comments sub-path,
    not the work-items one."""
    responses.post(
        f"{BASE}/wi-1/comments/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "c1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = work_items.comments.bulk_create(
        "wi-1", [CreateWorkItemComment(comment_html="<p>hi</p>")]
    )

    assert result.succeeded == 1
    assert "/comments/bulk-create/" in responses.calls[0].request.url


# -- Sub-resources: attachments (no expand) -------------------------------------


@responses.activate
def test_attachments_crud(work_items: WorkItems) -> None:
    responses.get(
        f"{BASE}/wi-1/attachments/",
        json={"data": [{"id": "a1", "name": "log.txt"}], "pagination": {"style": "offset"}},
    )
    responses.post(
        f"{BASE}/wi-1/attachments/",
        json={
            "asset_id": "a1",
            "asset_url": "/api/assets/v2/.../a1/",
            "upload_data": {"url": "https://s3.example.com", "fields": {"key": "a1"}},
            "attachment": {"id": "a1", "name": "log.txt"},
        },
    )
    responses.patch(f"{BASE}/wi-1/attachments/a1/", json={"id": "a1", "is_uploaded": True})
    responses.delete(f"{BASE}/wi-1/attachments/a1/", status=204)

    from plane.models.v2.work_items import CreateWorkItemAttachment, WorkItemAttachmentConfirm

    page = work_items.attachments.list("wi-1")
    assert page.data[0].name == "log.txt"

    created = work_items.attachments.create(
        "wi-1", CreateWorkItemAttachment(name="log.txt", size=10)
    )
    assert created.asset_id == "a1"
    assert created.attachment.id == "a1"
    assert created.upload_data["url"] == "https://s3.example.com"

    updated = work_items.attachments.update(
        "wi-1", "a1", WorkItemAttachmentConfirm(is_uploaded=True)
    )
    assert updated.is_uploaded is True

    assert work_items.attachments.delete("wi-1", "a1") is None


# -- Sub-resources: links -----------------------------------------------------


@responses.activate
def test_links_crud(work_items: WorkItems) -> None:
    from plane.models.v2.work_items import CreateWorkItemLink, UpdateWorkItemLink

    responses.post(f"{BASE}/wi-1/links/", json={"id": "l1", "url": "https://x.test"}, status=201)
    responses.patch(f"{BASE}/wi-1/links/l1/", json={"id": "l1", "url": "https://y.test"})
    responses.delete(f"{BASE}/wi-1/links/l1/", status=204)

    created = work_items.links.create("wi-1", CreateWorkItemLink(url="https://x.test"))
    assert created.id == "l1"

    updated = work_items.links.update("wi-1", "l1", UpdateWorkItemLink(url="https://y.test"))
    assert updated.url == "https://y.test"

    assert work_items.links.delete("wi-1", "l1") is None


# -- Sub-resources: worklogs (has expand) --------------------------------------


@responses.activate
def test_worklogs_crud_and_expand(work_items: WorkItems) -> None:
    from plane.models.v2.work_items import CreateWorkItemWorklog

    responses.get(
        f"{BASE}/wi-1/worklogs/",
        json={"data": [{"id": "w1", "duration": 60}], "pagination": {"style": "offset"}},
    )
    responses.post(f"{BASE}/wi-1/worklogs/", json={"id": "w1", "duration": 60}, status=201)

    page = work_items.worklogs.list("wi-1", expand=["logged_by"])
    assert page.data[0].duration == 60
    assert "expand=logged_by" in responses.calls[0].request.url

    created = work_items.worklogs.create("wi-1", CreateWorkItemWorklog(duration=60))
    assert created.id == "w1"


def test_worklogs_reject_unknown_expand(work_items: WorkItems) -> None:
    with pytest.raises(ValueError, match="bogus"):
        work_items.worklogs.list("wi-1", expand=["bogus"])


# -- Sub-resources: activities (read-only) --------------------------------------


@responses.activate
def test_activities_are_read_only(work_items: WorkItems) -> None:
    responses.get(
        f"{BASE}/wi-1/activities/",
        json={"data": [{"id": "act1", "verb": "updated"}], "pagination": {"style": "offset"}},
    )
    responses.get(f"{BASE}/wi-1/activities/act1/", json={"id": "act1", "verb": "updated"})

    page = work_items.activities.list("wi-1")
    assert page.data[0].verb == "updated"

    fetched = work_items.activities.retrieve("wi-1", "act1")
    assert fetched.id == "act1"

    # No create/update/delete methods exist on the resource at all.
    assert not hasattr(work_items.activities, "create")
    assert not hasattr(work_items.activities, "delete")


# -- Sub-resources: relations (non-paginated, delete-by-related-id) ------------


@responses.activate
def test_relations_list_returns_the_dict_shaped_object_not_a_page(work_items: WorkItems) -> None:
    responses.get(f"{BASE}/wi-1/relations/", json={"blocks": ["wi-2"], "blocked_by": []})

    result = work_items.relations.list("wi-1")

    assert result.model_extra == {"blocks": ["wi-2"], "blocked_by": []}


@responses.activate
def test_relations_create(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/wi-1/relations/", json={"blocks": ["wi-2"]}, status=201)

    result = work_items.relations.create(
        "wi-1",
        WorkItemRelationCreate(
            direction="outward", relation_definition_id="rd-1", work_item_ids=["wi-2"]
        ),
    )

    body = json.loads(responses.calls[0].request.body)
    assert body == {
        "direction": "outward",
        "relation_definition_id": "rd-1",
        "work_item_ids": ["wi-2"],
    }
    assert result.model_extra == {"blocks": ["wi-2"]}


@responses.activate
def test_relations_delete_is_by_related_work_item_id_not_a_row_pk(work_items: WorkItems) -> None:
    responses.delete(f"{BASE}/wi-1/relations/wi-2/", status=204)

    assert work_items.relations.delete("wi-1", "wi-2") is None
    assert responses.calls[0].request.url.endswith("/relations/wi-2/")


# -- Sub-resources: dependencies (fixed six directions) -------------------------


@responses.activate
def test_dependencies_list_has_the_six_fixed_directions(work_items: WorkItems) -> None:
    responses.get(
        f"{BASE}/wi-1/dependencies/",
        json={
            "blocked_by": ["wi-2"],
            "blocking": [],
            "start_after": [],
            "start_before": [],
            "finish_after": [],
            "finish_before": [],
        },
    )

    result = work_items.dependencies.list("wi-1")

    assert result.blocked_by == ["wi-2"]
    assert result.blocking == []


@responses.activate
def test_dependencies_create(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/wi-1/dependencies/", json={"blocked_by": ["wi-2"]}, status=201)

    work_items.dependencies.create(
        "wi-1",
        WorkItemDependencyCreate(relation_type="blocked_by", work_item_ids=["wi-2"]),
    )

    body = json.loads(responses.calls[0].request.body)
    assert body == {"relation_type": "blocked_by", "work_item_ids": ["wi-2"]}


@responses.activate
def test_dependencies_delete_is_by_related_work_item_id(work_items: WorkItems) -> None:
    responses.delete(f"{BASE}/wi-1/dependencies/wi-2/", status=204)

    assert work_items.dependencies.delete("wi-1", "wi-2") is None
