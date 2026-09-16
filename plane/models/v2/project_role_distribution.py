"""Workspace-wide project role distribution model for api_v2
(`GET /workspaces/{slug}/project-role-distribution/`).
"""

from __future__ import annotations

import builtins

from pydantic import BaseModel, ConfigDict


class ProjectRoleDistributionEntry(BaseModel):
    """Membership counts for one project role; no `id` field, `role_id` nullable (e.g. a deleted
    role) is the closest thing to identity."""

    model_config = ConfigDict(extra="allow")

    role_id: str | None = None
    name: str | None = None
    slug: str | None = None
    level: int | None = None
    is_system: bool | None = None
    membership_count: int
    distinct_member_count: int


class ProjectRoleDistribution(BaseModel):
    """Has no `id` field -- this is a single computed report, not an addressable
    row. Every field is required per the golden, with no `fields=` support."""

    model_config = ConfigDict(extra="allow")

    roles: builtins.list[ProjectRoleDistributionEntry]
    total_distinct_members: int
    total_memberships: int
