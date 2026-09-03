"""Live coverage for the `.work_items` bridge (api_v2): add/remove
link-management between a module and its work items, reached as
`...modules.work_items.add(...)`/`.remove(...)`; offline coverage lives in
`tests/v2`."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2.project import Project
from plane.client import PlaneClient
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
    def test_work_items_add_then_remove(
        self,
        proj: Project,
        module: dict[str, Any],
        work_item: Any,
    ) -> None:
        added = proj.modules.work_items.add(str(module["id"]), [work_item.id])
        assert work_item.id in added

        removed = proj.modules.work_items.remove(str(module["id"]), [work_item.id])
        assert work_item.id in removed

    def test_work_items_add_over_100_ids_is_rejected_client_side(
        self,
        proj: Project,
        module: dict[str, Any],
    ) -> None:
        """The bridge kernel enforces the golden's `maxItems: 100` before the
        request is ever sent -- this never reaches the server."""
        with pytest.raises(ValueError):
            proj.modules.work_items.add(
                str(module["id"]),
                [f"00000000-0000-0000-0000-{i:012d}" for i in range(101)],
            )
