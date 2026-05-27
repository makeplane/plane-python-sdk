"""Unit tests for WorkspaceWorkItemTypes API resource (smoke tests with real HTTP requests)."""

from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.models.work_item_types import CreateWorkItemType, UpdateWorkItemType


class TestWorkspaceWorkItemTypes:
    """Test WorkspaceWorkItemTypes API resource."""

    def test_list_workspace_work_item_types(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing workspace-level work item types."""
        types = client.workspace_work_item_types.list(workspace_slug)
        assert isinstance(types, list)

    def test_create_update_workspace_work_item_type(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating and updating a workspace-level work item type."""
        name = f"test-wit-{uuid4().hex[:8]}"
        data = CreateWorkItemType(name=name, description="Test workspace WIT", is_active=True)
        created = client.workspace_work_item_types.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        try:
            updated = client.workspace_work_item_types.update(
                workspace_slug,
                created.id,
                UpdateWorkItemType(description="Updated description"),
            )
            assert updated.id == created.id
            assert updated.description == "Updated description"
        finally:
            # No delete endpoint on workspace WITs per spec — log a warning if needed
            pass


class TestWorkspaceWorkItemTypeProperties:
    """Test WorkspaceWorkItemTypes.properties sub-resource."""

    def test_list_properties_for_workspace_wit(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing properties for a workspace work item type."""
        types = client.workspace_work_item_types.list(workspace_slug)
        if not types:
            pytest.skip("No workspace work item types available to test properties listing")

        wit = types[0]
        props = client.workspace_work_item_types.properties.list(workspace_slug, wit.id)
        assert isinstance(props, list)
