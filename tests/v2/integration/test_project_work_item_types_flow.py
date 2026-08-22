"""End-to-end flow for PROJECT-managed work item types (port of plane-ee's
`tests/e2e/api_v2/project_work_item_types_flow.py`). Runs only when the workspace is
in project mode; set PLANE_E2E_KEEP=1 to leave the created rows for inspection."""

from __future__ import annotations

import os
from typing import Any

import pytest

from plane.api.v2 import PlaneAPIError
from plane.api.v2.project import Project
from plane.api.v2.workspace import Workspace
from plane.client import PlaneClient
from plane.models.v2.work_item_properties import (
    CreateWorkItemProperty,
    CreateWorkItemPropertyOption,
)
from plane.models.v2.work_item_types import CreateWorkItemType
from plane.models.v2.work_items import CreateWorkItem

from .helpers import unique_name

KEEP = os.environ.get("PLANE_E2E_KEEP") == "1"


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
def _require_project_mode(ws: Workspace) -> None:
    if ws.features.retrieve().is_work_item_types_enabled:
        pytest.skip("workspace manages work item types at the workspace level; needs project mode")


def test_project_work_item_types_flow(proj: Project) -> None:
    suffix = unique_name("")[1:]
    created_work_items: list[str] = []
    attached: list[str] = []
    properties: list[str] = []
    type_id: str | None = None

    try:
        # 1. enable -- bootstraps the project's default (non-epic) type
        enabled = proj.work_item_types.enable()
        assert enabled.is_epic is False

        # 2. create a project-owned type
        type_name = f"E2E Type {suffix}"
        wtype = proj.work_item_types.create(CreateWorkItemType(name=type_name))
        type_id = wtype.id
        assert wtype.name == type_name
        assert wtype.is_epic is False

        # 3. list + retrieve + schema
        assert any(row.id == type_id for row in proj.work_item_types.list().data)
        assert proj.work_item_types.retrieve(type_id).id == type_id
        schema = proj.work_item_types.schema(type_id)
        assert schema.fields is not None
        assert schema.custom_fields is not None

        # 4. TEXT property
        text_prop = proj.work_item_properties.create(
            CreateWorkItemProperty(display_name=f"Severity {suffix}", property_type="TEXT")
        )
        properties.append(text_prop.id)
        sev_key = text_prop.name  # slugified display_name; the custom_fields key
        assert sev_key

        # 5. OPTION property with inline options
        option_prop = proj.work_item_properties.create(
            CreateWorkItemProperty(
                display_name=f"Tier {suffix}",
                property_type="OPTION",
                options=[
                    CreateWorkItemPropertyOption(name="Gold", is_default=True),
                    CreateWorkItemPropertyOption(name="Silver"),
                ],
            )
        )
        properties.append(option_prop.id)
        tier_key = option_prop.name
        assert tier_key
        assert {_name(o) for o in option_prop.options or []} == {"Gold", "Silver"}
        gold_id = next(_id(o) for o in option_prop.options or [] if _name(o) == "Gold")

        # 6. add one more option through the options endpoint
        proj.work_item_properties.options.create(
            option_prop.id, CreateWorkItemPropertyOption(name="Bronze")
        )
        names = {row.name for row in proj.work_item_properties.options.list(option_prop.id).data}
        assert names == {"Gold", "Silver", "Bronze"}

        # 7. a second default option is rejected
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.work_item_properties.options.create(
                option_prop.id, CreateWorkItemPropertyOption(name="Platinum", is_default=True)
            )
        assert exc_info.value.status == 400

        # 8. attach both properties to the type
        result = proj.work_item_types.properties.attach(type_id, [text_prop.id, option_prop.id])
        attached.extend([text_prop.id, option_prop.id])
        assert {text_prop.id, option_prop.id}.issubset(set(result.properties))
        listed = {row.id for row in proj.work_item_types.properties.list(type_id).data}
        assert {text_prop.id, option_prop.id}.issubset(listed)

        # 9. create a work item of this type with custom_fields, read it back
        item = proj.work_items.create(
            CreateWorkItem(
                name="E2E work item",
                type_id=type_id,
                custom_fields={sev_key: "high", tier_key: gold_id},
            )
        )
        created_work_items.append(item.id)
        assert item.custom_fields is not None
        assert item.custom_fields[sev_key]["value"] == "high"  # type: ignore[index]
        assert item.custom_fields[tier_key]["value_detail"]["name"] == "Gold"  # type: ignore[index]

        fetched = proj.work_items.retrieve(item.id)
        assert fetched.custom_fields is not None
        assert fetched.custom_fields[sev_key]["value"] == "high"  # type: ignore[index]

        # 10. the readable `type` name resolves to the same type
        item2 = proj.work_items.create(CreateWorkItem(name="E2E by type name", type=type_name))
        created_work_items.append(item2.id)
        assert item2.type_id == type_id

        # 11. mark-default
        assert proj.work_item_types.mark_default(type_id).is_default is True
    finally:
        if not KEEP:
            for work_item_id in created_work_items:
                _swallow(proj.work_items.delete, work_item_id)
            for property_id in attached:
                _swallow(proj.work_item_types.properties.detach, type_id or "", property_id)
            for property_id in properties:
                _swallow(proj.work_item_properties.delete, property_id)

    if not KEEP and type_id:
        # the type is now the project default, so delete is refused
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.work_item_types.delete(type_id)
        assert exc_info.value.status == 409


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
