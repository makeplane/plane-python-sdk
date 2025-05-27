import pytest
from unittest.mock import AsyncMock, MagicMock
import httpx
from plane import Client, Config
from plane.exceptions import AuthenticationError


class TestClient:
    """Test the main client."""

    def test_client_initialization(self):
        """Test client initialization."""
        config = Config(api_key="test-key")
        client = Client(config)

        assert client.config == config
        assert client.users is not None
        assert isinstance(client._http_client, httpx.AsyncClient)

    def test_client_from_env(self, monkeypatch):
        """Test client initialization from environment."""
        monkeypatch.setenv("MY_API_KEY", "env-test-key")
        monkeypatch.setenv("MY_API_BASE_URL", "https://env.api.com")

        client = Client()

        assert client.config.api_key == "env-test-key"
        assert client.config.base_url == "https://env.api.com"

    @pytest.mark.asyncio
    async def test_health_check_success(self, client, mock_http_client):
        """Test successful health check."""
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_http_client.get.return_value = mock_response

        result = await client.health_check()

        assert result == {"status": "ok"}
        mock_http_client.get.assert_called_once_with(f"{client.config.base_url}/health")

    @pytest.mark.asyncio
    async def test_health_check_error(self, client, mock_http_client):
        """Test health check with error."""
        mock_http_client.get.side_effect = Exception("Connection failed")

        result = await client.health_check()

        assert result["status"] == "error"
        assert "Connection failed" in result["message"]

    @pytest.mark.asyncio
    async def test_context_manager(self, config):
        """Test client as async context manager."""
        async with Client(config) as client:
            assert client is not None
            assert client._http_client is not None

        # Client should be closed after context
        assert client._http_client.is_closed
