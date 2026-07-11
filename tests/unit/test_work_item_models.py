"""Pure model-validation tests for work item response models (no HTTP).

The Plane API returns ``assignees`` and ``labels`` on a work item as bare UUID
strings unless the request expands them (``expand=assignees,labels``), in which
case they come back as nested objects. ``WorkItemDetail`` must accept both
shapes — the same tolerance it already grants ``state`` (``str | StateLite``).
"""

from plane.models.labels import Label
from plane.models.users import UserLite
from plane.models.work_items import WorkItemDetail


class TestWorkItemDetailRelations:
    def test_accepts_unexpanded_id_lists(self) -> None:
        """Default (unexpanded) responses carry bare UUID strings."""
        item = WorkItemDetail.model_validate(
            {
                "id": "wi-1",
                "assignees": ["00000000-0000-0000-0000-000000000001"],
                "labels": ["00000000-0000-0000-0000-000000000002"],
                "state": "00000000-0000-0000-0000-000000000003",
            }
        )
        assert item.assignees == ["00000000-0000-0000-0000-000000000001"]
        assert item.labels == ["00000000-0000-0000-0000-000000000002"]
        assert item.state == "00000000-0000-0000-0000-000000000003"

    def test_accepts_expanded_object_lists(self) -> None:
        """``expand=assignees,labels`` responses carry nested objects."""
        item = WorkItemDetail.model_validate(
            {
                "id": "wi-1",
                "assignees": [{"id": "u-1", "display_name": "henry"}],
                "labels": [{"id": "l-1", "name": "bug"}],
                "state": {"id": "s-1", "name": "Todo"},
            }
        )
        assert isinstance(item.assignees[0], UserLite)
        assert item.assignees[0].id == "u-1"
        assert isinstance(item.labels[0], Label)
        assert item.labels[0].name == "bug"

    def test_defaults_to_empty_lists(self) -> None:
        """Absent relations default to empty lists, not None."""
        item = WorkItemDetail.model_validate({"id": "wi-1"})
        assert item.assignees == []
        assert item.labels == []
