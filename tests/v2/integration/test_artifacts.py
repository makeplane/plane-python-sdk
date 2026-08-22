"""Artifacts against a real server; requires the `APPLETS` flag and workspace
admin/owner. No delete op in the golden, so created artifacts are permanent
test litter -- acceptable for this POC-scope resource; not verified live yet."""

from __future__ import annotations

from plane.api.v2.artifacts import Artifacts
from plane.client import PlaneClient
from plane.models.v2.artifacts import CreateArtifact, UpdateArtifactUpdate


def test_create_retrieve_update_publish(client: PlaneClient, workspace_slug: str) -> None:
    artifacts: Artifacts = client.v2.workspace(workspace_slug).artifacts

    created = artifacts.create(CreateArtifact(name="SDK IT artifact", html="<p>v1</p>"))
    assert created.current_version == 1
    assert created.is_published is False

    detail = artifacts.retrieve(created.id)
    assert detail.html == "<p>v1</p>"

    updated = artifacts.update(created.id, UpdateArtifactUpdate(html="<p>v2</p>"))
    assert updated.current_version == 2

    published = artifacts.publish(created.id)
    assert published.is_active is True
    assert published.anchor
