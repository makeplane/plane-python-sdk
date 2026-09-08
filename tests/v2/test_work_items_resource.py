"""Offline coverage for `WorkItems` (the flat depth-2 pattern), `WorkItemComments`
(the depth-3 exemplar: `slug, project, work_item` leading parameters), and the other
six work-item children on the same depth-3 shape. The children are constructed
directly (not through `work_items.attachments` etc.) because they are still
`PendingMigration` placeholders on the tree -- flat-shape migration and tree wiring
are separate steps."""

import json

import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_items import WorkItems
from plane.api.v2.work_items.activities import WorkItemActivities
from plane.api.v2.work_items.attachments import WorkItemAttachments
from plane.api.v2.work_items.dependencies import WorkItemDependencies
from plane.api.v2.work_items.links import WorkItemLinks
from plane.api.v2.work_items.relations import WorkItemRelations
from plane.api.v2.work_items.worklogs import WorkItemWorklogs
from plane.config import Configuration
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
def test_iterate_is_lazy_and_costs_exactly_one_request_for_one_row(
    work_items: WorkItems,
) -> None:
    """Two pages are on offer and only one row is taken, so an eager implementation
    would show up as a second request. Mocking a single page -- as this test used to
    -- cannot tell the two apart: `has_more`/`next` would be exhausted either way."""
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "wi-1"}, {"id": "wi-2"}],
            "pagination": {"style": "offset"},
            "next": 2,
        },
    )
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "wi-3"}], "pagination": {"style": "offset"}, "next": None},
    )

    rows = work_items.iterate("acme", "ENG")
    first = next(iter(rows))

    assert first.id == "wi-1"
    assert len(responses.calls) == 1

    # The second page arrives only once the generator is driven past the first.
    assert [row.id for row in rows] == ["wi-2", "wi-3"]
    assert len(responses.calls) == 2


@responses.activate
def test_iterate_with_fields_raises_on_an_unrequested_field(work_items: WorkItems) -> None:
    """`fields=` must survive the trip through the generator, not just through `list`."""
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


# -- The other six work-item children, on the same depth-3 shape ------------------


@pytest.fixture
def activities(config: Configuration) -> WorkItemActivities:
    return WorkItemActivities(V2Transport(config))


@pytest.fixture
def attachments(config: Configuration) -> WorkItemAttachments:
    return WorkItemAttachments(V2Transport(config))


@pytest.fixture
def links(config: Configuration) -> WorkItemLinks:
    return WorkItemLinks(V2Transport(config))


@pytest.fixture
def relations(config: Configuration) -> WorkItemRelations:
    return WorkItemRelations(V2Transport(config))


@pytest.fixture
def dependencies(config: Configuration) -> WorkItemDependencies:
    return WorkItemDependencies(V2Transport(config))


@pytest.fixture
def worklogs(config: Configuration) -> WorkItemWorklogs:
    return WorkItemWorklogs(V2Transport(config))


