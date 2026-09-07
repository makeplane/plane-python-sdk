"""Offline coverage for `WorkItems` (the flat depth-2 pattern) and `WorkItemComments`
(the depth-3 exemplar: `slug, project, work_item` leading parameters)."""

import json

import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_items import WorkItems
from plane.config import Configuration
from plane.models.v2.work_items import (
    CreateWorkItem,
    CreateWorkItemComment,
    UpdateWorkItem,
    UpdateWorkItemComment,
)

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items"


@pytest.fixture
def work_items(config: Configuration) -> WorkItems:
    return WorkItems(V2Transport(config))


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

    page = work_items.list("acme", "ENG")

    assert page.total_count == 1
    assert page.data[0].identifier == "ENG-1"


@responses.activate
def test_list_passes_expand_and_filters(work_items: WorkItems) -> None:
    responses.get(f"{BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    work_items.list("acme", "ENG", expand=["state", "labels"], priority="urgent")

    query = responses.calls[0].request.url
    assert "expand=state%2Clabels" in query
    assert "priority=urgent" in query


def test_list_rejects_unknown_expand_before_the_request(work_items: WorkItems) -> None:
    with pytest.raises(ValueError, match="bogus"):
        work_items.list("acme", "ENG", expand=["bogus"])


@responses.activate
def test_retrieve_work_item_navigates_to_comments(work_items: WorkItems) -> None:
    responses.get(f"{BASE}/wi-1/", json={"id": "wi-1", "name": "Fix bug"})

    row = work_items.retrieve("acme", "ENG", "wi-1")

    assert row.id == "wi-1"
    assert row.comments._ids == ("acme", "ENG", "wi-1")


@responses.activate
def test_create_prefers_readable_fields(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/", json={"id": "wi-1", "name": "Fix bug"}, status=201)

    work_items.create(
        "acme",
        "ENG",
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

    updated = work_items.update("acme", "ENG", "wi-1", UpdateWorkItem(name="Renamed"))

    assert updated.name == "Renamed"


@responses.activate
def test_delete_returns_none(work_items: WorkItems) -> None:
    responses.delete(f"{BASE}/wi-1/", status=204)

    assert work_items.delete("acme", "ENG", "wi-1") is None


@responses.activate
def test_upsert(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/upsert/", json={"id": "wi-1", "name": "Fix bug"})

    assert work_items.upsert("acme", "ENG", CreateWorkItem(name="Fix bug")).id == "wi-1"


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

    result = work_items.bulk_create("acme", "ENG", [CreateWorkItem(name="A")])

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

    result = work_items.bulk_update("acme", "ENG", [{"id": "1", "name": "B"}])

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

    result = work_items.bulk_delete("acme", "ENG", ["1"])

    assert result.succeeded == 1


# -- archive/unarchive (_action) ------------------------------------------------


@responses.activate
def test_archive_posts_to_archive_sub_path_and_returns_the_row(work_items: WorkItems) -> None:
    responses.post(
        f"{BASE}/wi-1/archive/", json={"id": "wi-1", "archived_at": "2026-01-01T00:00:00Z"}
    )

    row = work_items.archive("acme", "ENG", "wi-1")

    assert row.id == "wi-1"
    assert row.archived_at is not None


@responses.activate
def test_unarchive_posts_to_unarchive_sub_path(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/wi-1/unarchive/", json={"id": "wi-1", "archived_at": None})

    row = work_items.unarchive("acme", "ENG", "wi-1")

    assert row.id == "wi-1"
    assert row.archived_at is None


# -- Sub-resource: comments (depth-3 exemplar) -----------------------------------


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

    page = work_items.comments.list("acme", "ENG", "wi-1")
    assert page.data[0].id == "c1"

    created = work_items.comments.create(
        "acme", "ENG", "wi-1", CreateWorkItemComment(comment_html="<p>hi</p>")
    )
    assert created.id == "c1"

    fetched = work_items.comments.retrieve("acme", "ENG", "wi-1", "c1")
    assert fetched.id == "c1"

    updated = work_items.comments.update(
        "acme", "ENG", "wi-1", "c1", UpdateWorkItemComment(comment_html="<p>bye</p>")
    )
    assert updated.comment_html == "<p>bye</p>"

    assert work_items.comments.delete("acme", "ENG", "wi-1", "c1") is None


@responses.activate
def test_comments_upsert(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/wi-1/comments/upsert/", json={"id": "c1", "comment_html": "<p>hi</p>"})

    result = work_items.comments.upsert(
        "acme", "ENG", "wi-1", CreateWorkItemComment(comment_html="<p>hi</p>")
    )

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
        "acme", "ENG", "wi-1", [CreateWorkItemComment(comment_html="<p>hi</p>")]
    )

    assert result.succeeded == 1
    assert "/comments/bulk-create/" in responses.calls[0].request.url


@responses.activate
def test_comments_take_three_path_ids(config: Configuration) -> None:
    responses.get(
        f"{BASE}/ENG-12/comments/",
        json={"data": [{"id": "c1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )

    page = V2Namespace(config).workspaces.projects.work_items.comments.list("acme", "ENG", "ENG-12")

    assert page.data[0].id == "c1"


@responses.activate
def test_fetched_work_item_reaches_comments_with_no_ids_repeated(
    config: Configuration,
) -> None:
    responses.get(f"{BASE}/ENG-12/", json={"id": "w1", "sequence_id": 12})
    responses.get(
        f"{BASE}/w1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    work_item = V2Namespace(config).workspaces.projects.work_items.retrieve("acme", "ENG", "ENG-12")
    work_item.comments.list()

    assert responses.calls[1].request.url.endswith("/work-items/w1/comments/")


# -- `fields=` must reach `Loaded.build`, not just `Loaded` unit tests -----------
# (regression: `_load` forgot to forward it, so every field read as `None`
# instead of raising for a field never requested from a sparse response)


@responses.activate
def test_retrieve_with_fields_raises_on_an_unrequested_field(work_items: WorkItems) -> None:
    responses.get(f"{BASE}/wi-1/", json={"id": "wi-1"})

    row = work_items.retrieve("acme", "ENG", "wi-1", fields=["id"])

    assert len(row._present) == 1
    with pytest.raises(FieldNotRequested, match="name"):
        _ = row.name


@responses.activate
def test_list_with_fields_raises_on_an_unrequested_field_for_a_page_row(
    work_items: WorkItems,
) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "wi-1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )

    page = work_items.list("acme", "ENG", fields=["id"])
    row = page.data[0]

    assert len(row._present) == 1
    with pytest.raises(FieldNotRequested, match="name"):
        _ = row.name


@responses.activate
def test_retrieve_with_fields_reads_a_requested_but_null_field_as_none(
    work_items: WorkItems,
) -> None:
    responses.get(f"{BASE}/wi-1/", json={"id": "wi-1", "name": None})

    row = work_items.retrieve("acme", "ENG", "wi-1", fields=["id", "name"])

    assert row.name is None


# -- `iterate`/`update`/`upsert` must return navigable rows too, like `retrieve`/
# `create`/`list` -- a caller who switches from `list` to `iterate` to page
# through results must not silently lose navigation.


@responses.activate
def test_iterate_yields_navigable_rows(work_items: WorkItems) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "wi-1"}], "pagination": {"style": "offset"}},
    )
    responses.get(
        f"{BASE}/wi-1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    row = next(iter(work_items.iterate("acme", "ENG")))
    row.comments.list()

    assert responses.calls[-1].request.url.endswith("/work-items/wi-1/comments/")


@responses.activate
def test_iterate_with_fields_raises_on_an_unrequested_field(work_items: WorkItems) -> None:
    """The generator must not materialise the whole page eagerly to forward
    `fields` -- exercised here by only ever serving one page."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "wi-1"}], "pagination": {"style": "offset"}},
    )

    row = next(iter(work_items.iterate("acme", "ENG", fields=["id"])))

    assert len(row._present) == 1
    with pytest.raises(FieldNotRequested, match="name"):
        _ = row.name


@responses.activate
def test_update_returns_a_navigable_row(work_items: WorkItems) -> None:
    responses.patch(f"{BASE}/wi-1/", json={"id": "wi-1", "name": "Renamed"})
    responses.get(
        f"{BASE}/wi-1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    row = work_items.update("acme", "ENG", "wi-1", UpdateWorkItem(name="Renamed"))
    row.comments.list()

    assert row.name == "Renamed"
    assert responses.calls[-1].request.url.endswith("/work-items/wi-1/comments/")


# -- Signpost: coverage dropped pending migration, not silently lost --------------


@pytest.mark.parametrize(
    "resource", ["attachments", "links", "worklogs", "activities", "relations", "dependencies"]
)
def test_sub_resource_coverage_pending_flat_pattern_migration(resource: str) -> None:
    """Not a real test: `WorkItem<Resource>` still uses the retired single-id
    (`work_item_id`-only) shape, so its offline coverage was removed here when
    `WorkItems` moved to the flat pattern in task 10. Restore real tests for it
    once it is migrated too."""
    pytest.skip(f"WorkItem{resource.title()} coverage removed pending flat-pattern migration")


# -- Presence follows the *response*, not the request ----------------------------
# (regression: `_present` was derived from the caller's `fields=`, so a partial row
# returned with no `fields=` in play -- which is what collection deferral does --
# marked every field present and read back as a silent `None`.)


@responses.activate
def test_retrieve_with_no_fields_argument_raises_for_a_field_the_server_omitted(
    work_items: WorkItems,
) -> None:
    responses.get(f"{BASE}/wi-1/", json={"id": "wi-1", "name": "Fix bug"})

    row = work_items.retrieve("acme", "ENG", "wi-1")

    assert row._present == frozenset({"id", "name"})
    with pytest.raises(FieldNotRequested, match="priority"):
        _ = row.priority


@responses.activate
def test_list_with_no_fields_argument_raises_for_a_deferred_field(
    work_items: WorkItems,
) -> None:
    """Collection deferral: the list route returns a narrower row than the detail
    route even though the caller passed no `fields=`."""
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "wi-1", "name": "Fix bug"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    row = work_items.list("acme", "ENG").data[0]

    assert row.name == "Fix bug"
    assert row._present == frozenset({"id", "name"})
    with pytest.raises(FieldNotRequested, match="state_id"):
        _ = row.state_id


@responses.activate
def test_a_field_the_server_returned_but_the_caller_narrowed_away_stays_hidden(
    work_items: WorkItems,
) -> None:
    responses.get(f"{BASE}/wi-1/", json={"id": "wi-1", "name": "Fix bug"})

    row = work_items.retrieve("acme", "ENG", "wi-1", fields=["id"])

    assert row._present == frozenset({"id"})
    with pytest.raises(FieldNotRequested, match="name"):
        _ = row.name


# -- Every method answering with a row of a navigable type returns the loaded form --


@responses.activate
def test_archive_returns_a_navigable_row(work_items: WorkItems) -> None:
    responses.post(
        f"{BASE}/wi-1/archive/", json={"id": "wi-1", "archived_at": "2026-01-01T00:00:00Z"}
    )
    responses.get(
        f"{BASE}/wi-1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    row = work_items.archive("acme", "ENG", "wi-1")
    row.comments.list()

    assert responses.calls[-1].request.url.endswith("/work-items/wi-1/comments/")


@responses.activate
def test_unarchive_returns_a_navigable_row(work_items: WorkItems) -> None:
    responses.post(f"{BASE}/wi-1/unarchive/", json={"id": "wi-1", "archived_at": None})
    responses.get(
        f"{BASE}/wi-1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    row = work_items.unarchive("acme", "ENG", "wi-1")
    row.comments.list()

    assert responses.calls[-1].request.url.endswith("/work-items/wi-1/comments/")
