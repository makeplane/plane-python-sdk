"""Effective permissions (api_v2) -- the calling principal's own grants for a
workspace or a project -- plus the catalogue of keys a custom permission scheme
may grant (`WorkspacePermissions.resources`). Read-only GET endpoints. Split into two classes
(rather than one with a `project_me()` method) since `V2Resource` has one `path`.

`WorkspacePermissions` is a singleton at `/workspaces/{slug}/permissions/me/` with no
primary key of its own -- the row IS the collection, so it goes through the kernel's
`_retrieve_singleton` rather than `_retrieve` (which would append a pk segment and
request a wrong URL). Re-authored flat (leading `slug`), per Task 2; `ProjectPermissions`
is flat too (leading `slug, project`, same `_retrieve_singleton`), but is not yet
attached anywhere on the tree."""

from __future__ import annotations

from typing import Literal

from ...models.v2.permissions import EffectivePermissions, PermissionCatalogue
from ._kernel.resource import V2Resource


class WorkspacePermissions(
    V2Resource[EffectivePermissions, EffectivePermissions, EffectivePermissions]
):
    path = "/workspaces/{slug}/permissions/me/"
    extra_paths = {"resources": "/workspaces/{slug}/permissions/resources/"}
    model = EffectivePermissions
    operations = {
        "me": "workspaces_permissions_me_retrieve",
        "resources": "workspaces_permissions_resources_retrieve",
    }

    def me(self, slug: str) -> EffectivePermissions:
        """The caller's effective permissions across the whole workspace."""
        return self._retrieve_singleton(action="me", slug=slug)

    def resources(
        self, slug: str, *, namespace: Literal["workspace", "project"] | None = None
    ) -> PermissionCatalogue:
        """The permission keys a custom scheme of `namespace` may grant (the server
        defaults to `workspace`), per resource type, with what each key requires
        and includes on save."""
        return self._custom_action(
            "resources",
            model=PermissionCatalogue,
            method="GET",
            params={"namespace": namespace},
            slug=slug,
        )


class ProjectPermissions(
    V2Resource[EffectivePermissions, EffectivePermissions, EffectivePermissions]
):
    path = "/workspaces/{slug}/projects/{project_id}/permissions/me/"
    model = EffectivePermissions
    operations = {
        "me": "workspaces_projects_permissions_me_retrieve",
    }

    def me(self, slug: str, project: str) -> EffectivePermissions:
        """The caller's effective permissions scoped to this project."""
        return self._retrieve_singleton(action="me", slug=slug, project_id=project)
