"""Offline coverage for project/workspace work item templates plus the project-only `use` action,
which returns a `WorkItem`."""

from __future__ import annotations

import json

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.work_item_templates.project import ProjectWorkItemTemplates
from plane.api.v2.work_item_templates.workspace import WorkspaceWorkItemTemplates
from plane.config import Configuration
from plane.models.v2.work_item_templates import (
    CreateWorkItemTemplate,
    UpdateWorkItemTemplate,
    WorkItemTemplateData,
    WorkItemTemplateUse,
)

BASE = "https://api.example.com/api/v2"


@pytest.fixture
def project_templates(config: Configuration) -> ProjectWorkItemTemplates:
    return ProjectWorkItemTemplates(V2Transport(config), slug="acme", project_id="ENG")


@pytest.fixture
def workspace_templates(config: Configuration) -> WorkspaceWorkItemTemplates:
    return WorkspaceWorkItemTemplates(V2Transport(config), slug="acme")


@responses.activate
def test_project_templates_crud(project_templates: ProjectWorkItemTemplates) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/projects/ENG/work-item-templates/",
        json={
            "data": [{"id": "1", "name": "Bug report"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.post(
        f"{BASE}/workspaces/acme/projects/ENG/work-item-templates/",
        json={"id": "2", "name": "Feature request"},
        status=201,
    )
    responses.patch(
        f"{BASE}/workspaces/acme/projects/ENG/work-item-templates/2/",
        json={"id": "2", "name": "Feature"},
    )
    responses.delete(f"{BASE}/workspaces/acme/projects/ENG/work-item-templates/2/", status=204)

    page = project_templates.list()
    assert page.data[0].name == "Bug report"

    created = project_templates.create(
        CreateWorkItemTemplate(
            name="Feature request", template_data=WorkItemTemplateData(name="Feature request")
        ),
    )
    assert created.id == "2"

    updated = project_templates.update(created.id, UpdateWorkItemTemplate(name="Feature"))
    assert updated.name == "Feature"

    assert project_templates.delete(created.id) is None


@responses.activate
def test_project_template_use_parses_a_work_item_not_a_template(
    project_templates: ProjectWorkItemTemplates,
) -> None:
    """`use` returns a `WorkItem`, not this resource's own `model`
    (`WorkItemTemplate`) -- this is why it cannot go through `_action`."""
    responses.post(
        f"{BASE}/workspaces/acme/projects/ENG/work-item-templates/1/use/",
        json={"id": "wi-1", "name": "Feature request", "sequence_id": 42},
        status=201,
    )

    work_item = project_templates.use("1")

    assert work_item.id == "wi-1"
    assert work_item.sequence_id == 42
    assert responses.calls[0].request.body is None


@responses.activate
def test_project_template_use_sends_overrides(
    project_templates: ProjectWorkItemTemplates,
) -> None:
    responses.post(
        f"{BASE}/workspaces/acme/projects/ENG/work-item-templates/1/use/",
        json={"id": "wi-1", "name": "Custom name"},
        status=201,
    )

    project_templates.use("1", WorkItemTemplateUse(name="Custom name"))

    body = json.loads(responses.calls[0].request.body)
    assert body == {"name": "Custom name"}


@responses.activate
def test_workspace_templates_crud(workspace_templates: WorkspaceWorkItemTemplates) -> None:
    responses.get(
        f"{BASE}/workspaces/acme/work-item-templates/",
        json={"data": [{"id": "1", "name": "Bug report"}], "pagination": {"style": "offset"}},
    )
    responses.post(
        f"{BASE}/workspaces/acme/work-item-templates/",
        json={"id": "2", "name": "Feature request"},
        status=201,
    )

    page = workspace_templates.list()
    assert page.data[0].name == "Bug report"

    created = workspace_templates.create(
        CreateWorkItemTemplate(
            name="Feature request", template_data=WorkItemTemplateData(name="Feature request")
        ),
    )
    assert created.id == "2"


def test_workspace_templates_have_no_use_action(
    workspace_templates: WorkspaceWorkItemTemplates,
) -> None:
    """`use` is only offered on the project-scoped variant in the golden -- there
    is no `.../work-item-templates/{pk}/use/` route under `.../workspaces/{slug}/
    work-item-templates/`."""
    assert not hasattr(workspace_templates, "use")
