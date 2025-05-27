import pytest
from unittest.mock import MagicMock
import httpx
from plane.models.user import User, UserCreate, UserUpdate
from plane.exceptions import NotFoundError


class TestUsersResource:
    """Test users resource."""

    @pytest.mark.asyncio
    async def test_list_users(self, client, mock_http_client, sample_user_data):
        """Test listing users."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {
            "data": [sample_user_data],
            "pagination": {
                "page": 1,
                "perPage": 20,
                "total": 1,
                "totalPages": 1,
                "hasNext": False,
                "hasPrev": False,
            },
        }
        mock_http_client.request.return_value = mock_response

        result = await client.users.list()

        assert len(result["users"]) == 1
        assert isinstance(result["users"][0], User)
        assert result["users"][0].email == "test@example.com"
        assert result["pagination"].total == 1

    @pytest.mark.asyncio
    async def test_get_user(self, client, mock_http_client, sample_user_data):
        """Test getting a user."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = sample_user_data
        mock_http_client.request.return_value = mock_response

        user = await client.users.get("123")

        assert isinstance(user, User)
        assert user.id == "123"
        assert user.email == "test@example.com"
        assert user.full_name == "John Doe"

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, client, mock_http_client):
        """Test getting a non-existent user."""
        mock_response = MagicMock()
        mock_response.is_success = False
        mock_response.status_code = 404
        mock_response.json.return_value = {"message": "User not found"}
        mock_http_client.request.return_value = mock_response

        with pytest.raises(NotFoundError):
            await client.users.get("999")

    @pytest.mark.asyncio
    async def test_create_user(self, client, mock_http_client, sample_user_data):
        """Test creating a user."""
        user_create = UserCreate(
            email="new@example.com",
            firstName="Jane",
            lastName="Smith",
            password="password123",
        )

        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {
            **sample_user_data,
            "email": "new@example.com",
            "firstName": "Jane",
            "lastName": "Smith",
        }
        mock_http_client.request.return_value = mock_response

        user = await client.users.create(user_create)

        assert isinstance(user, User)
        assert user.email == "new@example.com"
        assert user.first_name == "Jane"

    @pytest.mark.asyncio
    async def test_update_user(self, client, mock_http_client, sample_user_data):
        """Test updating a user."""
        user_update = UserUpdate(firstName="Updated")

        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {**sample_user_data, "firstName": "Updated"}
        mock_http_client.request.return_value = mock_response

        user = await client.users.update("123", user_update)

        assert isinstance(user, User)
        assert user.first_name == "Updated"

    @pytest.mark.asyncio
    async def test_delete_user(self, client, mock_http_client):
        """Test deleting a user."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {}
        mock_http_client.request.return_value = mock_response

        result = await client.users.delete("123")

        assert result is True

    @pytest.mark.asyncio
    async def test_search_users(self, client, mock_http_client, sample_user_data):
        """Test searching users."""
        mock_response = MagicMock()
        mock_response.is_success = True
        mock_response.json.return_value = {"users": [sample_user_data]}
        mock_http_client.request.return_value = mock_response

        users = await client.users.search("john", limit=5)

        assert len(users) == 1
        assert isinstance(users[0], User)
        assert users[0].first_name == "John"
