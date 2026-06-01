from pydantic import BaseModel, ConfigDict

from .users import UserLite


class WorkspaceMember(UserLite):
    """Workspace member model.

    Extends UserLite with workspace-scoped role fields. Returned by
    Workspaces.get_members(). isinstance(member, UserLite) remains True,
    so existing callers that type-check against UserLite are unaffected.
    """

    role: int | None = None
    role_slug: str | None = None


class WorkspaceFeature(BaseModel):
  """Workspace feature model."""

  model_config = ConfigDict(extra="allow", populate_by_name=True)

  project_grouping: bool
  initiatives: bool
  teams: bool
  customers: bool
  wiki: bool
  pi: bool