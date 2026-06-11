"""Integration tests for work item dependency and custom relation endpoints."""

import warnings
from uuid import uuid4

import pytest

from plane.client import PlaneClient
from plane.errors.errors import HttpError
from plane.models.projects import Project
from plane.models.work_item_relation_definitions import (
    CreateWorkItemRelationDefinition,
)
from plane.models.work_items import (
    CreateWorkItem,
    CreateWorkItemCustomRelation,
    CreateWorkItemDependency,
    RemoveWorkItemCustomRelation,
    RemoveWorkItemDependency,
    WorkItemDependencyResponse,
    WorkItemWithRelationType,
)

# ── Fixtures ──────────────────────────────────────────────────────────────────


@pytest.fixture(scope="class")
def work_item_a(client: PlaneClient, workspace_slug: str, project: Project):
    """First work item used as the source in relation tests."""
    item = client.work_items.create(
        workspace_slug, project.id, CreateWorkItem(name=f"relation-test-a-{uuid4().hex[:6]}")
    )
    yield item
    try:
        client.work_items.delete(workspace_slug, project.id, item.id)
    except HttpError as exc:
        warnings.warn(f"Teardown failed for work item {item.id}: {exc}", stacklevel=1)


@pytest.fixture(scope="class")
def work_item_b(client: PlaneClient, workspace_slug: str, project: Project):
    """Second work item used as the target in relation tests."""
    item = client.work_items.create(
        workspace_slug, project.id, CreateWorkItem(name=f"relation-test-b-{uuid4().hex[:6]}")
    )
    yield item
    try:
        client.work_items.delete(workspace_slug, project.id, item.id)
    except HttpError as exc:
        warnings.warn(f"Teardown failed for work item {item.id}: {exc}", stacklevel=1)


@pytest.fixture(scope="class")
def custom_definition(client: PlaneClient, workspace_slug: str):
    """Workspace relation definition used in custom relation tests."""
    suffix = uuid4().hex[:8]
    defn = client.work_item_relation_definitions.create(
        workspace_slug,
        CreateWorkItemRelationDefinition(
            name=f"test-rel-{suffix}",
            outward=f"test-outward-{suffix}",
            inward=f"test-inward-{suffix}",
            is_active=True,
        ),
    )
    yield defn
    try:
        client.work_item_relation_definitions.delete(workspace_slug, defn.id)
    except HttpError as exc:
        warnings.warn(f"Teardown failed for definition {defn.id}: {exc}", stacklevel=1)


# ── Dependency tests ──────────────────────────────────────────────────────────


class TestWorkItemDependencies:
    """Tests for the /relation-dependencies/ endpoint."""

    def test_list_dependencies_empty(
        self, client: PlaneClient, workspace_slug: str, project: Project, work_item_a
    ) -> None:
        """Listing dependencies on a fresh work item returns empty groups."""
        result = client.work_items.dependencies.list(workspace_slug, project.id, work_item_a.id)
        assert isinstance(result, WorkItemDependencyResponse)
        assert result.blocking == []
        assert result.blocked_by == []
        assert result.start_before == []
        assert result.start_after == []
        assert result.finish_before == []
        assert result.finish_after == []

    def test_create_blocking_dependency(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
    ) -> None:
        """Creating a 'blocking' dependency returns the target with relation_type set."""
        created = client.work_items.dependencies.create(
            workspace_slug,
            project.id,
            work_item_a.id,
            CreateWorkItemDependency(
                relation_type="blocking",
                work_item_ids=[work_item_b.id],
            ),
        )
        assert isinstance(created, list)
        assert len(created) == 1
        item = created[0]
        assert isinstance(item, WorkItemWithRelationType)
        assert item.id == work_item_b.id
        assert item.relation_type == "blocking"

    def test_list_dependencies_after_create(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
    ) -> None:
        """After creating a blocking dependency, list returns it in the blocking group."""
        result = client.work_items.dependencies.list(workspace_slug, project.id, work_item_a.id)
        assert isinstance(result, WorkItemDependencyResponse)
        blocking_ids = [wi.id for wi in result.blocking]
        assert work_item_b.id in blocking_ids

    def test_list_reverse_dependency(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
    ) -> None:
        """The target sees the reverse dependency (blocked_by) in its own list."""
        result = client.work_items.dependencies.list(workspace_slug, project.id, work_item_b.id)
        blocked_by_ids = [wi.id for wi in result.blocked_by]
        assert work_item_a.id in blocked_by_ids

    def test_remove_dependency(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
    ) -> None:
        """Removing a dependency clears it from both sides."""
        client.work_items.dependencies.remove(
            workspace_slug,
            project.id,
            work_item_a.id,
            RemoveWorkItemDependency(work_item_id=work_item_b.id),
        )
        result = client.work_items.dependencies.list(workspace_slug, project.id, work_item_a.id)
        blocking_ids = [wi.id for wi in result.blocking]
        assert work_item_b.id not in blocking_ids

    def test_create_all_dependency_types(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
    ) -> None:
        """All six dependency directions are accepted by the API."""
        dep_types = [
            "blocking",
            "blocked_by",
            "start_before",
            "start_after",
            "finish_before",
            "finish_after",
        ]
        created_any = False
        for dep_type in dep_types:
            result = client.work_items.dependencies.create(
                workspace_slug,
                project.id,
                work_item_a.id,
                CreateWorkItemDependency(
                    relation_type=dep_type,
                    work_item_ids=[work_item_b.id],
                ),
            )
            assert isinstance(result, list)
            created_any = True
            # clean up immediately to avoid duplicate constraint issues
            client.work_items.dependencies.remove(
                workspace_slug,
                project.id,
                work_item_a.id,
                RemoveWorkItemDependency(work_item_id=work_item_b.id),
            )
        assert created_any


