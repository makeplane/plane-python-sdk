"""End-to-end flow for WORKSPACE-managed work item types (port of plane-ee's
`tests/e2e/api_v2/workspace_work_item_types_flow.py`). Needs workspace mode; enabling it
is irreversible, so it only flips when PLANE_E2E_ENABLE_WORKSPACE_WORK_ITEM_TYPES=1."""

from __future__ import annotations

import os
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.project import Project
from plane.api.v2.workspace import Workspace
from plane.client import PlaneClient
from plane.models.v2.features import UpdateWorkspaceFeature
from plane.models.v2.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyContext,
    WorkItemPropertyContextOptionInput,
)
from plane.models.v2.work_item_types import CreateWorkItemType
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name

KEEP = os.environ.get("PLANE_E2E_KEEP") == "1"
MAY_ENABLE = os.environ.get("PLANE_E2E_ENABLE_WORKSPACE_WORK_ITEM_TYPES") == "1"


def _name(row: Any) -> str:
    return str(row["name"] if isinstance(row, dict) else row.name)


def _id(row: Any) -> str:
    return str(row["id"] if isinstance(row, dict) else row.id)


@pytest.fixture
def ws(client: PlaneClient, workspace_slug: str) -> Workspace:
    return client.v2.workspace(workspace_slug)


@pytest.fixture
def proj(ws: Workspace, project_id: str) -> Project:
    return ws.project(project_id)


@pytest.fixture(autouse=True)
def _require_workspace_mode(ws: Workspace) -> None:
    if ws.features.retrieve().is_work_item_types_enabled:
        return
    if not MAY_ENABLE:
        pytest.skip(
            "workspace is in project mode; set PLANE_E2E_ENABLE_WORKSPACE_WORK_ITEM_TYPES=1 "
            "to let this flow enable workspace-level types (irreversible)"
        )
    # 1. enable -- auto-creates a default workspace type and fans it out to every project
    feature = ws.features.update(UpdateWorkspaceFeature(is_work_item_types_enabled=True))
    assert feature.is_work_item_types_enabled is True


def test_workspace_work_item_types_flow(ws: Workspace, proj: Project, project_id: str) -> None:
    suffix = unique_name("")[1:]
    created_work_items: list[str] = []
    attached: list[str] = []
    properties: list[str] = []
    type_id: str | None = None

    try:
        # 2. create a workspace-owned type
        type_name = f"WS Type {suffix}"
        wtype = ws.work_item_types.create(CreateWorkItemType(name=type_name))
        type_id = wtype.id

        # 3. list + retrieve
        assert any(row.id == type_id for row in ws.work_item_types.list().data)
        assert ws.work_item_types.retrieve(type_id).id == type_id

        # 4-5. workspace TEXT + OPTION properties (option values come from the context below)
        text_prop = ws.work_item_properties.create(
            CreateWorkItemProperty(display_name=f"Severity {suffix}", property_type="TEXT")
        )
        properties.append(text_prop.id)
        option_prop = ws.work_item_properties.create(
            CreateWorkItemProperty(display_name=f"Tier {suffix}", property_type="OPTION")
        )
        properties.append(option_prop.id)
        sev_key, tier_key = text_prop.name, option_prop.name
        assert sev_key and tier_key

        # 6. scope the OPTION property to this project + type via a context, with its options
        context = ws.work_item_properties.contexts.create(
            option_prop.id,
            CreateWorkItemPropertyContext(
                name=f"Bug-only {suffix}",
                is_required=False,
                applies_to_all_projects=False,
                applies_to_all_work_item_types=False,
                project_ids=[project_id],
                issue_type_ids=[type_id],
                options=[
                    WorkItemPropertyContextOptionInput(name="Gold", is_default=True),
                    WorkItemPropertyContextOptionInput(name="Silver"),
                ],
            ),
        )
        gold_id = next(_id(o) for o in context.options or [] if _name(o) == "Gold")

        # 7. attach both properties to the workspace type
        result = ws.work_item_types.properties.attach(type_id, [text_prop.id, option_prop.id])
        attached.extend([text_prop.id, option_prop.id])
        assert {text_prop.id, option_prop.id}.issubset(set(result.properties))

        # 8. import the workspace type into the project
        proj.work_item_types.import_types([type_id])
        assert any(row.id == type_id for row in proj.work_item_types.list().data)

        # 9-10. create a work item of the imported type with custom_fields, read it back
        item = proj.work_items.create(
            CreateWorkItem(
                name="WS-mode work item",
                type_id=type_id,
                custom_fields={sev_key: "high", tier_key: gold_id},
            )
        )
        created_work_items.append(item.id)
        assert item.custom_fields is not None
        assert item.custom_fields[sev_key]["value"] == "high"  # type: ignore[index]
        assert proj.work_items.retrieve(item.id).id == item.id

        # 11. project-level type writes are blocked in workspace mode
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.work_item_types.create(CreateWorkItemType(name="nope"))
        assert exc_info.value.status == 409
        assert exc_info.value.code == "work_item_types_managed_at_workspace"
    finally:
        if not KEEP:
            for work_item_id in created_work_items:
                _swallow(proj.work_items.delete, work_item_id)
            for property_id in attached:
                _swallow(ws.work_item_types.properties.detach, type_id or "", property_id)
            for property_id in properties:
                _swallow(ws.work_item_properties.delete, property_id)
            if type_id:
                _swallow(ws.work_item_types.delete, type_id)


def _swallow(action: Any, *args: Any) -> None:
    """Best-effort cleanup step; failures are collected and reported at the end."""
    try:
        action(*args)
    except Exception as exc:
        _cleanup_failures.append(f"{getattr(action, '__qualname__', action)}{args}: {exc}")


_cleanup_failures: list[str] = []


@pytest.fixture(autouse=True)
def _report_cleanup_failures() -> Any:
    _cleanup_failures.clear()
    yield
    assert not _cleanup_failures, "cleanup left rows behind:\n" + "\n".join(_cleanup_failures)
