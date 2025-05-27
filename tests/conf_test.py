import pytest
import httpx
from unittest.mock import AsyncMock
from plane import Client, Config


@pytest.fixture
def config():
    """Test configuration."""
    return Config(api_key="x-api-key", base_url="https://api.plane.so/api/v1")


@pytest.fixture
def mock_http_client():
    """Mock HTTP client."""
    return AsyncMock(spec=httpx.AsyncClient)


@pytest.fixture
async def client(config, mock_http_client):
    """Test client."""
    client = Client(config)
    client._http_client = mock_http_client
    yield client
    await client.close()


@pytest.fixture
def sample_user_data():
    """Sample user data for testing."""
    return {
        "id": "123",
        "email": "test@example.com",
        "firstName": "John",
        "lastName": "Doe",
        "username": "johndoe",
        "isActive": True,
        "createdAt": "2023-01-01T00:00:00Z",
        "updatedAt": "2023-01-01T00:00:00Z",
    }
