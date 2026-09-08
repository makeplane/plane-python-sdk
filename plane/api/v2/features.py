"""Feature toggles (api_v2) -- two GET/PATCH singletons, no `id` in the URL: the
row IS the collection, so these go through the kernel's
`_retrieve_singleton`/`_update_singleton` pair rather than `_retrieve`/`_update`
(which both require a `pk` to append).

`WorkspaceFeatures` is re-authored flat (leading `slug`, per Task 11); `ProjectFeatures`
is flat too (leading `slug, project`, same `_retrieve_singleton`/`_update_singleton`
pair), but is not yet attached anywhere on the tree."""

from __future__ import annotations

from typing_extensions import Never

from ...models.v2.features import (
    ProjectFeature,
    UpdateProjectFeature,
    UpdateWorkspaceFeature,
    WorkspaceFeature,
)
from ._kernel.resource import V2Resource


class WorkspaceFeatures(V2Resource[WorkspaceFeature, Never, UpdateWorkspaceFeature]):
    """The workspace's feature toggles -- a singleton, no primary key of its own.
    Reached as `ws.features`."""

    path = "/workspaces/{slug}/features/"
    model = WorkspaceFeature
    operations = {
        "retrieve": "workspace_features_retrieve",
        "update": "workspace_features_update",
    }

    def retrieve(self, slug: str) -> WorkspaceFeature:
        """`retrieve`, not `get`: a singleton has no primary key, but reading one is
        still the CRUD read. Its project-scoped twin below has always been spelled this
        way, and so is the golden's own operationId (`workspace_features_retrieve`)."""
        return self._retrieve_singleton(action="retrieve", slug=slug)

    def update(self, slug: str, data: UpdateWorkspaceFeature) -> WorkspaceFeature:
        return self._update_singleton(data, action="update", slug=slug)


class ProjectFeatures(V2Resource[ProjectFeature, UpdateProjectFeature, UpdateProjectFeature]):
    path = "/workspaces/{slug}/projects/{project_id}/features/"
    model = ProjectFeature
    operations = {
        "retrieve": "project_features_retrieve",
        "update": "project_features_update",
    }

    def retrieve(self, slug: str, project: str) -> ProjectFeature:
        return self._retrieve_singleton(action="retrieve", slug=slug, project_id=project)

    def update(self, slug: str, project: str, data: UpdateProjectFeature) -> ProjectFeature:
        return self._update_singleton(data, action="update", slug=slug, project_id=project)
