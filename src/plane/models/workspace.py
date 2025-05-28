from typing import Optional
from pydantic import Field
from .base import BaseAPIModel, TimestampMixin


class Workspace(BaseAPIModel, TimestampMixin):
    """Workspace model."""

    id: str
    name: str
    logo: Optional[str] = None
    logo_asset: Optional[str] = None
    owner: str
    slug: str
    organization_size: Optional[str] = None
    timezone: str = Field(default="UTC")


class WorkspaceUpdate(BaseAPIModel):
    """Model for creating a workspace."""

    name: str
    logo: Optional[str] = None
    logo_asset: Optional[str] = None
    organization_size: Optional[str] = None
    timezone: str = Field(default="UTC")
