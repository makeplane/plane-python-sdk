"""Unit tests for error classes and error-detail surfacing.

These tests do NOT require network access or environment variables.
They verify that HttpError, PlaneError, ConfigurationError, and the
internal _extract_detail helper work correctly and surface API error
details in str()/repr()/tracebacks.
"""

from __future__ import annotations

import json
import traceback
from unittest.mock import MagicMock

import pytest

from plane.api.base_resource import BaseResource
from plane.config import Configuration
from plane.errors.errors import (
    ConfigurationError,
    HttpError,
    PlaneError,
    _extract_detail,
)


# ---------------------------------------------------------------------------
# _extract_detail helper
# ---------------------------------------------------------------------------
class TestExtractDetail:
    """Tests for the internal _extract_detail helper."""

    def test_none_payload(self) -> None:
        assert _extract_detail(None) is None

    def test_empty_string(self) -> None:
        assert _extract_detail("") is None

    def test_whitespace_only_string(self) -> None:
        assert _extract_detail("   \n  ") is None

    def test_plain_text_string(self) -> None:
        assert _extract_detail("Something went wrong") == "Something went wrong"

    def test_plain_text_strips_whitespace(self) -> None:
        assert _extract_detail("  oops  ") == "oops"

    def test_dict_with_detail_key(self) -> None:
        assert _extract_detail({"detail": "Not found."}) == "Not found."

    def test_dict_with_error_key(self) -> None:
        assert _extract_detail({"error": "Permission denied."}) == "Permission denied."

    def test_dict_with_message_key(self) -> None:
        assert _extract_detail({"message": "Rate limit exceeded"}) == "Rate limit exceeded"

    def test_detail_takes_priority_over_error(self) -> None:
        payload = {"detail": "Primary", "error": "Secondary"}
        assert _extract_detail(payload) == "Primary"

    def test_error_takes_priority_over_message(self) -> None:
        payload = {"error": "Primary", "message": "Secondary"}
        assert _extract_detail(payload) == "Primary"

    def test_detail_value_is_list(self) -> None:
        payload = {"detail": ["Error one", "Error two"]}
        assert _extract_detail(payload) == "Error one; Error two"

    def test_field_level_errors_single_field(self) -> None:
        payload = {"name": ["This field is required."]}
        assert _extract_detail(payload) == "name: This field is required."

    def test_field_level_errors_multiple_fields(self) -> None:
        payload = {
            "name": ["This field is required."],
            "email": ["Enter a valid email address."],
        }
        result = _extract_detail(payload)
        assert "name: This field is required." in result
        assert "email: Enter a valid email address." in result

    def test_field_level_error_string_value(self) -> None:
        payload = {"identifier": "Already exists"}
        assert _extract_detail(payload) == "identifier: Already exists"

    def test_field_level_mixed_string_and_list(self) -> None:
        payload = {
            "name": ["Required"],
            "color": "Invalid hex",
        }
        result = _extract_detail(payload)
        assert "name: Required" in result
        assert "color: Invalid hex" in result

    def test_field_level_multiple_errors_per_field(self) -> None:
        payload = {"name": ["Too short", "Must be alphanumeric"]}
        assert _extract_detail(payload) == "name: Too short, Must be alphanumeric"

    def test_empty_dict(self) -> None:
        # Empty dict → str({}) = '{}', which is non-empty but not useful.
        # Falls through to the str() fallback.
        result = _extract_detail({})
        assert result == "{}"

    def test_non_string_non_dict_payload(self) -> None:
        # e.g. a list — falls back to str()
        assert _extract_detail([1, 2, 3]) == "[1, 2, 3]"

    def test_integer_payload(self) -> None:
        assert _extract_detail(42) == "42"

    def test_dict_with_non_string_non_list_values(self) -> None:
        # Values that are neither str nor list should be skipped by field
        # parsing and fall through to str() fallback.
        payload = {"count": 5, "ok": False}
        result = _extract_detail(payload)
        assert result is not None  # falls back to str(payload)


