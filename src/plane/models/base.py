"""Base model classes."""

from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class BaseAPIModel(BaseModel):
    """Base model for all API response models."""

    model_config = ConfigDict(
        str_strip_whitespace=True,
        validate_assignment=True,
        extra="forbid",
        populate_by_name=True,
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary."""
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BaseAPIModel":
        """Create model from dictionary."""
        return cls(**data)


class TimestampMixin(BaseModel):
    """Mixin for models with timestamp fields."""

    created_at: Optional[datetime] = Field(None, alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")


class PaginatedResponse(BaseAPIModel):
    """Model for paginated API responses."""

    page: int = 1
    per_page: int = Field(default=20, alias="perPage")
    total: int
    total_pages: int = Field(alias="totalPages")
    has_next: bool = Field(alias="hasNext")
    has_prev: bool = Field(alias="hasPrev")
