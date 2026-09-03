"""Live coverage for the `.work_items` bridge (api_v2): add/remove
link-management between a milestone and its work items, reached as
`...milestones.work_items.add(...)`/`.remove(...)`; offline coverage lives in
`tests/v2`."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2._kernel.errors import PlaneAPIError
from plane.api.v2.project import Project
from plane.client import PlaneClient
from plane.models.v2.milestones import CreateMilestone

from .helpers import unique_name


@pytest.fixture
def proj(client: PlaneClient, workspace_slug: str, project_id: str) -> Project:
    return client.v2.workspace(workspace_slug).project(project_id)


@pytest.fixture
def milestone(proj: Project) -> dict[str, Any]:
    created = proj.milestones.create(CreateMilestone(title=unique_name("milestone")))
    return created.model_dump()


class TestMilestoneWorkItems:
    def test_work_items_add_then_remove(
        self,
        proj: Project,
        milestone: dict[str, Any],
        work_item: Any,
    ) -> None:
        added = proj.milestones.work_items.add(str(milestone["id"]), [work_item.id])
        assert work_item.id in added

        removed = proj.milestones.work_items.remove(str(milestone["id"]), [work_item.id])
        assert work_item.id in removed

    def test_work_items_add_unknown_milestone_is_404(
        self,
        proj: Project,
        work_item: Any,
    ) -> None:
        with pytest.raises(PlaneAPIError) as exc_info:
            proj.milestones.work_items.add(
                "00000000-0000-0000-0000-000000000000",
                [work_item.id],
            )
        assert exc_info.value.status == 404
