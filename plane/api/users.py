from collections.abc import Mapping
from typing import Any

from ..models.users import UserAssetUploadRequest, UserLite
from .base_resource import BaseResource


class Users(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/users/")

    def retrieve(self, user_id: str) -> UserLite:
        """Retrieve a user by ID."""
        response = self._get(f"{user_id}/")
        return UserLite.model_validate(response)

    def list(self, params: Mapping[str, Any] | None = None) -> list[UserLite]:
        """List users with optional filtering parameters."""
        response = self._get("", params=params)
        return [UserLite.model_validate(item) for item in response]

    def upload_asset(self, data: UserAssetUploadRequest) -> dict[str, Any]:
        """Upload a user asset (avatar or cover)."""
        return self._post("assets/", data.model_dump(exclude_none=True))

    def get_me(self) -> UserLite:
        """Get current user information."""
        response = self._get("me/")
        return UserLite.model_validate(response)