# ── Custom relation tests ──────────────────────────────────────────────────────


class TestWorkItemCustomRelations:
    """Tests for the /work-item-relations/ endpoint."""

    def test_list_custom_relations_empty(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        custom_definition,
    ) -> None:
        """Listing custom relations returns a dict keyed by definition labels."""
        result = client.work_items.custom_relations.list(workspace_slug, project.id, work_item_a.id)
        assert isinstance(result, dict)
        # Active definitions must appear as keys
        assert custom_definition.outward in result
        assert custom_definition.inward in result
        assert result[custom_definition.outward] == []
        assert result[custom_definition.inward] == []

    def test_create_custom_relation_outward(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
        custom_definition,
    ) -> None:
        """Creating an outward relation returns targets with relation_type as outward label."""
        created = client.work_items.custom_relations.create(
            workspace_slug,
            project.id,
            work_item_a.id,
            CreateWorkItemCustomRelation(
                relation_definition_id=custom_definition.id,
                relation_definition_type=custom_definition.outward,
                work_item_ids=[work_item_b.id],
            ),
        )
        assert isinstance(created, list)
        assert len(created) == 1
        item = created[0]
        assert isinstance(item, WorkItemWithRelationType)
        assert item.id == work_item_b.id
        assert item.relation_type == custom_definition.outward

    def test_list_custom_relations_after_create(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
        custom_definition,
    ) -> None:
        """After creating an outward relation, the source sees it under the outward label."""
        result = client.work_items.custom_relations.list(workspace_slug, project.id, work_item_a.id)
        outward_ids = [wi.id for wi in result.get(custom_definition.outward, [])]
        assert work_item_b.id in outward_ids

    def test_list_custom_relations_inward_side(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
        custom_definition,
    ) -> None:
        """The target sees the relation under the inward label."""
        result = client.work_items.custom_relations.list(workspace_slug, project.id, work_item_b.id)
        inward_ids = [wi.id for wi in result.get(custom_definition.inward, [])]
        assert work_item_a.id in inward_ids

    def test_remove_custom_relation(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
        custom_definition,
    ) -> None:
        """Removing a custom relation clears it from both sides."""
        client.work_items.custom_relations.remove(
            workspace_slug,
            project.id,
            work_item_a.id,
            RemoveWorkItemCustomRelation(work_item_id=work_item_b.id),
        )
        result = client.work_items.custom_relations.list(workspace_slug, project.id, work_item_a.id)
        outward_ids = [wi.id for wi in result.get(custom_definition.outward, [])]
        assert work_item_b.id not in outward_ids

    def test_create_custom_relation_inward(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
        custom_definition,
    ) -> None:
        """Creating an inward relation (reversed directionality) is accepted by the API."""
        created = client.work_items.custom_relations.create(
            workspace_slug,
            project.id,
            work_item_a.id,
            CreateWorkItemCustomRelation(
                relation_definition_id=custom_definition.id,
                relation_definition_type=custom_definition.inward,
                work_item_ids=[work_item_b.id],
            ),
        )
        assert isinstance(created, list)
        assert len(created) == 1
        assert created[0].relation_type == custom_definition.inward

        # clean up
        client.work_items.custom_relations.remove(
            workspace_slug,
            project.id,
            work_item_a.id,
            RemoveWorkItemCustomRelation(work_item_id=work_item_b.id),
        )

    def test_create_relation_invalid_definition(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project: Project,
        work_item_a,
        work_item_b,
    ) -> None:
        """Using a non-existent definition UUID returns a 4xx error."""
        with pytest.raises(HttpError):
            client.work_items.custom_relations.create(
                workspace_slug,
                project.id,
                work_item_a.id,
                CreateWorkItemCustomRelation(
                    relation_definition_id=str(uuid4()),
                    relation_definition_type="nonexistent",
                    work_item_ids=[work_item_b.id],
                ),
            )
