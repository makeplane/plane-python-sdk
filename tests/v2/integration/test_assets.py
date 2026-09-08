"""`WorkspaceAssets`/`UserAssets` against a real server; each gets its own suite
since both are two-step S3 upload flows with no plain name+color shape. Only
the metadata lifecycle is exercised here, not the actual S3 PUT."""

from __future__ import annotations

import pytest

from plane.api.v2.assets import UserAssets, WorkspaceAssets
from plane.client import PlaneClient
from plane.models.v2.assets import (
    CreateUserAsset,
    CreateWorkspaceAsset,
    UserAssetConfirm,
    WorkspaceAssetConfirm,
)

from .helpers import unique_name


@pytest.fixture
def workspace_assets(client: PlaneClient) -> WorkspaceAssets:
    return client.v2.workspaces.assets


@pytest.fixture
def user_assets(client: PlaneClient) -> UserAssets:
    return client.v2.user_assets


class TestWorkspaceAssets:
    def test_create_returns_presigned_upload_data(
        self, workspace_assets: WorkspaceAssets, workspace_slug: str
    ) -> None:
        result = workspace_assets.create(
            workspace_slug, CreateWorkspaceAsset(name=f"{unique_name('asset')}.txt", size=11)
        )
        try:
            assert result.asset_id
            # `asset_url` is null here (confirmed live): `FileAsset.asset_url` only
            # populates for a fixed `entity_type` allowlist, and an unset `entity_type`
            # defaults server-side to `WORK_ITEM_IMPORT`, which isn't on that list.
            assert result.asset_url is None
            assert result.upload_data  # the contract question this test pins
            assert result.asset.id == result.asset_id
        finally:
            workspace_assets.delete(workspace_slug, result.asset_id)

    def test_confirm_then_retrieve_reflects_is_uploaded(
        self, workspace_assets: WorkspaceAssets, workspace_slug: str
    ) -> None:
        created = workspace_assets.create(
            workspace_slug, CreateWorkspaceAsset(name=f"{unique_name('asset')}.txt", size=11)
        )
        try:
            confirmed = workspace_assets.update(
                workspace_slug, created.asset_id, WorkspaceAssetConfirm(is_uploaded=True)
            )
            assert confirmed.is_uploaded is True

            fetched = workspace_assets.retrieve(workspace_slug, created.asset_id)
            assert fetched.is_uploaded is True
        finally:
            workspace_assets.delete(workspace_slug, created.asset_id)

    def test_list_includes_the_created_asset(
        self, workspace_assets: WorkspaceAssets, workspace_slug: str
    ) -> None:
        created = workspace_assets.create(
            workspace_slug, CreateWorkspaceAsset(name=f"{unique_name('asset')}.txt", size=11)
        )
        try:
            ids = {row.id for row in workspace_assets.list(workspace_slug).data}
            assert created.asset_id in ids
        finally:
            workspace_assets.delete(workspace_slug, created.asset_id)


class TestUserAssets:
    def test_create_and_confirm_avatar(self, user_assets: UserAssets) -> None:
        created = user_assets.create(
            CreateUserAsset(entity_type="USER_AVATAR", name=f"{unique_name('avatar')}.png", size=11)
        )
        try:
            assert created.asset_id
            assert created.upload_data

            confirmed = user_assets.update(created.asset_id, UserAssetConfirm(is_uploaded=True))
            assert confirmed.is_uploaded is True
        finally:
            user_assets.delete(created.asset_id)

    def test_list_is_not_workspace_scoped(self, user_assets: UserAssets) -> None:
        created = user_assets.create(
            CreateUserAsset(entity_type="USER_AVATAR", name=f"{unique_name('avatar')}.png", size=11)
        )
        try:
            ids = {row.id for row in user_assets.list().data}
            assert created.asset_id in ids
        finally:
            user_assets.delete(created.asset_id)
