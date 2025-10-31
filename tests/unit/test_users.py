"""Unit tests for Users API resource (smoke tests with real HTTP requests)."""

from plane.client import PlaneClient


class TestUsersAPI:
    """Test Users API resource."""

    def test_get_me(self, client: PlaneClient) -> None:
        """Test getting current user information."""
        user = client.users.get_me()
        assert user is not None
        assert hasattr(user, "id")
        assert hasattr(user, "display_name")
        assert hasattr(user, "email")
