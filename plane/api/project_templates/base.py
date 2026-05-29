from typing import Any

from ..base_resource import BaseResource
from .page_templates import ProjectPageTemplates
from .work_item_templates import ProjectWorkItemTemplates


class ProjectTemplates(BaseResource):
    """API client for managing project-scoped templates (work items and pages)."""

    def __init__(self, config: Any) -> None:
        super().__init__(config, "/workspaces/")

        self.work_item_templates = ProjectWorkItemTemplates(config)
        self.page_templates = ProjectPageTemplates(config)
