"""Asset models for api_v2 (two-step S3 upload flow). Confirmed live: `create` returns
`{upload_data, asset_id, asset_url, asset}` (not the golden's bare
`WorkspaceAsset`/`UserAsset`); `asset_url` is nullable."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

UserAssetEntityType = Literal["USER_AVATAR", "USER_COVER"]


# -- Workspace assets -------------------------------------------------------------


class WorkspaceAsset(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    asset_url: str | None = None
    attributes: dict[str, object] | None = None
    content_type: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    entity_type: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    is_uploaded: bool | None = None
    name: str | None = None
    size: float | None = None


class CreateWorkspaceAsset(BaseModel):
    """POST body. Registers the asset's metadata; the response's `upload_data`
    (see `WorkspaceAssetUploadResult`) is where the caller then PUTs the file's
    bytes, and a follow-up PATCH (`WorkspaceAssetConfirm`) marks it uploaded."""

    model_config = ConfigDict(extra="ignore")

    name: str
    size: int
    entity_type: str | None = None
    """Free-form; the golden defaults this server-side to `"WORK_ITEM_IMPORT"`."""
    type: str | None = None
    """MIME type; the golden defaults this server-side to
    `"application/octet-stream"`."""


class WorkspaceAssetConfirm(BaseModel):
    """PATCH body -- confirms the out-of-band upload completed. See the module
    docstring: the golden has no documented request body for this operation."""

    model_config = ConfigDict(extra="ignore")

    is_uploaded: bool | None = None


class WorkspaceAssetUploadResult(BaseModel):
    """The real response to `POST .../assets/` (confirmed live): `{upload_data, asset_id,
    asset_url, asset}`; `asset_url` may legitimately be null."""

    model_config = ConfigDict(extra="allow")

    asset_id: str
    asset_url: str | None = None
    upload_data: dict[str, object]
    asset: WorkspaceAsset


# -- User assets (avatar/cover, not workspace-scoped) ----------------------------


class UserAsset(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    asset_url: str | None = None
    attributes: dict[str, object] | None = None
    content_type: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    entity_type: str | None = None
    is_uploaded: bool | None = None
    name: str | None = None
    size: float | None = None
    user_id: str | None = None


class CreateUserAsset(BaseModel):
    """POST body. `entity_type` picks avatar vs cover."""

    model_config = ConfigDict(extra="ignore")

    entity_type: UserAssetEntityType
    name: str
    size: int
    type: str | None = None
    """MIME type; the golden defaults this server-side to `"image/jpeg"`."""


class UserAssetConfirm(BaseModel):
    """PATCH body -- confirms the out-of-band upload completed. See the module
    docstring: the golden has no documented request body for this operation."""

    model_config = ConfigDict(extra="ignore")

    is_uploaded: bool | None = None


class UserAssetUploadResult(BaseModel):
    """The likely response to `POST /users/me/assets/`, modeled by analogy to
    `WorkspaceAssetUploadResult`; not independently verified live."""

    model_config = ConfigDict(extra="allow")

    asset_id: str
    asset_url: str
    upload_data: dict[str, object]
    asset: UserAsset
