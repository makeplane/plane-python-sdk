from pydantic import BaseModel, ConfigDict

class WorkspaceFeature(BaseModel):
  """Workspace feature model."""

  model_config = ConfigDict(extra="allow", populate_by_name=True)

  project_grouping: bool
  initiatives: bool
  teams: bool
  customers: bool
  wiki: bool
  pi: bool