from collections.abc import Sequence
from typing import get_origin

from plane.api.v2._generated.constants import (
    BULK_MAX_ITEMS,
    ERROR_CODES,
    FIELDS,
    ORDER_BY,
    WorkItemPropertiesListFilters,
    WorkItemsListFilters,
)


def test_state_list_fields_match_the_api() -> None:
    assert "name" in FIELDS["states_list"]
    assert "group" in FIELDS["states_list"]
    assert "all" in FIELDS["states_list"]


def test_label_list_fields_include_parent_id() -> None:
    assert "parent_id" in FIELDS["labels_list"]


def test_order_by_is_bounded() -> None:
    assert "-created_at" in ORDER_BY["states_list"]
    assert "name" not in ORDER_BY["states_list"]


def test_batch_cap() -> None:
    assert BULK_MAX_ITEMS == 50


def test_error_codes_are_populated() -> None:
    assert len(ERROR_CODES) > 0
    assert "not_found" in ERROR_CODES
    assert "invalid_request" in ERROR_CODES


def test_work_item_properties_filters_include_display_name() -> None:
    """Regression pin against a stale golden: `display_name` shipped on the property list
    operations and must survive every regeneration -- reads the real, imported module rather
    than the generated file's text, so this runs in the default test suite."""
    assert "display_name" in WorkItemPropertiesListFilters.__annotations__
    assert WorkItemPropertiesListFilters.__annotations__["display_name"] is str


def test_work_items_in_filter_is_a_sequence_not_a_str() -> None:
    """Regression pin: `array`-typed query parameters (the golden's `__in` filters) must be
    typed as a `Sequence`, not silently fall through to `str`."""
    annotation = WorkItemsListFilters.__annotations__["assignee_id__in"]
    assert get_origin(annotation) is Sequence, (
        f"assignee_id__in is {annotation!r}, expected a Sequence[...] -- array-typed query "
        "parameters must not be typed as plain str."
    )
