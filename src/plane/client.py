"""Main API client."""

import asyncio
from typing import Optional
import httpx
from .config import Config
from .resources.users import UsersResource


class Client:
    """Main API client."""

    def __init__(self, config: Optional[Config] = None, **kwargs):
        """Initialize the client."""
        if config is None:
            config = Config.from_env(**kwargs)

        self.config = config
        self._http_client = self._create_http_client()

        # Initialize resources
        self.users = UsersResource(self)

    def _create_http_client(self) -> httpx.AsyncClient:
        """Create HTTP client with proper configuration."""
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "User-Agent": self.config.user_agent,
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

        return httpx.AsyncClient(
            headers=headers,
            timeout=self.config.timeout,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
        )

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()

    async def close(self):
        """Close the HTTP client."""
        if self._http_client:
            await self._http_client.aclose()

    async def health_check(self) -> dict:
        """Check API health."""
        try:
            response = await self._http_client.get(f"{self.config.base_url}/health")
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}


class SyncClient:
    """Synchronous wrapper for the async client."""

    def __init__(self, config: Optional[Config] = None, **kwargs):
        """Initialize the sync client."""
        self._async_client = Client(config, **kwargs)
        self._loop = None

    def _get_loop(self):
        """Get or create event loop."""
        try:
            return asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            return loop

    def _run_async(self, coro):
        """Run async function synchronously."""
        loop = self._get_loop()
        return loop.run_until_complete(coro)

    @property
    def users(self):
        """Access users resource synchronously."""
        return SyncUsersResource(self._async_client.users)

    def health_check(self) -> dict:
        """Check API health synchronously."""
        return self._run_async(self._async_client.health_check())

    def close(self):
        """Close the client."""
        self._run_async(self._async_client.close())

    def __enter__(self):
        """Sync context manager entry."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Sync context manager exit."""
        self.close()


class SyncUsersResource:
    """Synchronous wrapper for users resource."""

    def __init__(self, async_resource: UsersResource):
        self._async_resource = async_resource
        self._client = async_resource._client

    def _run_async(self, coro):
        """Run async function synchronously."""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        return loop.run_until_complete(coro)

    def list(self, page: int = 1, per_page: int = 20, search: Optional[str] = None):
        """List users synchronously."""
        return self._run_async(self._async_resource.list(page, per_page, search))

    def get(self, user_id: str):
        """Get user synchronously."""
        return self._run_async(self._async_resource.get(user_id))

    def create(self, user_data):
        """Create user synchronously."""
        return self._run_async(self._async_resource.create(user_data))

    def update(self, user_id: str, user_data):
        """Update user synchronously."""
        return self._run_async(self._async_resource.update(user_id, user_data))

    def delete(self, user_id: str):
        """Delete user synchronously."""
        return self._run_async(self._async_resource.delete(user_id))

    def search(self, query: str, limit: int = 10):
        """Search users synchronously."""
        return self._run_async(self._async_resource.search(query, limit))