# ---------------------------------------------------------------------------
# PlaneError
# ---------------------------------------------------------------------------
class TestPlaneError:
    """Tests for the base PlaneError class."""

    def test_message_in_str(self) -> None:
        err = PlaneError("something failed")
        assert str(err) == "something failed"

    def test_status_code_default_none(self) -> None:
        err = PlaneError("oops")
        assert err.status_code is None

    def test_status_code_set(self) -> None:
        err = PlaneError("oops", status_code=500)
        assert err.status_code == 500

    def test_inherits_exception(self) -> None:
        assert issubclass(PlaneError, Exception)

    def test_catchable_as_exception(self) -> None:
        with pytest.raises(PlaneError):
            raise PlaneError("test")


# ---------------------------------------------------------------------------
# ConfigurationError
# ---------------------------------------------------------------------------
class TestConfigurationError:
    """Tests for ConfigurationError."""

    def test_message(self) -> None:
        err = ConfigurationError("missing api_key")
        assert str(err) == "missing api_key"

    def test_status_code_is_none(self) -> None:
        err = ConfigurationError("bad config")
        assert err.status_code is None

    def test_inherits_plane_error(self) -> None:
        assert issubclass(ConfigurationError, PlaneError)

    def test_catchable_as_plane_error(self) -> None:
        with pytest.raises(PlaneError):
            raise ConfigurationError("test")


# ---------------------------------------------------------------------------
# HttpError — __str__
# ---------------------------------------------------------------------------
class TestHttpErrorStr:
    """Tests that HttpError.__str__ surfaces the response payload."""

    def test_str_with_no_response(self) -> None:
        err = HttpError("HTTP 500: Internal Server Error", 500)
        assert str(err) == "HTTP 500: Internal Server Error"

    def test_str_with_none_response(self) -> None:
        err = HttpError("HTTP 500: Internal Server Error", 500, response=None)
        assert str(err) == "HTTP 500: Internal Server Error"

    def test_str_with_detail_dict(self) -> None:
        err = HttpError("HTTP 404: Not Found", 404, {"detail": "Not found."})
        result = str(err)
        assert "HTTP 404: Not Found" in result
        assert "Not found." in result

    def test_str_with_error_dict(self) -> None:
        err = HttpError(
            "HTTP 403: Forbidden",
            403,
            {"error": "You do not have permission to perform this action."},
        )
        result = str(err)
        assert "HTTP 403: Forbidden" in result
        assert "You do not have permission to perform this action." in result

    def test_str_with_field_errors(self) -> None:
        err = HttpError(
            "HTTP 400: Bad Request",
            400,
            {"name": ["This field is required."]},
        )
        result = str(err)
        assert "HTTP 400: Bad Request" in result
        assert "name: This field is required." in result

    def test_str_with_multiple_field_errors(self) -> None:
        err = HttpError(
            "HTTP 400: Bad Request",
            400,
            {
                "name": ["This field is required."],
                "identifier": ["Must be unique."],
            },
        )
        result = str(err)
        assert "name: This field is required." in result
        assert "identifier: Must be unique." in result

    def test_str_with_plain_text_response(self) -> None:
        err = HttpError(
            "HTTP 502: Bad Gateway", 502, "<!DOCTYPE html>Server Error"
        )
        result = str(err)
        assert "HTTP 502: Bad Gateway" in result
        assert "Server Error" in result

    def test_str_no_duplicate_when_detail_matches_message(self) -> None:
        """If the detail is already in the message, don't append it again."""
        err = HttpError("HTTP 404: Not found.", 404, "Not found.")
        result = str(err)
        # Should NOT contain "Not found." twice
        assert result.count("Not found.") == 1

    def test_str_with_empty_string_response(self) -> None:
        err = HttpError("HTTP 500: Internal Server Error", 500, "")
        assert str(err) == "HTTP 500: Internal Server Error"

    def test_str_with_message_key(self) -> None:
        err = HttpError(
            "HTTP 429: Too Many Requests",
            429,
            {"message": "Rate limit exceeded. Try again in 60 seconds."},
        )
        result = str(err)
        assert "Rate limit exceeded" in result


