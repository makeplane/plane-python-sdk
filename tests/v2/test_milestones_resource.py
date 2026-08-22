"""Offline coverage for `Milestones`; includes `manage_work_items`, folded in from the former
separate `MilestoneWorkItems` class."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.milestones import Milestones
from plane.config import Configuration
from plane.models.v2.milestone_work_items import MilestoneWorkItemManageRequest
from plane.models.v2.milestones import CreateMilestone, UpdateMilestone

BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/milestones"


@pytest.fixture
def milestones(config: Configuration) -> Milestones:
    return Milestones(V2Transport(config), slug="acme", project_id="ENG")


@responses.activate
def test_list_milestones(milestones: Milestones) -> None:
    responses.get(
        f"{BASE}/",
        json={
            "data": [{"id": "1", "title": "Beta launch"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = milestones.list()

    assert page.total_count == 1
    assert page.data[0].title == "Beta launch"


@responses.activate
def test_sparse_response_leaves_absent_fields_none(milestones: Milestones) -> None:
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1"}], "pagination": {"style": "offset"}},
    )

    page = milestones.list(fields=["id"])

    assert page.data[0].id == "1"
    assert page.data[0].title is None


@responses.activate
def test_list_validates_fields_against_the_golden(milestones: Milestones) -> None:
    """`title` is a real field on `milestones_list` in the golden; `name` is not --
    milestones use `title`, not `name`, for the write/read field itself. A bad field
    name must be rejected client-side before the request is ever sent."""
    with pytest.raises(ValueError, match="Unknown field"):
        milestones.list(fields=["name"])


@responses.activate
def test_create_then_patch(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/",
        json={"id": "1", "title": "Beta launch"},
        status=201,
    )
    responses.patch(
        f"{BASE}/1/",
        json={"id": "1", "title": "GA launch"},
    )

    created = milestones.create(CreateMilestone(title="Beta launch"))
    updated = milestones.update(created.id, UpdateMilestone(title="GA launch"))

    assert updated.title == "GA launch"


@responses.activate
def test_delete(milestones: Milestones) -> None:
    responses.delete(f"{BASE}/1/", status=204)

    assert milestones.delete("1") is None


@responses.activate
def test_upsert_hits_the_upsert_url(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/upsert/",
        json={"id": "1", "title": "Beta launch"},
    )

    result = milestones.upsert(CreateMilestone(title="Beta launch"))

    assert result.id == "1"


@responses.activate
def test_bulk_create_hits_the_bulk_create_url(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    result = milestones.bulk_create([CreateMilestone(title="Beta launch")])

    assert result.succeeded == 1


@responses.activate
def test_find_by_name_filters_on_the_name_query_param(milestones: Milestones) -> None:
    """The golden aliases the `?name=` filter to the `title` column server-side, so
    `find_by_name` keeps the same `name` parameter every other resource uses even
    though the underlying field is `title`."""
    responses.get(
        f"{BASE}/",
        json={"data": [{"id": "1", "title": "Beta launch"}], "pagination": {"style": "offset"}},
    )

    assert milestones.find_by_name("Beta launch").id == "1"

    request = responses.calls[0].request
    assert "name=Beta" in (request.url or "")


# -- Custom action: manage_work_items --------------------------------------------


@responses.activate
def test_manage_work_items_add_and_remove(milestones: Milestones) -> None:
    responses.post(
        f"{BASE}/m1/work-items/",
        json={"added": ["wi-1"], "removed": ["wi-2"]},
    )

    result = milestones.manage_work_items(
        "m1", MilestoneWorkItemManageRequest(add=["wi-1"], remove=["wi-2"])
    )

    assert result.added == ["wi-1"]
    assert result.removed == ["wi-2"]
    sent_body = json.loads(responses.calls[0].request.body)
    assert sent_body == {"add": ["wi-1"], "remove": ["wi-2"]}
