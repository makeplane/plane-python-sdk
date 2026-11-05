from collections.abc import Iterable
from dataclasses import dataclass

from .errors import ConfigurationError


@dataclass(frozen=True)
class RetryConfig:
    total: int = 3
    backoff_factor: float = 0.3
    status_forcelist: Iterable[int] = (429, 500, 502, 503, 504)
    allowed_methods: frozenset[str] = frozenset(
        {"GET", "PUT", "DELETE", "HEAD", "OPTIONS", "PATCH"}
    )


class Configuration:
    def __init__(
        self,
        *,
        base_path: str,
        api_key: str | None = None,
        access_token: str | None = None,
        timeout: float | tuple[float, float] | None = 30.0,
        retry: RetryConfig | None = None,
        verify: bool | str = True,
    ) -> None:
        if not api_key and not access_token:
            raise ConfigurationError(
                "Either 'api_key' or 'access_token' must be provided for authentication"
            )
        if api_key and access_token:
            raise ConfigurationError(
                "Only one of 'api_key' or 'access_token' should be provided, not both"
            )

        self.base_path = base_path.rstrip("/") + "/api/v1"
        # Raw origin with no version suffix. v1 keeps `base_path`; v2 resources
        # build their own `/api/v2` prefix from this.
        self.api_root = base_path.rstrip("/")
        self.api_key = api_key
        self.access_token = access_token
        self.timeout = timeout
        self.retry = retry
        self.verify = verify
