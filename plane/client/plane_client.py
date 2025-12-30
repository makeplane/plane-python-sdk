from ..api.agent_runs import AgentRuns
from ..api.customers import Customers
from ..api.cycles import Cycles
from ..api.epics import Epics
from ..api.initiatives import Initiatives
from ..api.intake import Intake
from ..api.labels import Labels
from ..api.modules import Modules
from ..api.pages import Pages
from ..api.projects import Projects
from ..api.states import States
from ..api.stickies import Stickies
from ..api.teamspaces import Teamspaces
from ..api.users import Users
from ..api.work_item_properties import WorkItemProperties
from ..api.work_item_types import WorkItemTypes
from ..api.work_items import WorkItems
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
        self.labels = Labels(self.config)
        self.states = States(self.config)
        self.modules = Modules(self.config)
        self.cycles = Cycles(self.config)
        self.work_item_types = WorkItemTypes(self.config)
        self.work_item_properties = WorkItemProperties(self.config)
        self.customers = Customers(self.config)
        self.intake = Intake(self.config)
        self.agent_runs = AgentRuns(self.config)
        self.stickies = Stickies(self.config)
        self.initiatives = Initiatives(self.config)
        self.teamspaces = Teamspaces(self.config)

