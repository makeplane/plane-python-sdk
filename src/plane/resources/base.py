"""Base resource class."""

from typing import Any, Dict, Optional, Type, TypeVar, Generic, List
import httpx
from ..exceptions import (
    PlaneError,
    AuthenticationError,
    AuthorizationError,
    NotFoundError,
    ValidationError,
    RateLimitError,
    ServerError,
    TimeoutError,
    ConnectionError,
)
from ..models.base import BaseAPIModel

T = TypeVar("T", bound=BaseAPIModel)


class BaseResource(Generic[T]):
    """Base class for API resources."""

    def __init__(self, client: "Client"):
        self._client = client
        self._http_client = client._http_client

    def _handle_response(self, response: httpx.Response) -> Dict[str, Any]:
        """Handle HTTP response and raise appropriate exceptions."""
        try:
            data = response.json()
        except Exception:
            data = {"message": response.text}

        if response.is_success:
            return data

        message = data.get("message", f"HTTP {response.status_code}")

        if response.status_code == 401:
            raise AuthenticationError(message, response.status_code, data)
        elif response.status_code == 403:
            raise AuthorizationError(message, response.status_code, data)
        elif response.status_code == 404:
            raise NotFoundError(message, response.status_code, data)
        elif response.status_code == 422:
            raise ValidationError(message, response.status_code, data)
        elif response.status_code == 429:
            retry_after = response.headers.get("Retry-After")
            retry_after_int = int(retry_after) if retry_after else None
            raise RateLimitError(message, retry_after_int, response.status_code, data)
        elif response.status_code >= 500:
            raise ServerError(message, response.status_code, data)
        else:
            raise PlaneError(message, response.status_code, data)

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Make HTTP request."""
        url = f"{self._client.config.base_url.rstrip('/')}/{endpoint.lstrip('/')}"

        try:
            response = await self._http_client.request(
                method=method, url=url, json=data, params=params, **kwargs
            )
            return self._handle_response(response)
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Request timed out: {str(e)}")
        except httpx.ConnectError as e:
            raise ConnectionError(f"Connection failed: {str(e)}")
        except httpx.HTTPError as e:
            raise PlaneError(f"HTTP error: {str(e)}")
