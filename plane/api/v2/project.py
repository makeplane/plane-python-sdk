"""Project locator: every project-scoped api_v2 resource, bound to one workspace
slug and one project. Constructed by `Workspace.project(...)`; makes no request."""

from __future__ import annotations

from ._kernel.transport import V2Transport
from .automations import ProjectAutomations
from .cycles import Cycles
from .estimates import Estimates
from .features import ProjectFeatures
from .intakes import Intakes
from .labels import Labels
from .members import ProjectMembers
from .milestones import Milestones
from .modules import Modules
from .pages import ProjectPages
from .permissions import ProjectPermissions
from .states import States
from .views import ProjectViews
from .work_item_properties import WorkItemProperties
from .work_item_templates import ProjectWorkItemTemplates
from .work_item_types import WorkItemTypes
from .work_items import WorkItems
from .workflows import Workflows
from .worklogs import ProjectWorklogs


class Project:
    """A project bound inside a workspace. Makes no request to construct."""

    def __init__(self, transport: V2Transport, slug: str, project_id: str) -> None:
        self.transport = transport
        self.slug = slug
        self.project_id = project_id

        self.work_items = WorkItems(transport, slug=slug, project_id=project_id)
        self.cycles = Cycles(transport, slug=slug, project_id=project_id)
        self.modules = Modules(transport, slug=slug, project_id=project_id)
        self.milestones = Milestones(transport, slug=slug, project_id=project_id)
        self.states = States(transport, slug=slug, project_id=project_id)
        self.labels = Labels(transport, slug=slug, project_id=project_id)
        self.members = ProjectMembers(transport, slug=slug, project_id=project_id)
        self.pages = ProjectPages(transport, slug=slug, project_id=project_id)
        self.views = ProjectViews(transport, slug=slug, project_id=project_id)
        self.features = ProjectFeatures(transport, slug=slug, project_id=project_id)
        self.permissions = ProjectPermissions(transport, slug=slug, project_id=project_id)
        self.intakes = Intakes(transport, slug=slug, project_id=project_id)
        self.estimates = Estimates(transport, slug=slug, project_id=project_id)
        self.work_item_types = WorkItemTypes(transport, slug=slug, project_id=project_id)
        self.work_item_properties = WorkItemProperties(
            transport, slug=slug, project_id=project_id
        )
        self.work_item_templates = ProjectWorkItemTemplates(
            transport, slug=slug, project_id=project_id
        )
        self.workflows = Workflows(transport, slug=slug, project_id=project_id)
        self.automations = ProjectAutomations(transport, slug=slug, project_id=project_id)
        self.worklogs = ProjectWorklogs(transport, slug=slug, project_id=project_id)
