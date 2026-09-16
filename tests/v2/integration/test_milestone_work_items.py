"""Live coverage for the `.work_items` bridge (api_v2): add/remove link-management
between a milestone and its work items; offline coverage lives in `tests/v2`.

The happy path goes through the loaded milestone (`milestone.work_items.add([...])`),
which is where a bridge is meant to be reached from. The 404 case cannot: there is no
row to load for an id that does not exist, so it takes the flat path -- the one place
in this file where the milestone id is written out."""

from __future__ import annotations

from typing import Any

import pytest

from plane.api.v2 import LoadedProject, PlaneAPIError
from plane.client import PlaneClient
from plane.models.v2.milestones import CreateMilestone

from .helpers import unique_name


@pytest.fixture
def milestone(project: LoadedProject) -> Any:
    """The loaded row, not a `model_dump()` of it -- dumping it threw away the very
    navigation this file is about."""
    return project.milestones.create(CreateMilestone(title=unique_name("milestone")))


class TestMilestoneWorkItems:
    def test_work_items_add_then_remove(
        self,
        milestone: Any,
        work_item: Any,
    ) -> None:
        added = milestone.work_items.add([work_item.id])
        assert work_item.id in added

        removed = milestone.work_items.remove([work_item.id])
        assert work_item.id in removed

    def test_work_items_add_unknown_milestone_is_404(
        self,
        client: PlaneClient,
        workspace_slug: str,
        project_id: str,
        work_item: Any,
    ) -> None:
        """Flat path by necessity: a milestone that does not exist cannot be fetched,
        so there is no loaded row to hang the bridge off."""
        with pytest.raises(PlaneAPIError) as exc_info:
            client.v2.workspaces.projects.milestones.work_items.add(
                workspace_slug,
                project_id,
                "00000000-0000-0000-0000-000000000000",
                [work_item.id],
            )
        assert exc_info.value.status == 404
