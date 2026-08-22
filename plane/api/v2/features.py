"""Feature toggles (api_v2) -- two GET/PATCH singletons, no `id` in the URL: the
row IS the collection, so these hit the collection URL directly rather than
`_retrieve`/`_update` (which both require a `pk` to append)."""

from __future__ import annotations

from ...models.v2.features import (
    ProjectFeature,
    UpdateProjectFeature,
    UpdateWorkspaceFeature,
    WorkspaceFeature,
)
from ._kernel.resource import V2Resource


class WorkspaceFeatures(
    V2Resource[WorkspaceFeature, UpdateWorkspaceFeature, UpdateWorkspaceFeature]
):
    path = "/workspaces/{slug}/features/"
    model = WorkspaceFeature
    operations = {
        "retrieve": "workspace_features_retrieve",
        "update": "workspace_features_update",
    }

    def retrieve(self) -> WorkspaceFeature:
        payload = self.transport.request("GET", self._collection_url())
        return self.model.model_validate(payload)

    def update(self, data: UpdateWorkspaceFeature) -> WorkspaceFeature:
        payload = self.transport.request(
            "PATCH",
            self._collection_url(),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return self.model.model_validate(payload)


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
