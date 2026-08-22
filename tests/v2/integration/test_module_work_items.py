"""Live coverage for `manage_work_items` (api_v2): add/remove link-management
between a module and its work items, reached as
`...modules.manage_work_items(...)`; offline coverage lives in `tests/v2`."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2.project import Project
from plane.client import PlaneClient
from plane.models.v2.module_work_items import ModuleWorkItemManageRequest
from plane.models.v2.modules import CreateModule

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def module(proj: Project) -> dict[str, Any]:
    created = proj.modules.create(CreateModule(name=unique_name("module")))
    return created.model_dump()


class TestModuleWorkItems:
    def test_manage_adds_then_removes_a_work_item(
        self,
        proj: Project,
        module: dict[str, Any],
        work_item: Any,
    ) -> None:
        added = proj.modules.manage_work_items(
            str(module["id"]),
            ModuleWorkItemManageRequest(add=[work_item.id]),
        )
        assert work_item.id in added.added

        removed = proj.modules.manage_work_items(
            str(module["id"]),
            ModuleWorkItemManageRequest(remove=[work_item.id]),
        )
        assert work_item.id in removed.removed

    def test_manage_over_100_ids_is_rejected_client_side(
        self,
        proj: Project,
        module: dict[str, Any],
    ) -> None:
        """The pydantic DTO enforces the golden's `maxItems: 100` before the
        request is ever sent -- this never reaches the server."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ModuleWorkItemManageRequest(
                add=[f"00000000-0000-0000-0000-{i:012d}" for i in range(101)]
            )
