"""Assets (api_v2) -- two-step S3 upload flow, workspace- and user-scoped.
Golden's `create` response shape and `update` body are wrong; workspace envelope
confirmed live, user envelope modeled from schema only."""

from __future__ import annotations

from collections.abc import Iterator, Sequence

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
from ._generated.constants import (
    AssetsListField,
    AssetsListOrderBy,
    AssetsPartialUpdateField,
    AssetsRetrieveField,
    UserAssetsListField,
    UserAssetsListOrderBy,
    UserAssetsPartialUpdateField,
    UserAssetsRetrieveField,
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
        self,
        slug: str,
        *,
        fields: Sequence[AssetsListField] | None = None,
        order_by: AssetsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
    ) -> Page[WorkspaceAsset]:
        """One page of workspace assets. The golden offers no query filters on
        this operation."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
            },
            slug=slug,
        )

    def iterate(
        self,
        slug: str,
        *,
        fields: Sequence[AssetsListField] | None = None,
        order_by: AssetsListOrderBy | None = None,
    ) -> Iterator[WorkspaceAsset]:
        """Every workspace asset, following pages automatically."""
        return self._iter(params={"fields": fields, "order_by": order_by}, slug=slug)

    def retrieve(
        self, slug: str, asset: str, *, fields: Sequence[AssetsRetrieveField] | None = None
    ) -> WorkspaceAsset:
        return self._retrieve(pk=asset, params={"fields": fields}, slug=slug)

    def create(self, slug: str, data: CreateWorkspaceAsset) -> WorkspaceAssetUploadResult:
        """Registers the asset's metadata and returns presigned upload instructions;
        no `fields` param (a sparse response could drop `upload_data`).

        `_custom_action`: the response is an upload envelope, not a `WorkspaceAsset`
        row, so `_create` cannot parse it."""
        return self._custom_action("create", model=WorkspaceAssetUploadResult, data=data, slug=slug)

    def update(
        self,
        slug: str,
        asset: str,
        data: WorkspaceAssetConfirm,
        *,
        fields: Sequence[AssetsPartialUpdateField] | None = None,
    ) -> WorkspaceAsset:
        return self._update(data, pk=asset, params={"fields": fields}, slug=slug)

    def delete(self, slug: str, asset: str) -> None:
        return self._delete(pk=asset, slug=slug)


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

    def list(
        self,
        *,
        fields: Sequence[UserAssetsListField] | None = None,
        order_by: UserAssetsListOrderBy | None = None,
        per_page: int | None = None,
        offset: int | None = None,
    ) -> Page[UserAsset]:
        """One page of the calling principal's assets. Like `assets_list`, the golden
        offers no query filters on this operation -- hence no `**filters`."""
        return self._list(
            params={
                "fields": fields,
                "order_by": order_by,
                "per_page": per_page,
                "offset": offset,
            }
        )

    def iterate(
        self,
        *,
        fields: Sequence[UserAssetsListField] | None = None,
        order_by: UserAssetsListOrderBy | None = None,
    ) -> Iterator[UserAsset]:
        """Every asset belonging to the calling principal, following pages
        automatically."""
        return self._iter(params={"fields": fields, "order_by": order_by})

    def retrieve(
        self, asset: str, *, fields: Sequence[UserAssetsRetrieveField] | None = None
    ) -> UserAsset:
        return self._retrieve(pk=asset, params={"fields": fields})

    def create(self, data: CreateUserAsset) -> UserAssetUploadResult:
        """Registers the asset's metadata and returns presigned upload
        instructions (see the module docstring for the contract caveat);
        no `fields` param: `upload_data`'s presigned fields exist only in this
        one reply and cannot be re-fetched, so a projection could silently and
        irrecoverably drop them.

        `_custom_action` for the same reason as `WorkspaceAssets.create`: the
        response is an upload envelope, not a `UserAsset` row."""
        return self._custom_action("create", model=UserAssetUploadResult, data=data)

    def update(
        self,
        asset: str,
        data: UserAssetConfirm,
        *,
        fields: Sequence[UserAssetsPartialUpdateField] | None = None,
    ) -> UserAsset:
        return self._update(data, pk=asset, params={"fields": fields})

    def delete(self, asset: str) -> None:
        return self._delete(pk=asset)
