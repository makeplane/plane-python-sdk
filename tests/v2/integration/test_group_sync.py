"""Live coverage for `client.v2.workspaces.group_sync`: the workspace-wide config
singleton plus project-/workspace-scoped IdP group mappings, gated by
`FeatureFlag.IDP_GROUP_SYNC` (402 if unlicensed). Tests restore mutated config, and
the licence gate is a declared server-capability skip.

Flat path, and structurally so: `group_sync` is a *grouping node*, not a resource --
it holds no `V2Resource` base, `path` or `operations`, so it consumes no path id and
is deliberately absent from `LoadedWorkspace` (its children each take `slug`
themselves). A loaded workspace is not a route to it, and asking for one is how you
find that out."""

from __future__ import annotations

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.group_sync import GroupSync
from plane.client import PlaneClient
from plane.models.v2.group_sync import (
    CreateGroupMapping,
    CreateWorkspaceGroupMapping,
    UpdateGroupMapping,
    UpdateGroupSyncConfig,
)

from ._guard import skip_absent_capability
from .helpers import unique_name


@pytest.fixture
def group_sync(client: PlaneClient) -> GroupSync:
    return client.v2.workspaces.group_sync


def _require_group_sync(group_sync: GroupSync, workspace_slug: str) -> None:
    try:
        group_sync.config.get(workspace_slug)
    except PlaneAPIError as exc:
        if exc.status == 402:
            skip_absent_capability("IDP_GROUP_SYNC is not enabled on this workspace")
        raise


class TestGroupSyncConfig:
    @pytest.fixture(autouse=True)
    def _skip_if_disabled(self, group_sync: GroupSync, workspace_slug: str) -> None:
        _require_group_sync(group_sync, workspace_slug)

    def test_retrieve_returns_a_row(self, group_sync: GroupSync, workspace_slug: str) -> None:
        config = group_sync.config.get(workspace_slug)
        assert config.id

    def test_update_round_trips_and_restores(
        self, group_sync: GroupSync, workspace_slug: str
    ) -> None:
        original = group_sync.config.get(workspace_slug)
        try:
            toggled = group_sync.config.update(
                workspace_slug, UpdateGroupSyncConfig(auto_remove=not bool(original.auto_remove))
            )
            assert toggled.auto_remove != original.auto_remove
        finally:
            group_sync.config.update(
                workspace_slug, UpdateGroupSyncConfig(auto_remove=original.auto_remove)
            )


class TestGroupSyncProjectMappings:
    @pytest.fixture(autouse=True)
    def _skip_if_disabled(self, group_sync: GroupSync, workspace_slug: str) -> None:
        _require_group_sync(group_sync, workspace_slug)

    def test_create_list_update_delete_round_trip(
        self, group_sync: GroupSync, workspace_slug: str, project_id: str
    ) -> None:
        created = group_sync.project_mappings.create(
            workspace_slug,
            CreateGroupMapping(
                idp_group_name=unique_name("idp-group"),
                role_slug="member",
                project_id=project_id,
            )
        )
        try:
            page = group_sync.project_mappings.list(workspace_slug)
            assert any(row.id == created.id for row in page.data)

            updated = group_sync.project_mappings.update(
                workspace_slug, created.id, UpdateGroupMapping(role_slug="admin")
            )
            assert updated.role_slug == "admin"
        finally:
            group_sync.project_mappings.delete(workspace_slug, created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            group_sync.project_mappings.retrieve(workspace_slug, created.id)
        assert exc_info.value.status == 404

    def test_all_projects_mapping_has_no_project_id(
        self, group_sync: GroupSync, workspace_slug: str
    ) -> None:
        created = group_sync.project_mappings.create(
            workspace_slug,
            CreateGroupMapping(
                idp_group_name=unique_name("idp-group-all"),
                role_slug="member",
                all_projects=True,
            )
        )
        try:
            assert created.all_projects is True
            assert created.project_id is None
        finally:
            group_sync.project_mappings.delete(workspace_slug, created.id)


class TestGroupSyncWorkspaceMappings:
    @pytest.fixture(autouse=True)
    def _skip_if_disabled(self, group_sync: GroupSync, workspace_slug: str) -> None:
        _require_group_sync(group_sync, workspace_slug)

    def test_create_list_delete_round_trip(
        self, group_sync: GroupSync, workspace_slug: str
    ) -> None:
        created = group_sync.workspace_mappings.create(
            workspace_slug,
            CreateWorkspaceGroupMapping(
                idp_group_name=unique_name("idp-ws-group"), role_slug="member"
            )
        )
        try:
            page = group_sync.workspace_mappings.list(workspace_slug)
            assert any(row.id == created.id for row in page.data)
        finally:
            group_sync.workspace_mappings.delete(workspace_slug, created.id)

        with pytest.raises(PlaneAPIError) as exc_info:
            group_sync.workspace_mappings.retrieve(workspace_slug, created.id)
        assert exc_info.value.status == 404
