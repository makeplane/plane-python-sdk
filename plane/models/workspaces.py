from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse
from .users import UserLite


class WorkspaceMember(UserLite):
    """Workspace member model.

    Extends UserLite with workspace-scoped role fields. Returned by
    Workspaces.get_members(). isinstance(member, UserLite) remains True,
    so existing callers that type-check against UserLite are unaffected.
    """

    role: int | None = None
    role_slug: str | None = None
    is_active: bool | None = None
    is_bot: bool | None = None


class PaginatedWorkspaceMemberResponse(PaginatedResponse):
    """Paginated response for the workspace members-lite endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[WorkspaceMember]


class WorkspaceFeature(BaseModel):
    """Workspace feature model.

    All fields are optional so a caller can toggle a single feature; the update
    endpoint is a partial (PATCH) that only applies the fields that are sent.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    project_grouping: bool | None = None
    initiatives: bool | None = None
    teams: bool | None = None
    customers: bool | None = None
    wiki: bool | None = None
    pi: bool | None = None


class ProjectRoleDistributionEntry(BaseModel):
    """Per-role membership counts within a workspace's project-role distribution."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    role_id: str | None = None
    name: str | None = None
    slug: str | None = None
    is_system: bool | None = None
    level: int | None = None
    membership_count: int | None = None
    distinct_member_count: int | None = None


class ProjectRoleDistribution(BaseModel):
    """Aggregate count of project members by role across a workspace.

    Counts span all active (non-archived) projects in the workspace and include
    both built-in roles (admin, contributor, commenter, guest) and custom roles.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    total_memberships: int | None = None
    total_distinct_members: int | None = None
    roles: list[ProjectRoleDistributionEntry] = []
