"""Offline coverage for `GroupSync`: the pk-less `config` singleton plus
`project_mappings`/`workspace_mappings`."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.group_sync import GroupSync
from plane.config import Configuration
from plane.models.v2.group_sync import (
    CreateGroupMapping,
    CreateWorkspaceGroupMapping,
    UpdateGroupMapping,
    UpdateGroupSyncConfig,
)

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def group_sync(config: Configuration) -> GroupSync:
    return GroupSync(V2Transport(config), slug="acme")


def test_group_sync_forwards_its_scope_to_every_sub_resource(group_sync: GroupSync) -> None:
    assert group_sync.config._scope == {"slug": "acme"}
    assert group_sync.project_mappings._scope == {"slug": "acme"}
    assert group_sync.workspace_mappings._scope == {"slug": "acme"}


@responses.activate
def test_group_sync_config_get(group_sync: GroupSync) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/group-sync/config/",
        json={"id": "1", "is_enabled": True, "group_attribute_key": "groups"},
    )

    config = group_sync.config.get()

    assert config.is_enabled is True
    assert config.group_attribute_key == "groups"


@responses.activate
def test_group_sync_config_update_hits_config_url_not_a_detail_url(group_sync: GroupSync) -> None:
    """The config resource has no `{pk}` -- update must PATCH the collection URL
    itself, not append a row id the way a normal resource's `_update` would."""
    responses.patch(
        f"{BASE}/workspaces/acme/group-sync/config/",
        json={"id": "1", "is_enabled": False},
    )

    updated = group_sync.config.update(UpdateGroupSyncConfig(is_enabled=False))

    assert updated.is_enabled is False
    assert responses.calls[0].request.url == f"{BASE}/workspaces/acme/group-sync/config/"


@responses.activate
def test_group_sync_project_mappings_crud(group_sync: GroupSync) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/group-sync/project-mappings/",
        json={
            "data": [{"id": "1", "idp_group_name": "eng-team", "role_slug": "member"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{BASE}/workspaces/acme/group-sync/project-mappings/",
        json={"id": "2", "idp_group_name": "qa-team", "role_slug": "member"},
        status=201,
    )
    responses.patch(
        f"{BASE}/workspaces/acme/group-sync/project-mappings/2/",
        json={"id": "2", "role_slug": "admin"},
    )
    responses.delete(f"{BASE}/workspaces/acme/group-sync/project-mappings/2/", status=204)

    page = group_sync.project_mappings.list()
    assert page.data[0].idp_group_name == "eng-team"

    created = group_sync.project_mappings.create(
        CreateGroupMapping(idp_group_name="qa-team", role_slug="member")
    )
    assert created.id == "2"

    updated = group_sync.project_mappings.update(created.id, UpdateGroupMapping(role_slug="admin"))
    assert updated.role_slug == "admin"

    assert group_sync.project_mappings.delete(created.id) is None


@responses.activate
def test_group_sync_project_mapping_all_projects_write(group_sync: GroupSync) -> None:
    responses.post(
        f"{BASE}/workspaces/acme/group-sync/project-mappings/",
        json={"id": "3", "all_projects": True},
        status=201,
    )

    group_sync.project_mappings.create(
        CreateGroupMapping(idp_group_name="everyone", role_slug="member", all_projects=True),
    )

    body = json.loads(responses.calls[0].request.body)
    assert body["all_projects"] is True
    assert "project_id" not in body


@responses.activate
def test_group_sync_workspace_mappings_crud(group_sync: GroupSync) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/group-sync/workspace-mappings/",
        json={
            "data": [{"id": "1", "idp_group_name": "eng-team", "role_slug": "member"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{BASE}/workspaces/acme/group-sync/workspace-mappings/",
        json={"id": "2", "idp_group_name": "qa-team", "role_slug": "member"},
        status=201,
    )
    responses.delete(f"{BASE}/workspaces/acme/group-sync/workspace-mappings/2/", status=204)

    page = group_sync.workspace_mappings.list()
    assert page.data[0].idp_group_name == "eng-team"

    created = group_sync.workspace_mappings.create(
        CreateWorkspaceGroupMapping(idp_group_name="qa-team", role_slug="member")
    )
    assert created.id == "2"

    assert group_sync.workspace_mappings.delete(created.id) is None


def test_workspace_mappings_have_no_project_id_field() -> None:
    """Workspace mappings map an IdP group straight to a workspace role -- there is
    no `project_id`/`all_projects` field to carry, unlike `CreateGroupMapping`."""
    assert not hasattr(CreateWorkspaceGroupMapping, "model_fields") or (
        "project_id" not in CreateWorkspaceGroupMapping.model_fields
    )
