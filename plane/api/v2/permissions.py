"""Effective permissions (api_v2) -- the calling principal's own grants for a
workspace or a project. Read-only, two GET endpoints. Split into two classes
(rather than one with a `project_me()` method) since `V2Resource` has one `path`.

`WorkspacePermissions` is a singleton at `/workspaces/{slug}/permissions/me/` with no
primary key of its own -- the row IS the collection, so it goes through the kernel's
`_retrieve_singleton` rather than `_retrieve` (which would append a pk segment and
request a wrong URL). Re-authored flat (leading `slug`), per Task 2; `ProjectPermissions`
still uses the pre-flat shape and is not yet attached anywhere on the tree."""

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

    def me(self, slug: str) -> EffectivePermissions:
        """The caller's effective permissions across the whole workspace."""
        return self._retrieve_singleton(action="me", slug=slug)


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
