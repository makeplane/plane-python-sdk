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
        """`_custom_action` like its three siblings here: the response is a lean
        `Artifact`, not the `ArtifactDetail` this resource's `model` names."""
        return self._custom_action("create", model=Artifact, data=data, slug=slug)

    def retrieve(self, slug: str, artifact: str) -> ArtifactDetail:
        """Metadata + the current version's HTML."""
        return self._retrieve(pk=artifact, slug=slug)

    def publish(self, slug: str, artifact: str) -> ArtifactPublish:
        """Publish (anchor) an artifact for public hosting. No request body.

        `_custom_action`, not `_action`: the URL is the same (`{detail}/publish/`) but
        the response is an `ArtifactPublish` envelope, not an `ArtifactDetail` row."""
        return self._custom_action("publish", model=ArtifactPublish, pk=artifact, slug=slug)

    def update(self, slug: str, artifact: str, data: UpdateArtifactUpdate) -> ArtifactUpdated:
        """Append a new HTML version (each call creates the next version wholesale
        -- there is no true partial update). Another `_custom_action`: a PATCH to
        `{detail}/update/` answering an `ArtifactUpdated` envelope."""
        return self._custom_action(
            "update",
            model=ArtifactUpdated,
            method="PATCH",
            pk=artifact,
            data=data,
            slug=slug,
        )
