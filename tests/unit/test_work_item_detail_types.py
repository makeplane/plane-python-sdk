"""Unit tests for WorkItemDetail model type compatibility with Plane v1.3.0+.

Plane v1.3.0 changed the API to return labels and assignees as UUID strings
instead of expanded objects, even when not using the `fields` sparse parameter.
These tests verify that WorkItemDetail handles both representations.
"""

import pytest
from pydantic import ValidationError

from plane.models.work_items import WorkItemDetail


MINIMAL_WORK_ITEM = {
    "id": "ef6bf853-fecb-433e-a4e3-8546e60abebd",
    "name": "Test issue",
    "sequence_id": 1,
}


class TestWorkItemDetailLabelsAssigneesTypes:
    """WorkItemDetail should accept labels/assignees as UUID strings or objects."""

    def test_labels_as_uuid_strings(self) -> None:
        """Plane v1.3.0 returns labels as UUID strings — must not raise."""
        data = {
            **MINIMAL_WORK_ITEM,
            "labels": ["f6a24a78-a275-4fd1-a777-0e9e0e99dbef"],
            "assignees": [],
        }
        item = WorkItemDetail(**data)
        assert item.labels == ["f6a24a78-a275-4fd1-a777-0e9e0e99dbef"]

    def test_assignees_as_uuid_strings(self) -> None:
        """Plane v1.3.0 returns assignees as UUID strings — must not raise."""
        data = {
            **MINIMAL_WORK_ITEM,
            "labels": [],
            "assignees": ["48b05854-3e71-44f0-9fcb-7a5d6887f5ec"],
        }
        item = WorkItemDetail(**data)
        assert item.assignees == ["48b05854-3e71-44f0-9fcb-7a5d6887f5ec"]

    def test_both_as_uuid_strings(self) -> None:
        """Both fields as UUID strings simultaneously."""
        data = {
            **MINIMAL_WORK_ITEM,
            "labels": [
                "f6a24a78-a275-4fd1-a777-0e9e0e99dbef",
                "a8509ac8-7c71-4b9e-9a4a-623ef2c2365b",
            ],
            "assignees": ["48b05854-3e71-44f0-9fcb-7a5d6887f5ec"],
        }
        item = WorkItemDetail(**data)
        assert len(item.labels) == 2
        assert len(item.assignees) == 1

    def test_labels_as_objects(self) -> None:
        """Expanded label objects (pre-v1.3.0 behavior) still parse correctly."""
        data = {
            **MINIMAL_WORK_ITEM,
            "labels": [
                {
                    "id": "f6a24a78-a275-4fd1-a777-0e9e0e99dbef",
                    "name": "v3",
                    "color": "#FF6900",
                    "project": "9aa02e26-3b44-4fd2-96f9-015aa9ee7a52",
                    "workspace": "0f4d413a-a164-4168-aa31-abbdaa0aecd1",
                }
            ],
            "assignees": [],
        }
        item = WorkItemDetail(**data)
        assert len(item.labels) == 1

    def test_assignees_as_objects(self) -> None:
        """Expanded assignee objects (pre-v1.3.0 behavior) still parse correctly."""
        data = {
            **MINIMAL_WORK_ITEM,
            "labels": [],
            "assignees": [
                {
                    "id": "48b05854-3e71-44f0-9fcb-7a5d6887f5ec",
                    "display_name": "vic",
                    "avatar": None,
                    "is_bot": False,
                }
            ],
        }
        item = WorkItemDetail(**data)
        assert len(item.assignees) == 1

    def test_empty_lists(self) -> None:
        """Empty lists for both fields are valid."""
        data = {**MINIMAL_WORK_ITEM, "labels": [], "assignees": []}
        item = WorkItemDetail(**data)
        assert item.labels == []
        assert item.assignees == []

    def test_fields_omitted_defaults_to_empty(self) -> None:
        """Fields absent from response default to empty lists (sparse responses)."""
        item = WorkItemDetail(**MINIMAL_WORK_ITEM)
        assert item.labels == []
        assert item.assignees == []

    def test_name_still_required(self) -> None:
        """name remains a required field — no over-relaxation."""
        with pytest.raises(ValidationError):
            WorkItemDetail(id="abc", labels=[], assignees=[])
