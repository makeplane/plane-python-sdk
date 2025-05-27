from typing import Optional
from pydantic import Field, EmailStr
from .base import BaseAPIModel, TimestampMixin


class User(BaseAPIModel, TimestampMixin):
    """User model."""

    id: str
    email: EmailStr
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    username: Optional[str] = None
    is_active: bool = Field(default=True, alias="isActive")
    avatar_url: Optional[str] = Field(None, alias="avatarUrl")

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"


class UserCreate(BaseAPIModel):
    """Model for creating a user."""

    email: EmailStr
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    username: Optional[str] = None
    password: str = Field(min_length=8)


class UserUpdate(BaseAPIModel):
    """Model for updating a user."""

    first_name: Optional[str] = Field(None, alias="firstName")
    last_name: Optional[str] = Field(None, alias="lastName")
    username: Optional[str] = None
    avatar_url: Optional[str] = Field(None, alias="avatarUrl")
