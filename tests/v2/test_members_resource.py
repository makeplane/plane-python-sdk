"""Offline coverage for `ProjectMembers`/`WorkspaceMembers`; the latter is list-only plus `remove`,
keyed on email not a row id."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.members import ProjectMembers, WorkspaceMembers
from plane.config import Configuration
from plane.models.v2.members import CreateProjectMember, UpdateProjectMember, WorkspaceMemberRemove

PROJECT_BASE = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/members"
WORKSPACE_BASE = "https://api.example.com/api/v2/workspaces/acme/members"


@pytest.fixture
def project_members(config: Configuration) -> ProjectMembers:
    return ProjectMembers(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_members(config: Configuration) -> WorkspaceMembers:
    return WorkspaceMembers(V2Transport(config))


# -- ProjectMembers ----------------------------------------------------------------


@responses.activate
def test_project_members_list(project_members: ProjectMembers) -> None:
    responses.get(
        f"{PROJECT_BASE}/",
        json={
            "data": [{"id": "m1", "member_id": "u1", "role": "contributor"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = project_members.list()

    assert page.total_count == 1
    assert page.data[0].role == "contributor"


@responses.activate
def test_project_members_list_passes_expand(project_members: ProjectMembers) -> None:
    responses.get(f"{PROJECT_BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    project_members.list(expand=["member"])

    assert "expand=member" in responses.calls[0].request.url


def test_project_members_list_rejects_unknown_expand(project_members: ProjectMembers) -> None:
    with pytest.raises(ValueError, match="bogus"):
        project_members.list(expand=["bogus"])


@responses.activate
def test_project_members_retrieve(project_members: ProjectMembers) -> None:
    responses.get(f"{PROJECT_BASE}/m1/", json={"id": "m1", "member_id": "u1"})

    row = project_members.retrieve("m1")

    assert row.id == "m1"


@responses.activate
def test_project_members_create(project_members: ProjectMembers) -> None:
    responses.post(f"{PROJECT_BASE}/", json={"id": "m1", "member_id": "u1"}, status=201)

    created = project_members.create(CreateProjectMember(member_id="u1", role="contributor"))

    assert created.id == "m1"
    body = json.loads(responses.calls[0].request.body)
    assert body == {"member_id": "u1", "role": "contributor"}


@responses.activate
def test_project_members_update_changes_role(project_members: ProjectMembers) -> None:
    responses.patch(f"{PROJECT_BASE}/m1/", json={"id": "m1", "role": "admin"})

    updated = project_members.update("m1", UpdateProjectMember(role="admin"))

    assert updated.role == "admin"


@responses.activate
def test_project_members_delete_returns_none(project_members: ProjectMembers) -> None:
    responses.delete(f"{PROJECT_BASE}/m1/", status=204)

    assert project_members.delete("m1") is None


# -- WorkspaceMembers (list-only + remove) ----------------------------------------


@responses.activate
def test_workspace_members_list(workspace_members: WorkspaceMembers) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={
            "data": [{"id": "m1", "member_id": "u1", "role": "member"}],
            "pagination": {"style": "offset"},
        },
    )

    page = workspace_members.list("acme")

    assert page.data[0].role == "member"
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/"


@responses.activate
def test_workspace_members_list_per_page_and_offset(workspace_members: WorkspaceMembers) -> None:
    responses.get(f"{WORKSPACE_BASE}/", json={"data": [], "pagination": {"style": "offset"}})

    workspace_members.list("acme", per_page=15, offset=30)

    query = responses.calls[0].request.url
    assert "per_page=15" in query
    assert "offset=30" in query


@responses.activate
def test_workspace_members_has_no_detail_crud(workspace_members: WorkspaceMembers) -> None:
    """`WorkspaceMembers` deliberately exposes no `retrieve`/`create`/`update`/
    `delete` -- the golden has no such operations for this resource."""
    assert not hasattr(workspace_members, "retrieve")
    assert not hasattr(workspace_members, "create")
    assert not hasattr(workspace_members, "update")
    assert not hasattr(workspace_members, "delete")


@responses.activate
def test_remove_posts_to_remove_sub_path_keyed_by_email(
    workspace_members: WorkspaceMembers,
) -> None:
    responses.post(f"{WORKSPACE_BASE}/remove/", status=204)

    result = workspace_members.remove(
        "acme", WorkspaceMemberRemove(email="gone@example.com", remove_seat=True)
    )

    assert result is None
    body = json.loads(responses.calls[0].request.body)
    assert body == {"email": "gone@example.com", "remove_seat": True}
    assert responses.calls[0].request.url == f"{WORKSPACE_BASE}/remove/"