# ---------------------------------------------------------------------------
# HttpError — __repr__
# ---------------------------------------------------------------------------
class TestHttpErrorRepr:
    """Tests that HttpError.__repr__ is informative for debugging."""

    def test_repr_contains_class_name(self) -> None:
        err = HttpError("HTTP 400: Bad Request", 400, {"name": ["required"]})
        result = repr(err)
        assert result.startswith("HttpError(")

    def test_repr_contains_message(self) -> None:
        err = HttpError("HTTP 400: Bad Request", 400, None)
        result = repr(err)
        assert "HTTP 400: Bad Request" in result

    def test_repr_contains_status_code(self) -> None:
        err = HttpError("HTTP 400: Bad Request", 400, None)
        result = repr(err)
        assert "status_code=400" in result

    def test_repr_contains_response(self) -> None:
        payload = {"detail": "oops"}
        err = HttpError("HTTP 400: Bad Request", 400, payload)
        result = repr(err)
        assert "response={'detail': 'oops'}" in result

    def test_repr_with_none_response(self) -> None:
        err = HttpError("HTTP 400: Bad Request", 400, None)
        result = repr(err)
        assert "response=None" in result


# ---------------------------------------------------------------------------
# HttpError — attributes & inheritance
# ---------------------------------------------------------------------------
class TestHttpErrorAttributes:
    """Tests for HttpError attribute access and inheritance."""

    def test_status_code_attribute(self) -> None:
        err = HttpError("msg", 422, {"detail": "Unprocessable"})
        assert err.status_code == 422

    def test_response_attribute(self) -> None:
        payload = {"name": ["required"]}
        err = HttpError("msg", 400, payload)
        assert err.response == payload

    def test_response_attribute_none_default(self) -> None:
        err = HttpError("msg", 400)
        assert err.response is None

    def test_inherits_plane_error(self) -> None:
        assert issubclass(HttpError, PlaneError)

    def test_catchable_as_plane_error(self) -> None:
        with pytest.raises(PlaneError):
            raise HttpError("msg", 400, None)

    def test_catchable_as_exception(self) -> None:
        with pytest.raises(HttpError):
            raise HttpError("msg", 400, None)

    def test_args_tuple(self) -> None:
        err = HttpError("HTTP 400: Bad Request", 400, None)
        assert err.args == ("HTTP 400: Bad Request",)


# ---------------------------------------------------------------------------
# HttpError in tracebacks
# ---------------------------------------------------------------------------
class TestHttpErrorTraceback:
    """Ensure error details are visible in unhandled-exception tracebacks."""

    def test_traceback_contains_response_detail(self) -> None:
        try:
            raise HttpError(
                "HTTP 400: Bad Request",
                400,
                {"name": ["This field is required."]},
            )
        except HttpError:
            tb = traceback.format_exc()

        assert "HTTP 400: Bad Request" in tb
        assert "name: This field is required." in tb

    def test_traceback_contains_detail_key(self) -> None:
        try:
            raise HttpError("HTTP 404: Not Found", 404, {"detail": "Not found."})
        except HttpError:
            tb = traceback.format_exc()

        assert "Not found." in tb

    def test_traceback_with_plain_text(self) -> None:
        try:
            raise HttpError("HTTP 502: Bad Gateway", 502, "upstream error")
        except HttpError:
            tb = traceback.format_exc()

        assert "upstream error" in tb


