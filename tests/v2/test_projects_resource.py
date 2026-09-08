"""Offline coverage for `Projects`: CRUD, `upsert`, bulk create/update (no bulk-delete),
archive/unarchive, `summary`, and `role_distribution`."""

from __future__ import annotations

import pytest
import responses
from responses import matchers

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.projects import Projects
from plane.config import Configuration
from plane.models.v2.projects import CreateProject, UpdateProject

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def projects(config: Configuration) -> Projects:
    return Projects(V2Transport(config))


@responses.activate
def test_projects_retrieve_accepts_bare_identifier(projects: Projects) -> None:
    """`pk` is `{"pattern": "^[^/]+$"}` in the golden, not a uuid format -- a bare
    project key like `ENG` must round-trip through `retrieve` with no separate
    lookup step."""
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/",
        json={"id": "real-uuid", "identifier": "ENG", "name": "Engineering"},
    )

    project = projects.retrieve("acme", "ENG")

    assert project.identifier == "ENG"
    assert responses.calls[0].request.url == f"{BASE}/workspaces/acme/projects/ENG/"


@responses.activate
def test_find_by_name(projects: Projects) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/",
        json={
            "data": [{"id": "1", "identifier": "ENG", "name": "Engineering"}],
            "pagination": {"style": "offset"},
        },
        match=[
            matchers.query_param_matcher({"name": "Engineering", "per_page": "2", "count": "False"})
        ],
    )

    assert projects.find_by_name("acme", "Engineering").id == "1"


@responses.activate
def test_projects_create_then_update_then_delete(projects: Projects) -> None:
    responses.post(
        f"{BASE}/workspaces/acme/projects/",
        json={"id": "1", "identifier": "ENG", "name": "Engineering"},
        status=201,
    )
    responses.patch(
        f"{BASE}/workspaces/acme/projects/ENG/",
        json={"id": "1", "identifier": "ENG", "name": "Eng Team"},
    )
    responses.delete(f"{BASE}/workspaces/acme/projects/ENG/", status=204)

    created = projects.create("acme", CreateProject(identifier="ENG", name="Engineering"))
    assert created.id == "1"

    updated = projects.update("acme", "ENG", UpdateProject(name="Eng Team"))
    assert updated.name == "Eng Team"

    assert projects.delete("acme", "ENG") is None


@responses.activate
def test_projects_upsert(projects: Projects) -> None:
    responses.post(
        f"{BASE}/workspaces/acme/projects/upsert/",
        json={"id": "1", "identifier": "ENG", "name": "Engineering"},
        status=201,
    )

    result = projects.upsert("acme", CreateProject(identifier="ENG", name="Engineering"))

    assert result.id == "1"


@responses.activate
def test_projects_bulk_create_and_bulk_update(projects: Projects) -> None:
    responses.post(
        f"{BASE}/workspaces/acme/projects/bulk-create/",
        json={
            "results": [{"index": 0, "result": "created", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )
    responses.post(
        f"{BASE}/workspaces/acme/projects/bulk-update/",
        json={
            "results": [{"index": 0, "result": "updated", "id": "1"}],
            "succeeded": 1,
            "failed": 0,
        },
    )

    created = projects.bulk_create("acme", [CreateProject(identifier="ENG", name="Engineering")])
    assert created.succeeded == 1

    updated = projects.bulk_update("acme", [{"id": "1", "name": "Eng Team"}])
    assert updated.succeeded == 1


def test_projects_has_no_bulk_delete(projects: Projects) -> None:
    """Deleting a project cascades work items/cycles/modules/pages/members, so the
    API deliberately does not offer a batched bulk-delete for this resource --
    unlike states/labels/work-items, which all do."""
    assert not hasattr(projects, "bulk_delete")


@responses.activate
def test_projects_archive_and_unarchive_return_none(projects: Projects) -> None:
    responses.post(f"{BASE}/workspaces/acme/projects/ENG/archive/", status=204)
    responses.post(f"{BASE}/workspaces/acme/projects/ENG/unarchive/", status=204)

    assert projects.archive("acme", "ENG") is None
    assert projects.unarchive("acme", "ENG") is None


@responses.activate
def test_projects_summary_parses_the_summary_shape_not_project(projects: Projects) -> None:
    """`summary` returns `ProjectSummary` (id/identifier/name/counts), a different
    shape than `Project` -- this is why it cannot go through `_action`, which always
    parses the resource's own `model`."""
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/summary/",
        json={"id": "1", "identifier": "ENG", "name": "Engineering", "counts": {"members": 3}},
    )

    summary = projects.summary("acme", "ENG")

    assert summary.counts == {"members": 3}


@responses.activate
def test_projects_summary_joins_counts_filter(projects: Projects) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/summary/",
        json={"id": "1", "identifier": "ENG", "name": "Engineering", "counts": {"members": 3}},
    )

    projects.summary("acme", "ENG", counts=["members", "states"])

    assert "counts=members%2Cstates" in responses.calls[0].request.url


@responses.activate
def test_role_distribution_hits_the_sibling_workspace_path(projects: Projects) -> None:
    """`role_distribution` is a workspace-wide report with no `{pk}`, folded in from the former
    standalone `project-role-distribution` resource."""
    responses.get(
        f"{BASE}/workspaces/acme/project-role-distribution/",
        json={
            "roles": [
                {
                    "role_id": "r1",
                    "name": "Admin",
                    "slug": "admin",
                    "level": 20,
                    "is_system": True,
                    "membership_count": 3,
                    "distinct_member_count": 3,
                }
            ],
            "total_distinct_members": 3,
            "total_memberships": 3,
        },
    )

    report = projects.role_distribution("acme")

    assert report.total_memberships == 3
    assert report.roles[0].name == "Admin"
    assert responses.calls[0].request.url == f"{BASE}/workspaces/acme/project-role-distribution/"


@responses.activate
def test_role_distribution_handles_nulled_role(projects: Projects) -> None:
    """A role since deleted comes back with `role_id`/`name`/`slug` all null,
    per the golden's nullable-but-required fields."""
    responses.get(
        f"{BASE}/workspaces/acme/project-role-distribution/",
        json={
            "roles": [
                {
                    "role_id": None,
                    "name": None,
                    "slug": None,
                    "level": None,
                    "is_system": None,
                    "membership_count": 1,
                    "distinct_member_count": 1,
                }
            ],
            "total_distinct_members": 1,
            "total_memberships": 1,
        },
    )

    report = projects.role_distribution("acme")

    assert report.roles[0].role_id is None
    assert report.roles[0].membership_count == 1
