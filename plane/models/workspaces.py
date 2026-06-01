from pydantic import BaseModel, ConfigDict


class WorkspaceMember(BaseModel):
    """Workspace member model.

    Returned by Workspaces.get_members(). Includes the member's workspace role
    — fields that UserLite does not carry.
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    email: str | None = None
    display_name: str | None = None
    avatar: str | None = None
    avatar_url: str | None = None
    first_name: str | None = None
    last_name: str | None = None
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