@responses.activate
def test_activities_list_and_retrieve_take_three_ids(activities: WorkItemActivities) -> None:
    responses.get(
        f"{BASE}/w1/activities/",
        json={"data": [{"id": "a1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )
    responses.get(f"{BASE}/w1/activities/a1/", json={"id": "a1", "field": "state"})

    page = activities.list("acme", "ENG", "w1")
    assert page.data[0].id == "a1"
    assert responses.calls[0].request.url == f"{BASE}/w1/activities/"

    row = activities.retrieve("acme", "ENG", "w1", "a1")
    assert row.field == "state"
    assert responses.calls[1].request.url == f"{BASE}/w1/activities/a1/"


@responses.activate
def test_attachments_crud_takes_three_leading_ids(attachments: WorkItemAttachments) -> None:
    responses.get(
        f"{BASE}/w1/attachments/",
        json={"data": [{"id": "att1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )
    responses.get(f"{BASE}/w1/attachments/att1/", json={"id": "att1", "name": "spec.pdf"})
    responses.post(
        f"{BASE}/w1/attachments/",
        json={
            "asset_id": "asset-1",
            "asset_url": "https://uploads.example.com/asset-1",
            "upload_data": {},
            "attachment": {"id": "att1", "name": "spec.pdf"},
        },
        status=201,
    )
    responses.patch(f"{BASE}/w1/attachments/att1/", json={"id": "att1", "is_uploaded": True})
    responses.delete(f"{BASE}/w1/attachments/att1/", status=204)

    page = attachments.list("acme", "ENG", "w1")
    assert page.data[0].id == "att1"
    assert responses.calls[0].request.url == f"{BASE}/w1/attachments/"

    fetched = attachments.retrieve("acme", "ENG", "w1", "att1")
    assert fetched.name == "spec.pdf"
    assert responses.calls[1].request.url == f"{BASE}/w1/attachments/att1/"

    created = attachments.create(
        "acme", "ENG", "w1", CreateWorkItemAttachment(name="spec.pdf", size=100)
    )
    assert created.asset_id == "asset-1"
    assert responses.calls[2].request.url == f"{BASE}/w1/attachments/"

    updated = attachments.update(
        "acme", "ENG", "w1", "att1", WorkItemAttachmentConfirm(is_uploaded=True)
    )
    assert updated.is_uploaded is True
    assert responses.calls[3].request.url == f"{BASE}/w1/attachments/att1/"

    assert attachments.delete("acme", "ENG", "w1", "att1") is None
    assert responses.calls[4].request.url == f"{BASE}/w1/attachments/att1/"


@responses.activate
def test_work_item_links_take_three_ids(links: WorkItemLinks) -> None:
    responses.get(
        f"{BASE}/w1/links/",
        json={"data": [{"id": "l1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )

    page = links.list("acme", "ENG", "w1")

    assert page.data[0].id == "l1"
    assert responses.calls[0].request.url == f"{BASE}/w1/links/"


@responses.activate
def test_links_full_crud(links: WorkItemLinks) -> None:
    responses.get(f"{BASE}/w1/links/l1/", json={"id": "l1", "url": "https://a.example.com"})
    responses.post(
        f"{BASE}/w1/links/", json={"id": "l1", "url": "https://a.example.com"}, status=201
    )
    responses.patch(f"{BASE}/w1/links/l1/", json={"id": "l1", "url": "https://b.example.com"})
    responses.delete(f"{BASE}/w1/links/l1/", status=204)

    created = links.create("acme", "ENG", "w1", CreateWorkItemLink(url="https://a.example.com"))
    assert created.id == "l1"
    assert responses.calls[0].request.url == f"{BASE}/w1/links/"

    fetched = links.retrieve("acme", "ENG", "w1", "l1")
    assert fetched.url == "https://a.example.com"
    assert responses.calls[1].request.url == f"{BASE}/w1/links/l1/"

    updated = links.update(
        "acme", "ENG", "w1", "l1", UpdateWorkItemLink(url="https://b.example.com")
    )
    assert updated.url == "https://b.example.com"
    assert responses.calls[2].request.url == f"{BASE}/w1/links/l1/"

    assert links.delete("acme", "ENG", "w1", "l1") is None
    assert responses.calls[3].request.url == f"{BASE}/w1/links/l1/"


@responses.activate
def test_relations_list_and_create_hit_the_collection_url_directly(
    relations: WorkItemRelations,
) -> None:
    """`list`/`create` return a dict-shaped envelope, not a paginated `Page`."""
    responses.get(f"{BASE}/w1/relations/", json={"blocking": ["w2"]})
    responses.post(f"{BASE}/w1/relations/", json={"blocking": ["w2", "w3"]}, status=201)
    responses.delete(f"{BASE}/w1/relations/w2/", status=204)

    listed = relations.list("acme", "ENG", "w1")
    assert listed.model_extra == {"blocking": ["w2"]}
    assert responses.calls[0].request.url == f"{BASE}/w1/relations/"

    created = relations.create(
        "acme",
        "ENG",
        "w1",
        WorkItemRelationCreate(
            direction="blocking", relation_definition_id="rd1", work_item_ids=["w3"]
        ),
    )
    assert created.model_extra == {"blocking": ["w2", "w3"]}
    assert responses.calls[1].request.url == f"{BASE}/w1/relations/"

    assert relations.delete("acme", "ENG", "w1", "w2") is None
    assert responses.calls[2].request.url == f"{BASE}/w1/relations/w2/"


@responses.activate
def test_dependencies_list_and_create_hit_the_collection_url_directly(
    dependencies: WorkItemDependencies,
) -> None:
    responses.get(
        f"{BASE}/w1/dependencies/",
        json={
            "blocked_by": [],
            "blocking": ["w2"],
            "start_after": [],
            "start_before": [],
            "finish_after": [],
            "finish_before": [],
        },
    )
    responses.post(
        f"{BASE}/w1/dependencies/",
        json={
            "blocked_by": [],
            "blocking": ["w2", "w3"],
            "start_after": [],
            "start_before": [],
            "finish_after": [],
            "finish_before": [],
        },
        status=201,
    )
    responses.delete(f"{BASE}/w1/dependencies/w2/", status=204)

    listed = dependencies.list("acme", "ENG", "w1")
    assert listed.blocking == ["w2"]
    assert responses.calls[0].request.url == f"{BASE}/w1/dependencies/"

    created = dependencies.create(
        "acme",
        "ENG",
        "w1",
        WorkItemDependencyCreate(relation_type="blocking", work_item_ids=["w3"]),
    )
    assert created.blocking == ["w2", "w3"]
    assert responses.calls[1].request.url == f"{BASE}/w1/dependencies/"

    assert dependencies.delete("acme", "ENG", "w1", "w2") is None
    assert responses.calls[2].request.url == f"{BASE}/w1/dependencies/w2/"


@responses.activate
def test_worklogs_full_crud_with_expand(worklogs: WorkItemWorklogs) -> None:
    responses.get(
        f"{BASE}/w1/worklogs/",
        json={"data": [{"id": "wl1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )
    responses.post(f"{BASE}/w1/worklogs/", json={"id": "wl1", "duration": 60}, status=201)
    responses.get(f"{BASE}/w1/worklogs/wl1/", json={"id": "wl1", "duration": 60})
    responses.patch(f"{BASE}/w1/worklogs/wl1/", json={"id": "wl1", "duration": 90})
    responses.delete(f"{BASE}/w1/worklogs/wl1/", status=204)

    page = worklogs.list("acme", "ENG", "w1", expand=["logged_by"])
    assert page.data[0].id == "wl1"
    assert "expand=logged_by" in responses.calls[0].request.url

    created = worklogs.create("acme", "ENG", "w1", CreateWorkItemWorklog(duration=60))
    assert created.duration == 60
    assert responses.calls[1].request.url == f"{BASE}/w1/worklogs/"

    fetched = worklogs.retrieve("acme", "ENG", "w1", "wl1")
    assert fetched.duration == 60
    assert responses.calls[2].request.url == f"{BASE}/w1/worklogs/wl1/"

    updated = worklogs.update("acme", "ENG", "w1", "wl1", UpdateWorkItemWorklog(duration=90))
    assert updated.duration == 90
    assert responses.calls[3].request.url == f"{BASE}/w1/worklogs/wl1/"

    assert worklogs.delete("acme", "ENG", "w1", "wl1") is None
    assert responses.calls[4].request.url == f"{BASE}/w1/worklogs/wl1/"


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