# ---------------------------------------------------------------------------
# Integration with BaseResource._handle_response
# ---------------------------------------------------------------------------
class TestHandleResponseIntegration:
    """Test that _handle_response raises HttpError with the full payload."""

    @pytest.fixture
    def resource(self) -> BaseResource:
        config = Configuration(
            base_path="https://api.plane.so",
            api_key="test-key",
        )
        return BaseResource(config, "/test")

    def _make_mock_response(
        self,
        status_code: int,
        reason: str,
        json_body: dict | None = None,
        text_body: str = "",
        content_type: str = "application/json",
    ) -> MagicMock:
        resp = MagicMock()
        resp.status_code = status_code
        resp.reason = reason
        resp.content = json.dumps(json_body).encode() if json_body else text_body.encode()
        resp.text = text_body or (json.dumps(json_body) if json_body else "")
        resp.headers = {"content-type": content_type}
        if json_body is not None:
            resp.json.return_value = json_body
        else:
            resp.json.side_effect = ValueError("No JSON")
        return resp

    def test_400_field_errors_surfaced(self, resource: BaseResource) -> None:
        """A 400 with field errors should include them in str(e)."""
        mock_resp = self._make_mock_response(
            400,
            "Bad Request",
            json_body={"name": ["This field is required."]},
        )
        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        assert err.status_code == 400
        assert err.response == {"name": ["This field is required."]}
        assert "name: This field is required." in str(err)

    def test_403_error_key_surfaced(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(
            403,
            "Forbidden",
            json_body={"error": "You do not have permission."},
        )
        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        assert err.status_code == 403
        assert "You do not have permission." in str(err)

    def test_404_detail_key_surfaced(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(
            404,
            "Not Found",
            json_body={"detail": "Not found."},
        )
        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        assert err.status_code == 404
        assert "Not found." in str(err)

    def test_422_multiple_field_errors(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(
            422,
            "Unprocessable Entity",
            json_body={
                "name": ["Too short", "Must be alphanumeric"],
                "color": ["Invalid hex color"],
            },
        )
        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        result = str(err)
        assert "name: Too short, Must be alphanumeric" in result
        assert "color: Invalid hex color" in result

    def test_500_plain_text_fallback(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(
            500,
            "Internal Server Error",
            text_body="Something broke",
            content_type="text/html",
        )
        # json() will raise
        mock_resp.json.side_effect = ValueError("No JSON")

        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        assert err.status_code == 500
        assert err.response == "Something broke"
        assert "Something broke" in str(err)

    def test_204_returns_none(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(204, "No Content")
        mock_resp.status_code = 204
        result = resource._handle_response(mock_resp)
        assert result is None

    def test_200_json_returns_body(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(
            200,
            "OK",
            json_body={"id": "abc123", "name": "Test"},
        )
        result = resource._handle_response(mock_resp)
        assert result == {"id": "abc123", "name": "Test"}

    def test_429_message_key_surfaced(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(
            429,
            "Too Many Requests",
            json_body={"message": "Rate limit exceeded"},
        )
        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        assert err.status_code == 429
        assert "Rate limit exceeded" in str(err)

    def test_401_unauthorized(self, resource: BaseResource) -> None:
        mock_resp = self._make_mock_response(
            401,
            "Unauthorized",
            json_body={"detail": "Authentication credentials were not provided."},
        )
        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        assert err.status_code == 401
        assert "Authentication credentials were not provided." in str(err)

    def test_response_attribute_is_full_payload(self, resource: BaseResource) -> None:
        """The .response attribute should be the full dict for programmatic use."""
        payload = {"detail": "Not found.", "extra_info": "some-uuid"}
        mock_resp = self._make_mock_response(404, "Not Found", json_body=payload)
        with pytest.raises(HttpError) as exc_info:
            resource._handle_response(mock_resp)

        err = exc_info.value
        assert err.response == payload
        assert err.response["extra_info"] == "some-uuid"


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
class TestHttpErrorEdgeCases:
    """Edge cases and backward compatibility."""

    def test_response_none_str_unchanged(self) -> None:
        """When response is None, str() should be the raw message only."""
        err = HttpError("HTTP 500: Internal Server Error", 500, None)
        assert str(err) == "HTTP 500: Internal Server Error"

    def test_response_empty_dict_str(self) -> None:
        err = HttpError("HTTP 400: Bad Request", 400, {})
        result = str(err)
        # Should include fallback str({}) = '{}'
        assert "HTTP 400: Bad Request" in result

    def test_response_list_payload(self) -> None:
        """Some endpoints may return a list of errors."""
        err = HttpError("HTTP 400: Bad Request", 400, ["Error 1", "Error 2"])
        result = str(err)
        assert "Error 1" in result

    def test_error_can_be_pickled(self) -> None:
        """Exceptions should be picklable for multiprocessing/logging."""
        import pickle

        err = HttpError("HTTP 400: Bad Request", 400, {"detail": "oops"})
        roundtripped = pickle.loads(pickle.dumps(err))
        assert str(roundtripped) == str(err)
        assert roundtripped.status_code == err.status_code
        assert roundtripped.response == err.response

    def test_error_in_except_clause_print(self) -> None:
        """Simulate a typical user error-handling pattern."""
        try:
            raise HttpError(
                "HTTP 400: Bad Request",
                400,
                {"name": ["This field is required."], "color": ["Invalid hex"]},
            )
        except HttpError as e:
            msg = f"Failed: {e}"

        assert "name: This field is required." in msg
        assert "color: Invalid hex" in msg

    def test_error_in_format_string(self) -> None:
        """Ensure str formatting works cleanly."""
        err = HttpError("HTTP 404: Not Found", 404, {"detail": "Not found."})
        assert "Not found." in f"Error: {err}"
        # Also verify str() works directly (used by logging, etc.)
        assert "Not found." in f"Error: {str(err)}"
