"""Workspace invitation models for api_v2; read-only + create + bulk-create only -- no PATCH
(invites are accepted or deleted, never edited)."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class WorkspaceInvite(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    email: str | None = None
    accepted: bool | None = None
    message: str | None = None
    role: str | None = None
    responded_at: datetime | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateWorkspaceInvite(BaseModel):
    """POST body. `email` is required; `role` defaults to `"member"` server-side."""

    model_config = ConfigDict(extra="ignore")

    email: str
    message: str | None = None
    role: str | None = None


class BulkCreateWorkspaceInvites(BaseModel):
    """POST body for `.../invitations/bulk/` -- one call for up to 100 emails."""

    model_config = ConfigDict(extra="ignore")

    emails: list[str] = Field(min_length=1, max_length=100)
    message: str | None = None
    role: str | None = None
