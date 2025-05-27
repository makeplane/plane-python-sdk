"""Configuration management for the API SDK."""

import os
from typing import Optional
from dataclasses import dataclass


@dataclass
class Config:
    """Configuration class for the API client."""

    api_key: str
    base_url: str = "https://api.plane.so/api/v1"
    timeout: int = 30
    max_retries: int = 3
    retry_delay: float = 1.0
    user_agent: Optional[str] = None

    def __post_init__(self):
        """Validate configuration after initialization."""
        if not self.api_key:
            raise ValueError("API key is required")

        if not self.user_agent:
            self.user_agent = f"plane-sdk/1.0.0"

    @classmethod
    def from_env(cls, **kwargs) -> "Config":
        """Create configuration from environment variables."""
        api_key = os.getenv("PLANE_API_KEY")
        if not api_key:
            raise ValueError("PLANE_API_KEY environment variable is required")

        base_url = os.getenv("MY_API_BASE_URL", "https://api.example.com/v1")
        timeout = int(os.getenv("MY_API_TIMEOUT", "30"))
        max_retries = int(os.getenv("MY_API_MAX_RETRIES", "3"))

        return cls(
            api_key=api_key,
            base_url=base_url,
            timeout=timeout,
            max_retries=max_retries,
            **kwargs,
        )
