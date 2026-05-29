"""Unit tests for WorkspaceProjectLabels API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

from plane.client import PlaneClient
from plane.models.workspace_project_labels import (
    CreateWorkspaceProjectLabel,
    UpdateWorkspaceProjectLabel,
)


class TestWorkspaceProjectLabels:
    """Test WorkspaceProjectLabels API resource."""

    def test_list_workspace_project_labels(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace project labels."""
        labels = client.workspace_project_labels.list(workspace_slug)
        assert isinstance(labels, list)

    def test_create_update_delete_workspace_project_label(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating, updating, and deleting a workspace project label."""
        name = f"test-label-{uuid4().hex[:8]}"
        data = CreateWorkspaceProjectLabel(name=name, color="#FF6B6B")
        created = client.workspace_project_labels.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        try:
            updated = client.workspace_project_labels.update(
                workspace_slug,
                created.id,
                UpdateWorkspaceProjectLabel(color="#00FF00"),
            )
            assert updated.id == created.id
            assert updated.color == "#00FF00"
        finally:
            try:
                client.workspace_project_labels.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for workspace project label {created.id}: {exc}", stacklevel=1
                )
