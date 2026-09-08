"""Live coverage for the `work_item_templates` resource, both project- and
workspace-scoped. Reuses shared `client`/`workspace_slug`/`project_id`
fixtures; the disposable template is local to this file."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.models.v2.work_item_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplateData,
    WorkItemTemplateUse,
)

from .helpers import unique_name


@pytest.fixture
def project_template(project: LoadedProject) -> Iterator[Any]:
    created = project.work_item_templates.create(
        CreateWorkItemTemplate(
            name=unique_name("template"),
            template_data=WorkItemTemplateData(name="Templated work item"),
        ),
    )
    yield created
    try:
        project.work_item_templates.delete(created.id)
    except Exception:
        pass


class TestProjectWorkItemTemplates:
    def test_list_includes_the_created_template(self, project: LoadedProject, project_template: Any) -> None:
        page = project.work_item_templates.list()
        assert any(row.id == project_template.id for row in page.data)

    def test_retrieve_returns_the_seed_data(self, project: LoadedProject, project_template: Any) -> None:
        fetched = project.work_item_templates.retrieve(project_template.id)
        assert fetched.id == project_template.id
        assert fetched.template_data is not None

    def test_patch_updates_the_name(self, project: LoadedProject, project_template: Any) -> None:
        updated = project.work_item_templates.update(
            project_template.id, UpdateWorkItemTemplate(name="Renamed template")
        )
        assert updated.name == "Renamed template"

    def test_use_instantiates_a_work_item(self, project: LoadedProject, project_template: Any) -> None:
        work_item = project.work_item_templates.use(project_template.id)
        try:
            assert work_item.id
            assert work_item.name == "Templated work item"
        finally:
            project.work_items.delete(work_item.id)

    def test_use_honors_a_name_override(self, project: LoadedProject, project_template: Any) -> None:
        work_item = project.work_item_templates.use(
            project_template.id, WorkItemTemplateUse(name="Overridden name")
        )
        try:
            assert work_item.name == "Overridden name"
        finally:
            project.work_items.delete(work_item.id)

    def test_delete_then_retrieve_404s(self, project: LoadedProject) -> None:
        created = project.work_item_templates.create(
            CreateWorkItemTemplate(
                name=unique_name("template"), template_data=WorkItemTemplateData(name="Throwaway")
            ),
        )
        project.work_item_templates.delete(created.id)
        with pytest.raises(PlaneAPIError) as exc_info:
            project.work_item_templates.retrieve(created.id)
        assert exc_info.value.status == 404


class TestWorkspaceWorkItemTemplates:
    def test_create_list_delete_round_trip(self, client: PlaneClient, workspace_slug: str) -> None:
        templates = client.v2.workspace(workspace_slug).work_item_templates
        created = templates.create(
            CreateWorkItemTemplate(
                name=unique_name("ws-template"),
                template_data=WorkItemTemplateData(name="Any templated item"),
            ),
        )
        try:
            page = templates.list()
            assert any(row.id == created.id for row in page.data)
        finally:
            templates.delete(created.id)

    def test_has_no_use_action(self, client: PlaneClient, workspace_slug: str) -> None:
        templates = client.v2.workspace(workspace_slug).work_item_templates
        assert not hasattr(templates, "use")
