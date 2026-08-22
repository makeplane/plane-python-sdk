"""Effective permissions (api_v2) -- the calling principal's own grants for a
workspace or a project. Read-only, two GET endpoints. Split into two classes
(rather than one with a `project_me()` method) since `V2Resource` has one `path`."""

from __future__ import annotations

from ...models.v2.permissions import EffectivePermissions
from ._kernel.resource import V2Resource


class WorkspacePermissions(
    V2Resource[EffectivePermissions, EffectivePermissions, EffectivePermissions]
):
    path = "/workspaces/{slug}/permissions/me/"
    model = EffectivePermissions
    operations = {
        "me": "workspaces_permissions_me_retrieve",
    }

    def me(self) -> EffectivePermissions:
        """The caller's effective permissions across the whole workspace."""
        payload = self.transport.request("GET", self._collection_url())
        return self.model.model_validate(payload)


class ProjectPermissions(
    V2Resource[EffectivePermissions, EffectivePermissions, EffectivePermissions]
):
    path = "/workspaces/{slug}/projects/{project_id}/permissions/me/"
    model = EffectivePermissions
    operations = {
        "me": "workspaces_projects_permissions_me_retrieve",
    }

    def me(self) -> EffectivePermissions:
        """The caller's effective permissions scoped to this project."""
        payload = self.transport.request("GET", self._collection_url())
        return self.model.model_validate(payload)
