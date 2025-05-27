"""Users resource."""

from typing import List, Optional, Dict, Any
from .base import BaseResource
from ..models.user import User, UserCreate, UserUpdate
from ..models.base import PaginatedResponse


class UsersResource(BaseResource[User]):
    """Resource for managing users."""

    async def list(
        self, page: int = 1, per_page: int = 20, search: Optional[str] = None
    ) -> Dict[str, Any]:
        """List users with pagination."""
        params = {
            "page": page,
            "per_page": per_page,
        }
        if search:
            params["search"] = search

        response = await self._request("GET", "users", params=params)

        # Parse users
        users_data = response.get("data", [])
        users = [User.from_dict(user_data) for user_data in users_data]

        # Parse pagination
        pagination = PaginatedResponse.from_dict(response.get("pagination", {}))

        return {"users": users, "pagination": pagination}

    async def get(self, user_id: str) -> User:
        """Get a user by ID."""
        response = await self._request("GET", f"users/{user_id}")
        return User.from_dict(response)

    async def create(self, user_data: UserCreate) -> User:
        """Create a new user."""
        response = await self._request("POST", "users", data=user_data.to_dict())
        return User.from_dict(response)

    async def update(self, user_id: str, user_data: UserUpdate) -> User:
        """Update a user."""
        response = await self._request(
            "PATCH", f"users/{user_id}", data=user_data.to_dict()
        )
        return User.from_dict(response)

    async def delete(self, user_id: str) -> bool:
        """Delete a user."""
        await self._request("DELETE", f"users/{user_id}")
        return True

    async def search(self, query: str, limit: int = 10) -> List[User]:
        """Search users."""
        params = {"q": query, "limit": limit}
        response = await self._request("GET", "users/search", params=params)

        users_data = response.get("users", [])
        return [User.from_dict(user_data) for user_data in users_data]
