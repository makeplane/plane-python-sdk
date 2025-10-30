from typing import Any

from ..models.users import UserAssetUploadRequest, UserLite
from .base_resource import BaseResource


class Users(BaseResource):
    def __init__(self, config: Any) -> None:
        super().__init__(config, "/users/")

    def upload_asset(self, data: UserAssetUploadRequest) -> dict[str, Any]:
        """Upload a user asset (avatar or cover)."""
        return self._post("assets/", data.model_dump(exclude_none=True))

    def get_me(self) -> UserLite:
        """Get current user information."""
        response = self._get("me")
        return UserLite.model_validate(response)
