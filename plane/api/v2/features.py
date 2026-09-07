"""Feature toggles (api_v2) -- two GET/PATCH singletons, no `id` in the URL: the
row IS the collection, so these hit `url_for` directly rather than
`_retrieve`/`_update` (which both require a `pk` to append).

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
        payload = self.transport.request("GET", self.url_for("get", slug=slug))
        return WorkspaceFeature.model_validate(payload)

    def update(self, slug: str, data: UpdateWorkspaceFeature) -> WorkspaceFeature:
        payload = self.transport.request(
            "PATCH",
            self.url_for("update", slug=slug),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return WorkspaceFeature.model_validate(payload)


class ProjectFeatures(V2Resource[ProjectFeature, UpdateProjectFeature, UpdateProjectFeature]):
    path = "/workspaces/{slug}/projects/{project_id}/features/"
    model = ProjectFeature
    operations = {
        "retrieve": "project_features_retrieve",
        "update": "project_features_update",
    }

    def retrieve(self) -> ProjectFeature:
        payload = self.transport.request("GET", self._collection_url())
        return self.model.model_validate(payload)

    def update(self, data: UpdateProjectFeature) -> ProjectFeature:
        payload = self.transport.request(
            "PATCH",
            self._collection_url(),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return self.model.model_validate(payload)
