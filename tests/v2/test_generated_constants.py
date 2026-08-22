from plane.api.v2._generated.constants import BULK_MAX_ITEMS, ERROR_CODES, FIELDS, ORDER_BY


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
