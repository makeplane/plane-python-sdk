from plane.api.v2 import PlaneAPIError


def test_from_payload_tolerates_malformed_errors_entries() -> None:
    """`from_payload` must drop a malformed `errors` entry rather than raising, keeping well-formed
    entries and the real HTTP status."""
    error = PlaneAPIError.from_payload(
        400,
        {
            "type": "invalid_request",
            "code": "invalid_request",
            "detail": "bad request",
            "errors": ["oops", {"field": "name", "message": "required"}],
        },
    )

    assert error.status == 400
    assert error.code == "invalid_request"
    assert error.errors is not None
    assert len(error.errors) == 1
    assert error.errors[0].field == "name"


def test_from_payload_all_errors_entries_malformed_leaves_errors_none() -> None:
    error = PlaneAPIError.from_payload(
        400,
        {
            "type": "invalid_request",
            "code": "invalid_request",
            "detail": "bad request",
            "errors": ["oops", "still not a field error"],
        },
    )

    assert error.status == 400
    assert error.errors is None


def test_from_payload_non_dict_body_still_carries_status() -> None:
    error = PlaneAPIError.from_payload(502, "Bad Gateway")

    assert error.status == 502
    assert error.code == "server_error"
