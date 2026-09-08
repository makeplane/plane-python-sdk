"""Artifacts (api_v2) -- the Plane Intelligence generate/publish/host flow.
Only `create`/`retrieve`/`publish`/`update` exist; each returns a different envelope."""

from __future__ import annotations

from ...models.v2.artifacts import (
    Artifact,
    ArtifactDetail,
    ArtifactPublish,
    ArtifactUpdated,
    CreateArtifact,
    UpdateArtifactUpdate,
)
from ._kernel.resource import V2Resource


class Artifacts(V2Resource[ArtifactDetail, CreateArtifact, UpdateArtifactUpdate]):
    path = "/workspaces/{slug}/artifacts/"
    model = ArtifactDetail
    operations = {
        "create": "workspaces_artifacts_create",
        "retrieve": "workspaces_artifacts_retrieve",
        "publish": "workspaces_artifacts_publish_create",
        "update": "workspaces_artifacts_update_partial_update",
    }

    def create(self, slug: str, data: CreateArtifact) -> Artifact:
        payload = self.transport.request(
            "POST",
            self._collection_url("create", slug=slug),
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return Artifact.model_validate(payload)

    def retrieve(self, slug: str, artifact_id: str) -> ArtifactDetail:
        """Metadata + the current version's HTML."""
        return self._retrieve(pk=artifact_id, slug=slug)

    def publish(self, slug: str, artifact_id: str) -> ArtifactPublish:
        """Publish (anchor) an artifact for public hosting. No request body."""
        payload = self.transport.request(
            "POST", f"{self._detail_url(artifact_id, 'publish', slug=slug)}publish/"
        )
        return ArtifactPublish.model_validate(payload)

    def update(self, slug: str, artifact_id: str, data: UpdateArtifactUpdate) -> ArtifactUpdated:
        """Append a new HTML version (each call creates the next version wholesale
        -- there is no true partial update)."""
        payload = self.transport.request(
            "PATCH",
            f"{self._detail_url(artifact_id, 'update', slug=slug)}update/",
            json=data.model_dump(mode="json", exclude_none=True),
        )
        return ArtifactUpdated.model_validate(payload)
