"""Artifacts against a real server; requires the `APPLETS` flag and workspace
admin/owner. No delete op in the golden, so created artifacts are permanent
test litter -- acceptable for this POC-scope resource; not verified live yet.

Flat path: with no `delete`, there is no round trip worth a loaded row here, and the
workspace slug in every URL is the whole shape of the resource."""

from __future__ import annotations

from plane.api.v2.artifacts import Artifacts
from plane.client import PlaneClient
from plane.models.v2.artifacts import CreateArtifact, UpdateArtifactUpdate


def test_create_retrieve_update_publish(client: PlaneClient, workspace_slug: str) -> None:
    artifacts: Artifacts = client.v2.workspaces.artifacts

    created = artifacts.create(
        workspace_slug, CreateArtifact(name="SDK IT artifact", html="<p>v1</p>")
    )
    assert created.current_version == 1
    assert created.is_published is False

    detail = artifacts.retrieve(workspace_slug, created.id)
    assert detail.html == "<p>v1</p>"

    updated = artifacts.update(workspace_slug, created.id, UpdateArtifactUpdate(html="<p>v2</p>"))
    assert updated.current_version == 2

    published = artifacts.publish(workspace_slug, created.id)
    assert published.is_active is True
    assert published.anchor
