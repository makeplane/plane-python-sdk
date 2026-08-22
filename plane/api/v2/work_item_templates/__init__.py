"""Work item templates (api_v2). `ProjectWorkItemTemplates` adds `use` (instantiate
a work item from the template); `WorkspaceWorkItemTemplates` has no `use`."""

from .project import ProjectWorkItemTemplates
from .workspace import WorkspaceWorkItemTemplates

__all__ = ["ProjectWorkItemTemplates", "WorkspaceWorkItemTemplates"]
