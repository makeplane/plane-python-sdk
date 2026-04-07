"""Tests for WorkItemDetail parsing with sparse API responses (MFT-34).

When the Plane API is called with a ``fields`` parameter, it returns only the
requested fields.  ``assignees`` and ``labels`` may be absent.  These tests
verify that ``WorkItemDetail`` handles both full and sparse payloads without
raising a ``ValidationError``.
"""

import pytest
from pydantic import ValidationError

from plane.models.work_items import WorkItemDetail


# -- Fixtures ----------------------------------------------------------------

FULL_RESPONSE = {
    "id": "abc-123",
    "name": "Test item",
    "assignees": [
        {
            "id": "user-1",
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com",
            "display_name": "alice",
        }
    ],
    "labels": [
        {
            "id": "label-1",
            "name": "Bug",
            "color": "#FF0000",
        }
    ],
    "priority": "high",
    "state": "state-uuid",
    "project": "proj-uuid",
    "workspace": "ws-uuid",
}

SPARSE_RESPONSE_NO_ASSIGNEES_LABELS = {
    "id": "abc-123",
    "name": "Test item",
    "state": "state-uuid",
}

SPARSE_RESPONSE_ID_AND_NAME_ONLY = {
    "id": "abc-123",
    "name": "Test item",
}


# -- Tests -------------------------------------------------------------------


class TestWorkItemDetailSparseResponse:
    """Regression tests for MFT-34: fields parameter causes ValidationError."""

    def test_full_response_parses(self):
        """Full API response (with assignees + labels) still works."""
        item = WorkItemDetail.model_validate(FULL_RESPONSE)
        assert item.id == "abc-123"
        assert len(item.assignees) == 1
        assert item.assignees[0].id == "user-1"
        assert len(item.labels) == 1
        assert item.labels[0].name == "Bug"

    def test_sparse_response_without_assignees_and_labels(self):
        """Sparse response (fields=id,name,state) must not raise ValidationError."""
        item = WorkItemDetail.model_validate(SPARSE_RESPONSE_NO_ASSIGNEES_LABELS)
        assert item.id == "abc-123"
        assert item.name == "Test item"
        assert item.assignees == []
        assert item.labels == []

    def test_sparse_response_id_and_name_only(self):
        """Minimal sparse response (fields=id,name) must not raise."""
        item = WorkItemDetail.model_validate(SPARSE_RESPONSE_ID_AND_NAME_ONLY)
        assert item.id == "abc-123"
        assert item.assignees == []
        assert item.labels == []

    def test_empty_assignees_and_labels_accepted(self):
        """Explicit empty lists are accepted (normal case with no assignees)."""
        data = {**FULL_RESPONSE, "assignees": [], "labels": []}
        item = WorkItemDetail.model_validate(data)
        assert item.assignees == []
        assert item.labels == []

    def test_name_still_required(self):
        """``name`` is still required — sparse responses always include it."""
        with pytest.raises(ValidationError):
            WorkItemDetail.model_validate({"id": "abc-123"})
