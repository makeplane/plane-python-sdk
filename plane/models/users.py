from pydantic import BaseModel, ConfigDict, Field

from .enums import EntityTypeEnum, TypeMimeEnum
from .pagination import PaginatedResponse


class UserLite(BaseModel):
    """Lite user information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    avatar: str | None = None
    avatar_url: str | None = Field(None, description="Avatar URL")
    display_name: str | None = None


class PaginatedUserLiteResponse(PaginatedResponse):
    """Paginated response for user lite."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[UserLite]


class UserAssetUploadRequest(BaseModel):
    """Request model for uploading user assets."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str = Field(..., description="Original filename of the asset")
    type: TypeMimeEnum | None = Field(
        None,
        description="MIME type of the file",
    )
    size: int = Field(..., description="File size in bytes")
    entity_type: EntityTypeEnum = Field(
        ...,
        description="Type of user asset",
    )
