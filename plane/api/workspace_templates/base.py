from typing import Any

from ..base_resource import BaseResource
from .page_templates import WorkspacePageTemplates
from .project_templates import WorkspaceProjectTemplates
from .workitem_templates import WorkspaceWorkItemTemplates


class WorkspaceTemplates(BaseResource):
    """Container for workspace-level template sub-resources."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        # Initialize sub-resources
        self.work_items = WorkspaceWorkItemTemplates(config)
        self.projects = WorkspaceProjectTemplates(config)
        self.pages = WorkspacePageTemplates(config)
