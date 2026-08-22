"""`Workspace` -- the root scope, bound once. Constructing it makes no request:
it builds every workspace-level resource, each already bound with `slug`."""

from __future__ import annotations

from ._kernel.transport import V2Transport
from .artifacts import Artifacts
from .assets import WorkspaceAssets
from .audit_logs import AuditLogs
from .automations import WorkspaceAutomations
from .customer_properties import CustomerProperties
from .customers import Customers
from .features import WorkspaceFeatures
from .group_sync import GroupSync
from .initiatives import Initiatives
from .invitations import Invitations
from .members import WorkspaceMembers
from .permission_schemes import PermissionSchemes
from .permissions import WorkspacePermissions
from .project import Project
from .projects import Projects
from .releases import Releases
from .roles import Roles
from .stickies import Stickies
from .teamspaces import Teamspaces
from .views import WorkspaceViews
from .webhooks import Webhooks
from .wiki import Wiki
from .work_item_properties import WorkspaceWorkItemProperties
from .work_item_relation_definitions import WorkItemRelationDefinitions
from .work_item_templates import WorkspaceWorkItemTemplates
from .work_item_types import WorkspaceWorkItemTypes
from .work_items import WorkspaceWorkItems


class Workspace:
    """A workspace bound by slug. Makes no request to construct."""

    def __init__(self, transport: V2Transport, slug: str) -> None:
        self.transport = transport
        self.slug = slug

        self.projects = Projects(transport, slug=slug)
        self.members = WorkspaceMembers(transport, slug=slug)
        self.invitations = Invitations(transport, slug=slug)
        self.roles = Roles(transport, slug=slug)
        self.permission_schemes = PermissionSchemes(transport, slug=slug)
        self.permissions = WorkspacePermissions(transport, slug=slug)
        self.features = WorkspaceFeatures(transport, slug=slug)
        self.audit_logs = AuditLogs(transport, slug=slug)
        self.views = WorkspaceViews(transport, slug=slug)
        self.work_items = WorkspaceWorkItems(transport, slug=slug)
        self.work_item_types = WorkspaceWorkItemTypes(transport, slug=slug)
        self.work_item_properties = WorkspaceWorkItemProperties(transport, slug=slug)
        self.work_item_relation_definitions = WorkItemRelationDefinitions(
            transport, slug=slug
        )
        self.work_item_templates = WorkspaceWorkItemTemplates(transport, slug=slug)
        self.group_sync = GroupSync(transport, slug=slug)
        self.automations = WorkspaceAutomations(transport, slug=slug)
        self.assets = WorkspaceAssets(transport, slug=slug)
        self.artifacts = Artifacts(transport, slug=slug)
        self.webhooks = Webhooks(transport, slug=slug)
        self.stickies = Stickies(transport, slug=slug)
        self.teamspaces = Teamspaces(transport, slug=slug)
        self.customers = Customers(transport, slug=slug)
        self.customer_properties = CustomerProperties(transport, slug=slug)
        self.initiatives = Initiatives(transport, slug=slug)
        self.releases = Releases(transport, slug=slug)
        self.wiki = Wiki(transport, slug=slug)

    def project(self, project: str) -> Project:
        """Bind a project inside this workspace. Makes no request. `project`
        accepts a project id or its key (e.g. `"ENG"`)."""
        return Project(self.transport, self.slug, project)
