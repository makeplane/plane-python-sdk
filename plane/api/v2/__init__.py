"""api_v2 surface. Reached as `client.v2`.
Flat tree: `client.v2.workspaces.projects.states` (etc.) -- every resource is a
plain attribute, reached by attribute access, never a chain of locator calls.
`users`/`user_assets` have no workspace in their path and sit on `V2Namespace`
directly.

The 19 `Loaded*` row types are re-exported here too. They are the declared return
type of every `retrieve`/`list`/`iterate`/`find_by_*`/verb on a navigable resource,
so a caller must be able to *name* one -- to annotate a variable, a helper's
parameter or a test fixture -- without importing out of the private `_loaded`
package. `tests/v2/test_loaded_exports.py` keeps this set in step with the
resources: a new navigable family that forgets to export its row type fails there.
"""

from ...config import Configuration
from ._kernel.errors import (
    FieldError,
    FieldNotRequested,
    MissingPathId,
    MultipleMatchesFound,
    NoMatchFound,
    PlaneAPIError,
)
from ._kernel.transport import V2Transport
from ._loaded.automation import LoadedProjectAutomation, LoadedWorkspaceAutomation
from ._loaded.collection import LoadedCollection
from ._loaded.customer import LoadedCustomer
from ._loaded.cycle import LoadedCycle
from ._loaded.estimate import LoadedEstimate
from ._loaded.initiative import LoadedInitiative
from ._loaded.milestone import LoadedMilestone
from ._loaded.module import LoadedModule
from ._loaded.project import LoadedProject
from ._loaded.release import LoadedRelease
from ._loaded.webhook import LoadedWebhook
from ._loaded.work_item import LoadedWorkItem
from ._loaded.work_item_property import LoadedWorkItemProperty, LoadedWorkspaceWorkItemProperty
from ._loaded.work_item_type import LoadedWorkItemType, LoadedWorkspaceWorkItemType
from ._loaded.workflow import LoadedWorkflow
from ._loaded.workspace import LoadedWorkspace
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
from .projects import Projects
from .releases import Releases
from .roles import Roles
from .states import States
from .stickies import Stickies
from .teamspaces import Teamspaces
from .users import Users
from .views import ProjectViews, WorkspaceViews
from .webhooks import Webhooks
from .wiki_node import Wiki
from .work_item_properties import WorkItemProperties, WorkspaceWorkItemProperties
from .work_item_relation_definitions import WorkItemRelationDefinitions
from .work_item_templates import ProjectWorkItemTemplates, WorkspaceWorkItemTemplates
from .work_item_types import WorkItemTypes, WorkspaceWorkItemTypes
from .work_items import WorkItems, WorkspaceWorkItems
from .workflows import Workflows
from .worklogs import ProjectWorklogs
from .workspaces import Workspaces


class V2Namespace:
    """Root of the flat path: `client.v2.workspaces.projects.states.list(slug, project)`."""

    def __init__(self, config: Configuration) -> None:
        self.transport = V2Transport(config)
        self.users = Users(self.transport)
        self.user_assets = UserAssets(self.transport)
        self.workspaces = Workspaces(self.transport)


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
    "FieldNotRequested",
    "GroupSync",
    "Initiatives",
    "Intakes",
    "Invitations",
    "Labels",
    "LoadedCollection",
    "LoadedCustomer",
    "LoadedCycle",
    "LoadedEstimate",
    "LoadedInitiative",
    "LoadedMilestone",
    "LoadedModule",
    "LoadedProject",
    "LoadedProjectAutomation",
    "LoadedRelease",
    "LoadedWebhook",
    "LoadedWorkItem",
    "LoadedWorkItemProperty",
    "LoadedWorkItemType",
    "LoadedWorkflow",
    "LoadedWorkspace",
    "LoadedWorkspaceAutomation",
    "LoadedWorkspaceWorkItemProperty",
    "LoadedWorkspaceWorkItemType",
    "Milestones",
    "MissingPathId",
    "Modules",
    "MultipleMatchesFound",
    "NoMatchFound",
    "PermissionSchemes",
    "ProjectPermissions",
    "WorkspacePermissions",
    "PlaneAPIError",
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
    "Workspaces",
    "WorkspaceAssets",
    "WorkspaceFeatures",
    "WorkspaceMembers",
    "WorkspaceViews",
    "WorkspaceWorkItemProperties",
    "WorkspaceWorkItemTypes",
    "WorkspaceWorkItems",
]
