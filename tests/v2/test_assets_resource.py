"""Offline coverage for `WorkspaceAssets`/`UserAssets`; pins that `create()` parses the
`*UploadResult` envelope."""

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.assets import UserAssets, WorkspaceAssets
from plane.config import Configuration
from plane.models.v2.assets import (
    CreateUserAsset,
    CreateWorkspaceAsset,
    UserAssetConfirm,
    WorkspaceAssetConfirm,
)

WORKSPACE_BASE = "https://api.example.com/api/v2/workspaces/acme/assets"
USER_BASE = "https://api.example.com/api/v2/users/me/assets"


@pytest.fixture
def workspace_assets(config: Configuration) -> WorkspaceAssets:
    return WorkspaceAssets(V2Transport(config), slug="acme")


@pytest.fixture
def user_assets(config: Configuration) -> UserAssets:
    return UserAssets(V2Transport(config))


# -- WorkspaceAssets -------------------------------------------------------------


@responses.activate
def test_workspace_assets_list(workspace_assets: WorkspaceAssets) -> None:
    responses.get(
        f"{WORKSPACE_BASE}/",
        json={
            "data": [{"id": "a1", "name": "log.txt"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    page = workspace_assets.list()

    assert page.total_count == 1
    assert page.data[0].name == "log.txt"


@responses.activate
def test_workspace_assets_retrieve(workspace_assets: WorkspaceAssets) -> None:
    responses.get(f"{WORKSPACE_BASE}/a1/", json={"id": "a1", "name": "log.txt"})

    row = workspace_assets.retrieve("a1")

    assert row.id == "a1"


@responses.activate
def test_workspace_assets_create_parses_the_upload_envelope(
    workspace_assets: WorkspaceAssets,
) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/",
        json={
            "asset_id": "a1",
            "asset_url": "/api/assets/v2/.../a1/",
            "upload_data": {"url": "https://s3.example.com", "fields": {"key": "a1"}},
            "asset": {"id": "a1", "name": "log.txt", "is_uploaded": False},
        },
    )

    result = workspace_assets.create(CreateWorkspaceAsset(name="log.txt", size=42))

    assert result.asset_id == "a1"
    assert result.upload_data["url"] == "https://s3.example.com"
    assert result.asset.id == "a1"
    assert result.asset.is_uploaded is False


@responses.activate
def test_workspace_assets_create_sends_only_the_write_fields(
    workspace_assets: WorkspaceAssets,
) -> None:
    responses.post(
        f"{WORKSPACE_BASE}/",
        json={
            "asset_id": "a1",
            "asset_url": "u",
            "upload_data": {},
            "asset": {"id": "a1"},
        },
    )

    workspace_assets.create(CreateWorkspaceAsset(name="log.txt", size=42))

    body = json.loads(responses.calls[0].request.body)
    assert body == {"name": "log.txt", "size": 42}


@responses.activate
def test_workspace_assets_update_confirms_upload(workspace_assets: WorkspaceAssets) -> None:
    responses.patch(f"{WORKSPACE_BASE}/a1/", json={"id": "a1", "is_uploaded": True})

    updated = workspace_assets.update("a1", WorkspaceAssetConfirm(is_uploaded=True))

    assert updated.is_uploaded is True
    body = json.loads(responses.calls[0].request.body)
    assert body == {"is_uploaded": True}


@responses.activate
def test_workspace_assets_delete_returns_none(workspace_assets: WorkspaceAssets) -> None:
    responses.delete(f"{WORKSPACE_BASE}/a1/", status=204)

    assert workspace_assets.delete("a1") is None


# -- UserAssets (not workspace-scoped) --------------------------------------------


@responses.activate
def test_user_assets_list_has_no_workspace_in_the_url(user_assets: UserAssets) -> None:
    responses.get(
        f"{USER_BASE}/",
        json={"data": [{"id": "u1"}], "pagination": {"style": "offset"}},
    )

    page = user_assets.list()

    assert page.data[0].id == "u1"
    assert "workspaces" not in responses.calls[0].request.url


@responses.activate
def test_user_assets_create_requires_entity_type(user_assets: UserAssets) -> None:
    responses.post(
        f"{USER_BASE}/",
        json={
            "asset_id": "u1",
            "asset_url": "u",
            "upload_data": {},
            "asset": {"id": "u1"},
        },
    )

    result = user_assets.create(
        CreateUserAsset(entity_type="USER_AVATAR", name="avatar.png", size=10)
    )

    assert result.asset_id == "u1"
    body = json.loads(responses.calls[0].request.body)
    assert body["entity_type"] == "USER_AVATAR"


@responses.activate
def test_user_assets_update_confirms_upload(user_assets: UserAssets) -> None:
    responses.patch(f"{USER_BASE}/u1/", json={"id": "u1", "is_uploaded": True})

    updated = user_assets.update("u1", UserAssetConfirm(is_uploaded=True))

    assert updated.is_uploaded is True


@responses.activate
def test_user_assets_delete_returns_none(user_assets: UserAssets) -> None:
    responses.delete(f"{USER_BASE}/u1/", status=204)

    assert user_assets.delete("u1") is None
