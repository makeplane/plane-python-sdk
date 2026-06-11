class PlaneError(Exception):
    """Base exception for all Plane SDK errors."""

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code

    def __reduce__(self) -> tuple:
        return (type(self), (str(self), self.status_code))


class ConfigurationError(PlaneError):
    """Raised when client configuration is invalid or incomplete."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=None)


def _extract_detail(payload: object) -> str | None:
    """Extract a human-readable detail string from an API error payload.

    Plane API endpoints return errors in several shapes:
      - ``{"detail": "Not found."}``
      - ``{"error": "Permission denied."}``
      - ``{"name": ["This field is required."]}``  (field-level errors)
      - ``{"field": "single error string"}``
      - plain text strings

    This helper normalises all of those into a single string suitable for
    inclusion in an exception message.  Returns ``None`` when nothing useful
    can be extracted.
    """
    if payload is None:
        return None

    if isinstance(payload, str):
        stripped = payload.strip()
        return stripped if stripped else None

    if isinstance(payload, dict):
        # Prefer the canonical "detail" / "error" keys first.
        for key in ("detail", "error", "message"):
            value = payload.get(key)
            if value is not None:
                if isinstance(value, list):
                    return "; ".join(str(v) for v in value)
                return str(value)

        # Field-level validation errors, e.g. {"name": ["required"]}
        parts: list[str] = []
        for field, errors in payload.items():
            if isinstance(errors, list):
                joined = ", ".join(str(e) for e in errors)
                parts.append(f"{field}: {joined}")
            elif isinstance(errors, str):
                parts.append(f"{field}: {errors}")
        if parts:
            return "; ".join(parts)

    # For any other type, fall back to str()
    text = str(payload).strip()
    return text if text else None


class HttpError(PlaneError):
    """Raised on non-2xx HTTP responses.

    Attributes:
        status_code: The HTTP status code.
        response: The parsed response body (dict / str / None).  Use this for
            programmatic inspection of field-level errors.
    """

    def __init__(
        self, message: str, status_code: int, response: object | None = None
    ) -> None:
        super().__init__(message, status_code=status_code)
        self.response = response

    def __reduce__(self) -> tuple:
        return (
            type(self),
            (super().__str__(), self.status_code, self.response),
        )

    def __str__(self) -> str:
        base = super().__str__()
        detail = _extract_detail(self.response)
        if detail and detail not in base:
            return f"{base}: {detail}"
        return base

    def __repr__(self) -> str:
        return (
            f"{type(self).__name__}(message={super().__str__()!r}, "
            f"status_code={self.status_code!r}, response={self.response!r})"
        )
