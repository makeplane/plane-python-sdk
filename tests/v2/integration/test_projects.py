"""Live coverage for `ws.projects`, reached through the chain
(`client.v2.workspaces.projects`); no method takes a `workspace_slug`
parameter, and every detail method's first positional argument is `project`."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2.projects import Projects
from plane.client import PlaneClient
from plane.models.v2.projects import CreateProject, UpdateProject

from .helpers import unique_name


@pytest.fixture
def projects(client: PlaneClient) -> Projects:
    return client.v2.workspaces.projects


@pytest.fixture
def temp_project(projects: Projects, workspace_slug: str) -> Iterator[Any]:
    """A project created and torn down by this file, independent of the shared
    session `project` fixture, since these tests exercise `Projects` itself."""
    identifier = f"B{unique_name('').split('-')[-1][:8].upper()}"
    created = projects.create(
        workspace_slug, CreateProject(identifier=identifier, name=f"Projects IT {identifier}")
    )
    yield created
    try:
        projects.delete(workspace_slug, created.id)
    except Exception:
        pass


class TestProjects:
    def test_retrieve_by_uuid_and_by_identifier_agree(
        self, projects: Projects, temp_project: Any, workspace_slug: str
    ) -> None:
        by_id = projects.retrieve(workspace_slug, temp_project.id)
        by_key = projects.retrieve(workspace_slug, temp_project.identifier)
        assert by_id.id == by_key.id == temp_project.id

    def test_list_includes_the_created_project(
        self, projects: Projects, temp_project: Any, workspace_slug: str
    ) -> None:
        page = projects.list(workspace_slug, identifier=temp_project.identifier)
        assert any(row.id == temp_project.id for row in page.data)

    def test_update_renames_the_project(
        self, projects: Projects, temp_project: Any, workspace_slug: str
    ) -> None:
        updated = projects.update(
            workspace_slug, temp_project.identifier, UpdateProject(name="Renamed by projects IT")
        )
        assert updated.name == "Renamed by projects IT"

    def test_archive_then_unarchive_round_trip(
        self, projects: Projects, temp_project: Any, workspace_slug: str
    ) -> None:
        # `archive`/`unarchive` are 204-no-body, so they are typed `-> None`; the
        # evidence they worked is the round-trip below, not their return value.
        projects.archive(workspace_slug, temp_project.identifier)
        archived = projects.retrieve(workspace_slug, temp_project.identifier)
        assert archived.archived_at is not None

        projects.unarchive(workspace_slug, temp_project.identifier)
        restored = projects.retrieve(workspace_slug, temp_project.identifier)
        assert restored.archived_at is None

    def test_summary_reports_zero_counts_for_a_fresh_project(
        self, projects: Projects, temp_project: Any, workspace_slug: str
    ) -> None:
        summary = projects.summary(workspace_slug, temp_project.identifier)
        assert summary.id == temp_project.id
        assert summary.identifier == temp_project.identifier
        assert isinstance(summary.counts, dict)

    def test_summary_narrows_to_requested_counts(
        self, projects: Projects, temp_project: Any, workspace_slug: str
    ) -> None:
        summary = projects.summary(workspace_slug, temp_project.identifier, counts=["states"])
        assert set(summary.counts) <= {"states"}

    def test_upsert_reconciles_on_external_identity(
        self, projects: Projects, workspace_slug: str
    ) -> None:
        external_id = unique_name("project-ext")
        identifier = f"U{unique_name('').split('-')[-1][:8].upper()}"
        first = projects.upsert(
            workspace_slug,
            CreateProject(
                identifier=identifier,
                name="Upsert IT v1",
                external_id=external_id,
                external_source="projects-it",
            ),
        )
        try:
            second = projects.upsert(
                workspace_slug,
                CreateProject(
                    identifier=identifier,
                    name="Upsert IT v2",
                    external_id=external_id,
                    external_source="projects-it",
                ),
            )
            assert second.id == first.id
            assert second.name == "Upsert IT v2"
        finally:
            projects.delete(workspace_slug, first.id)

    def test_bulk_create_then_bulk_update(self, projects: Projects, workspace_slug: str) -> None:
        id_a = f"A{unique_name('').split('-')[-1][:8].upper()}"
        id_b = f"B{unique_name('').split('-')[-1][:8].upper()}"
        result = projects.bulk_create(
            workspace_slug,
            [
                CreateProject(identifier=id_a, name="Bulk A"),
                CreateProject(identifier=id_b, name="Bulk B"),
            ],
        )
        try:
            assert result.succeeded == 2
            ids = [row.id for row in result.results if hasattr(row, "id")]
            # Project names are unique per workspace (confirmed live) -- renaming
            # every row to the same literal string would 409 all but the first,
            # so each row needs its own new name.
            update_result = projects.bulk_update(
                workspace_slug,
                [{"id": pk, "name": f"Bulk renamed {i}"} for i, pk in enumerate(ids)],
            )
            assert update_result.succeeded == 2
        finally:
            for pk in [id_a, id_b]:
                try:
                    projects.delete(workspace_slug, pk)
                except Exception:
                    pass

    def test_projects_has_no_bulk_delete(self, projects: Projects) -> None:
        assert not hasattr(projects, "bulk_delete")

    def test_role_distribution_reflects_the_calling_member(
        self, projects: Projects, workspace_slug: str
    ) -> None:
        """The token's own membership counts toward at least one role."""
        report = projects.role_distribution(workspace_slug)
        assert report.total_memberships >= 1
        assert report.total_distinct_members >= 1
        assert sum(role.membership_count for role in report.roles) == report.total_memberships
