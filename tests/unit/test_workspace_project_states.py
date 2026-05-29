"""Unit tests for WorkspaceProjectStates API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

from plane.client import PlaneClient
from plane.models.workspace_project_states import (
    CreateWorkspaceProjectState,
    UpdateWorkspaceProjectState,
)


class TestWorkspaceProjectStates:
    """Test WorkspaceProjectStates API resource."""

    def test_list_workspace_project_states(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace project states."""
        states = client.workspace_project_states.list(workspace_slug)
        assert isinstance(states, list)

    def test_create_update_delete_workspace_project_state(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating, updating, and deleting a workspace project state."""
        name = f"test-state-{uuid4().hex[:8]}"
        data = CreateWorkspaceProjectState(
            name=name,
            color="#FF0000",
            group="unstarted",
            description="Test workspace state",
        )
        created = client.workspace_project_states.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        try:
            updated = client.workspace_project_states.update(
                workspace_slug,
                created.id,
                UpdateWorkspaceProjectState(description="Updated description"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated description"
        finally:
            try:
                client.workspace_project_states.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for workspace project state {created.id}: {exc}", stacklevel=1
                )
