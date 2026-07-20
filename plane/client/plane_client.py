from ..api.agent_runs import AgentRuns
from ..api.collections import Collections
from ..api.customers import Customers
from ..api.cycles import Cycles
from ..api.epics import Epics
from ..api.estimates import Estimates
from ..api.initiatives import Initiatives
from ..api.intake import Intake
from ..api.labels import Labels
from ..api.milestones import Milestones
from ..api.modules import Modules
from ..api.pages import Pages
from ..api.project_templates import ProjectTemplates
from ..api.projects import Projects
from ..api.releases import Releases
from ..api.roles import Roles
from ..api.states import States
from ..api.stickies import Stickies
from ..api.teamspaces import Teamspaces
from ..api.users import Users
from ..api.work_item_properties import WorkItemProperties
from ..api.work_item_relation_definitions import WorkItemRelationDefinitions
from ..api.work_item_types import WorkItemTypes
from ..api.work_items import WorkItems
from ..api.workflows import Workflows
from ..api.workspace_project_labels import WorkspaceProjectLabels
from ..api.workspace_project_states import WorkspaceProjectStates
from ..api.workspace_templates import WorkspaceTemplates
from ..api.workspace_work_item_properties import WorkspaceWorkItemProperties
from ..api.workspace_work_item_types import WorkspaceWorkItemTypes
from ..api.workspaces import Workspaces
from ..config import Configuration
from ..errors import ConfigurationError


class PlaneClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str | None = None,
        access_token: str | None = None,
    ) -> None:
        if not api_key and not access_token:
            raise ConfigurationError(
                "Either 'api_key' or 'access_token' must be provided for authentication"
            )
        if api_key and access_token:
            raise ConfigurationError(
                "Only one of 'api_key' or 'access_token' should be provided, not both"
            )

        self.config = Configuration(
            base_path=base_url,
            api_key=api_key,
            access_token=access_token,
        )

        self.users = Users(self.config)
        self.workspaces = Workspaces(self.config)
        self.projects = Projects(self.config)
        self.epics = Epics(self.config)
        self.work_items = WorkItems(self.config)
        self.pages = Pages(self.config)
        self.collections = Collections(self.config)
        self.labels = Labels(self.config)
        self.states = States(self.config)
        self.milestones = Milestones(self.config)
        self.modules = Modules(self.config)
        self.cycles = Cycles(self.config)
        self.estimates = Estimates(self.config)
        self.work_item_types = WorkItemTypes(self.config)
        self.work_item_properties = WorkItemProperties(self.config)
        self.customers = Customers(self.config)
        self.intake = Intake(self.config)
        self.agent_runs = AgentRuns(self.config)
        self.stickies = Stickies(self.config)
        self.initiatives = Initiatives(self.config)
        self.teamspaces = Teamspaces(self.config)
        self.workflows = Workflows(self.config)
        self.project_templates = ProjectTemplates(self.config)
        self.workspace_templates = WorkspaceTemplates(self.config)
        self.workspace_work_item_types = WorkspaceWorkItemTypes(self.config)
        self.workspace_work_item_properties = WorkspaceWorkItemProperties(self.config)
        self.workspace_project_labels = WorkspaceProjectLabels(self.config)
        self.workspace_project_states = WorkspaceProjectStates(self.config)
        self.work_item_relation_definitions = WorkItemRelationDefinitions(self.config)
        self.releases = Releases(self.config)
        self.roles = Roles(self.config)
