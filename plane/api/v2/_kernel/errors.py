"""RFC 9457 problem+json errors for api_v2."""

from typing import Any

from pydantic import BaseModel, ConfigDict, ValidationError

from ....errors import PlaneError


class FieldError(BaseModel):
    """One entry of a ValidationProblemDetail `errors` array."""

    model_config = ConfigDict(extra="allow")

    field: str
    message: str


class PlaneAPIError(PlaneError):
    """A non-2xx api_v2 response, parsed from `application/problem+json`.

    `code` is an open vocabulary; compare it as a plain string, not an enum."""

    def __init__(
        self,
        *,
        status: int,
        type: str,
        code: str,
        detail: str,
        title: str | None = None,
        errors: list[FieldError] | None = None,
        response: Any = None,
    ) -> None:
        super().__init__(f"HTTP {status} {code}: {detail}", status_code=status)
        self.status = status
        self.type = type
        self.code = code
        self.detail = detail
        self.title = title
        self.errors = errors
        self.response = response

    @classmethod
    def from_payload(cls, status: int, payload: Any) -> "PlaneAPIError":
        """Build from a parsed body; tolerates a non-problem body (proxy/gateway)."""
        if not isinstance(payload, dict):
            return cls(
                status=status,
                type="server_error",
                code="server_error",
                detail=str(payload) if payload else "Request failed.",
                response=payload,
            )
        raw_errors = payload.get("errors")
        errors: list[FieldError] | None = None
        if isinstance(raw_errors, list):
            parsed: list[FieldError] = []
            for item in raw_errors:
                try:
                    parsed.append(FieldError.model_validate(item))
                except ValidationError:
                    # A malformed `errors` entry must not lose the real HTTP status
                    # (e.g. a proxy/gateway echoing a plain string instead of the
                    # `{field, message}` shape) -- drop it and keep going.
                    continue
            errors = parsed or None
        return cls(
            status=payload.get("status", status),
            type=payload.get("type", "server_error"),
            code=payload.get("code", "server_error"),
            detail=payload.get("detail", "Request failed."),
            title=payload.get("title"),
            errors=errors,
            response=payload,
        )


class NoMatchFound(PlaneError):
    """An identity lookup (`find_by_name`) matched nothing."""


class MultipleMatchesFound(PlaneError):
    """An identity lookup matched more than one row."""


class MissingPathId(PlaneError):
    """A resource method was called without one of the path ids its URL needs.

    Raised instead of the bare `KeyError` that `str.format_map` would otherwise
    produce, which named the template key and nothing else."""


class FieldNotRequested(AttributeError):
    """Raised when reading a field that the request's `fields=` excluded."""
