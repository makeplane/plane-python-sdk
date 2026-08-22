"""Member models for api_v2; `Member` backs both `ProjectMembers` and `WorkspaceMembers`
(structurally identical schemas)."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class Member(BaseModel):
    """A roster row. `role` is a slug from `role_ref` -- context-correct
    (workspace `"member"` vs project `"contributor"`, custom roles, `"owner"`);
    null only for legacy rows."""

    model_config = ConfigDict(extra="allow")

    id: str
    member_id: str | None = None
    role: str | None = None


class CreateProjectMember(BaseModel):
    """POST body to add a member to a project. The golden names no required
    field, but `member_id` is what makes the call meaningful."""

    model_config = ConfigDict(extra="ignore")

    member_id: str | None = None
    role: str | None = None


class UpdateProjectMember(BaseModel):
    """PATCH body -- change a project member's role. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    member_id: str | None = None
    role: str | None = None


class WorkspaceMemberRemove(BaseModel):
    """POST body for `WorkspaceMembers.remove` (v1 parity) -- removes by email,
    not by member row id; `remove_seat` additionally frees the license seat."""

    model_config = ConfigDict(extra="ignore")

    email: str
    remove_seat: bool = False
