"""Unit tests for WorkItemRelationDefinitions API resource (smoke tests with real HTTP requests)."""

import warnings
from uuid import uuid4

from plane.client import PlaneClient
from plane.models.work_item_relation_definitions import (
    CreateWorkItemRelationDefinition,
    UpdateWorkItemRelationDefinition,
)


class TestWorkItemRelationDefinitions:
    """Test WorkItemRelationDefinitions API resource."""

    def test_list_relation_definitions(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing work item relation definitions."""
        definitions = client.work_item_relation_definitions.list(workspace_slug)
        assert isinstance(definitions, list)

    def test_list_relation_definitions_with_filters(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test listing relation definitions with is_default and is_active filters."""
        filtered = client.work_item_relation_definitions.list(
            workspace_slug, is_default=False, is_active=True
        )
        assert isinstance(filtered, list)

    def test_create_update_delete_relation_definition(
        self, client: PlaneClient, workspace_slug: str
    ) -> None:
        """Test creating, updating, and deleting a work item relation definition."""
        name = f"test-rel-{uuid4().hex[:8]}"
        data = CreateWorkItemRelationDefinition(
            name=name,
            outward="blocks",
            inward="is blocked by",
            is_active=True,
        )
        created = client.work_item_relation_definitions.create(workspace_slug, data)
        assert created is not None
        assert created.id is not None
        assert created.name == name

        try:
            updated = client.work_item_relation_definitions.update(
                workspace_slug,
                created.id,
                UpdateWorkItemRelationDefinition(outward="depends on"),
            )
            assert updated.id == created.id
            assert updated.outward == "depends on"
        finally:
            try:
                client.work_item_relation_definitions.delete(workspace_slug, created.id)
            except Exception as exc:
                warnings.warn(
                    f"Teardown failed for relation definition {created.id}: {exc}", stacklevel=1
                )
