class PlaneError(Exception):
    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class ConfigurationError(PlaneError):
    """Raised when client configuration is invalid or incomplete."""

    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=None)


class HttpError(PlaneError):
    def __init__(self, message: str, status_code: int, response: object | None = None) -> None:
        super().__init__(message, status_code=status_code)
        self.response = response
