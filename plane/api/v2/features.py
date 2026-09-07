"""Feature toggles (api_v2) -- two GET/PATCH singletons, no `id` in the URL: the
row IS the collection, so these go through the kernel's
`_retrieve_singleton`/`_update_singleton` pair rather than `_retrieve`/`_update`
(which both require a `pk` to append).

`WorkspaceFeatures` is re-authored flat (leading `slug`, per Task 11); `ProjectFeatures`
still uses the pre-flat shape and is not yet attached anywhere on the tree."""

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
        "get": "workspace_features_retrieve",
        "update": "workspace_features_update",
    }

    def get(self, slug: str) -> WorkspaceFeature:
        return self._retrieve_singleton(action="get", slug=slug)

    def update(self, slug: str, data: UpdateWorkspaceFeature) -> WorkspaceFeature:
        return self._update_singleton(data, action="update", slug=slug)


class ProjectFeatures(V2Resource[ProjectFeature, UpdateProjectFeature, UpdateProjectFeature]):
    path = "/workspaces/{slug}/projects/{project_id}/features/"
    model = ProjectFeature
    operations = {
        "retrieve": "project_features_retrieve",
        "update": "project_features_update",
    }

    def retrieve(self) -> ProjectFeature:
        return self._retrieve_singleton(action="retrieve")

    def update(self, data: UpdateProjectFeature) -> ProjectFeature:
        return self._update_singleton(data, action="update")
