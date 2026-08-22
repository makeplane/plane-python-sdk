"""api_v2 surface. Reached as `client.v2`.
Chain `.workspace(slug)`/`.project(project)` (zero-I/O locators) for most
resources; 6 have no workspace in their path and sit on `V2Namespace` directly."""

from ...config import Configuration
from ._kernel.errors import FieldError, MultipleMatchesFound, NoMatchFound, PlaneAPIError
from ._kernel.transport import V2Transport
from .artifacts import Artifacts
from .assets import UserAssets, WorkspaceAssets
from .audit_logs import AuditLogs
from .automations import ProjectAutomations, WorkspaceAutomations
from .collections import CollectionMembers, CollectionPages, Collections
from .customer_properties import CustomerProperties
from .customers import Customers
from .cycles import Cycles
from .estimates import Estimates
from .features import ProjectFeatures, WorkspaceFeatures
from .group_sync import GroupSync
from .initiatives import Initiatives
from .intakes import Intakes
from .invitations import Invitations
from .labels import Labels
from .members import ProjectMembers, WorkspaceMembers
from .milestones import Milestones
from .modules import Modules
from .pages import ProjectPages, WikiPages
from .permission_schemes import PermissionSchemes
from .permissions import ProjectPermissions, WorkspacePermissions
from .project import Project
from .projects import Projects
from .releases import Releases
from .roles import Roles
from .states import States
from .stickies import Stickies
from .teamspaces import Teamspaces
from .users import Users
from .views import ProjectViews, WorkspaceViews
from .webhooks import Webhooks
from .wiki import Wiki
from .work_item_properties import WorkItemProperties, WorkspaceWorkItemProperties
from .work_item_relation_definitions import WorkItemRelationDefinitions
from .work_item_templates import ProjectWorkItemTemplates, WorkspaceWorkItemTemplates
from .work_item_types import WorkItemTypes, WorkspaceWorkItemTypes
from .work_items import WorkItems, WorkspaceWorkItems
from .workflows import Workflows
from .worklogs import ProjectWorklogs
from .workspace import Workspace


class V2Namespace:
    """The 6 non-workspace-scoped operations, plus the workspace locator.

    Everything else is reached via `.workspace(slug)` (`Workspace`) and `.project(project)`."""

    def __init__(self, config: Configuration) -> None:
        self.transport = V2Transport(config)
        self.users = Users(self.transport)
        self.user_assets = UserAssets(self.transport)

    def workspace(self, workspace_slug: str) -> Workspace:
        """Bind a workspace. Makes no request."""
        return Workspace(self.transport, workspace_slug)


__all__ = [
    "Artifacts",
    "AuditLogs",
    "ProjectAutomations",
    "WorkspaceAutomations",
    "CollectionMembers",
    "CollectionPages",
    "Collections",
    "Customers",
    "CustomerProperties",
    "Cycles",
    "Estimates",
    "FieldError",
    "GroupSync",
    "Initiatives",
    "Intakes",
    "Invitations",
    "Labels",
    "Milestones",
    "Modules",
    "MultipleMatchesFound",
    "NoMatchFound",
    "PermissionSchemes",
    "ProjectPermissions",
    "WorkspacePermissions",
    "PlaneAPIError",
    "Project",
    "ProjectFeatures",
    "ProjectMembers",
    "ProjectPages",
    "ProjectViews",
    "Projects",
    "ProjectWorklogs",
    "Releases",
    "Roles",
    "States",
    "Stickies",
    "Teamspaces",
    "UserAssets",
    "Users",
    "V2Namespace",
    "Webhooks",
    "Wiki",
    "WikiPages",
    "WorkItemProperties",
    "WorkItemRelationDefinitions",
    "WorkItems",
    "ProjectWorkItemTemplates",
    "WorkspaceWorkItemTemplates",
    "WorkItemTypes",
    "Workflows",
    "Workspace",
    "WorkspaceAssets",
    "WorkspaceFeatures",
    "WorkspaceMembers",
    "WorkspaceViews",
    "WorkspaceWorkItemProperties",
    "WorkspaceWorkItemTypes",
    "WorkspaceWorkItems",
]
