"""Assets (api_v2) -- two-step S3 upload flow, workspace- and user-scoped.
Golden's `create` response shape and `update` body are wrong; workspace envelope
confirmed live, user envelope modeled from schema only."""

from __future__ import annotations

from collections.abc import Iterator, Sequence
from typing import Any

from ...models.v2.assets import (
    CreateUserAsset,
    CreateWorkspaceAsset,
    UserAsset,
    UserAssetConfirm,
    UserAssetUploadResult,
    WorkspaceAsset,
    WorkspaceAssetConfirm,
    WorkspaceAssetUploadResult,
)
from ._kernel.pagination import Page
from ._kernel.resource import V2Resource

__all__ = ["UserAssets", "WorkspaceAssets"]


class WorkspaceAssets(V2Resource[WorkspaceAsset, CreateWorkspaceAsset, WorkspaceAssetConfirm]):
    path = "/workspaces/{slug}/assets/"
    model = WorkspaceAsset
    operations = {
        "list": "assets_list",
        "retrieve": "assets_retrieve",
        "create": "assets_create",
        "update": "assets_partial_update",
        "delete": "assets_destroy",
    }

    def list(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Page[WorkspaceAsset]:
        """One page of workspace assets."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[WorkspaceAsset]:
        """Every workspace asset, following pages automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(
        self, asset_id: str, *, fields: Sequence[str] | None = None
    ) -> WorkspaceAsset:
        return self._retrieve(pk=asset_id, params={"fields": fields})

    def create(self, data: CreateWorkspaceAsset) -> WorkspaceAssetUploadResult:
        """Registers the asset's metadata and returns presigned upload instructions;
        no `fields` param (a sparse response could drop `upload_data`)."""
        payload = self.transport.request(
            "POST",
            self._collection_url(),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return WorkspaceAssetUploadResult.model_validate(payload)

    def update(self, asset_id: str, data: WorkspaceAssetConfirm) -> WorkspaceAsset:
        return self._update(data, pk=asset_id)

    def delete(self, asset_id: str) -> None:
        return self._delete(pk=asset_id)


class UserAssets(V2Resource[UserAsset, CreateUserAsset, UserAssetConfirm]):
    """The calling principal's own avatar/cover assets. Not workspace-scoped --
    no method here takes a workspace slug, unlike the rest of api_v2."""

    path = "/users/me/assets/"
    model = UserAsset
    operations = {
        "list": "user_assets_list",
        "retrieve": "user_assets_retrieve",
        "create": "user_assets_create",
        "update": "user_assets_partial_update",
        "delete": "user_assets_destroy",
    }

    def list(self, *, fields: Sequence[str] | None = None, **filters: Any) -> Page[UserAsset]:
        """One page of the calling principal's assets."""
        return self._list(params={"fields": fields, **filters})

    def iterate(
        self, *, fields: Sequence[str] | None = None, **filters: Any
    ) -> Iterator[UserAsset]:
        """Every asset belonging to the calling principal, following pages
        automatically."""
        return self._iter(params={"fields": fields, **filters})

    def retrieve(self, asset_id: str, *, fields: Sequence[str] | None = None) -> UserAsset:
        return self._retrieve(pk=asset_id, params={"fields": fields})

    def create(self, data: CreateUserAsset) -> UserAssetUploadResult:
        """Registers the asset's metadata and returns presigned upload
        instructions (see the module docstring for the contract caveat)."""
        payload = self.transport.request(
            "POST", self._collection_url(), json=data.model_dump(mode="json", exclude_none=True)
        )
        return UserAssetUploadResult.model_validate(payload)

    def update(self, asset_id: str, data: UserAssetConfirm) -> UserAsset:
        return self._update(data, pk=asset_id)

    def delete(self, asset_id: str) -> None:
        return self._delete(pk=asset_id)
