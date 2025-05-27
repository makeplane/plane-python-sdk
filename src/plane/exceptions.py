"""Custom exceptions for the Plane SDK."""

from typing import Optional, Dict, Any


class PlaneError(Exception):
    """Base exception for all API errors."""

    def __init__(
        self,
        message: str,
        status_code: Optional[int] = None,
        response_data: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.response_data = response_data or {}

    def __str__(self) -> str:
        if self.status_code:
            return f"[{self.status_code}] {self.message}"
        return self.message


class AuthenticationError(PlaneError):
    """Raised when authentication fails (401)."""

    pass


class AuthorizationError(PlaneError):
    """Raised when authorization fails (403)."""

    pass


class NotFoundError(PlaneError):
    """Raised when a resource is not found (404)."""

    pass


class ValidationError(PlaneError):
    """Raised when request validation fails (422)."""

    pass


class RateLimitError(PlaneError):
    """Raised when rate limit is exceeded (429)."""

    def __init__(self, message: str, retry_after: Optional[int] = None, **kwargs):
        super().__init__(message, **kwargs)
        self.retry_after = retry_after


class ServerError(PlaneError):
    """Raised when server errors occur (5xx)."""

    pass


class TimeoutError(PlaneError):
    """Raised when request times out."""

    pass


class ConnectionError(PlaneError):
    """Raised when connection fails."""

    pass
