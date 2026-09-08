"""Workspaces (api_v2) -- the root of the flat tree:
`client.v2.workspaces.projects.states.list(slug, project)`.

Every workspace-scoped family hangs off this class, and
`tests/v2/test_tree.py`'s `WORKSPACE_TREE_ATTACHMENTS` table carries a row per
attachment -- attach one without a row and its completeness assertion fails by
name."""

from __future__ import annotations

from collections.abc import Sequence

from typing_extensions import Never

from ...models.v2.workspaces import Workspace
from ._generated.constants import WorkspacesRetrieveField
from ._kernel.resource import V2Resource
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
from .projects import Projects
from .releases import Releases
from .roles import Roles
from .stickies import Stickies
from .teamspaces import Teamspaces
from .views import WorkspaceViews
from .webhooks import Webhooks
from .wiki_node import Wiki
from .work_item_properties import WorkspaceWorkItemProperties
from .work_item_relation_definitions import WorkItemRelationDefinitions
from .work_item_templates import WorkspaceWorkItemTemplates
from .work_item_types import WorkspaceWorkItemTypes
from .work_items import WorkspaceWorkItems


class Workspaces(V2Resource[Workspace, Never, Never]):
    path = "/workspaces/{slug}/"
    model = Workspace
    operations = {"retrieve": "workspaces_retrieve"}

    def __init__(self, transport: V2Transport) -> None:
        super().__init__(transport)
        self.projects = Projects(transport)
        self.wiki = Wiki(transport)
        self.features = WorkspaceFeatures(transport)
        self.releases = Releases(transport)
        self.artifacts = Artifacts(transport)
        self.assets = WorkspaceAssets(transport)
        self.audit_logs = AuditLogs(transport)
        self.automations = WorkspaceAutomations(transport)
        self.customer_properties = CustomerProperties(transport)
        self.customers = Customers(transport)
        self.group_sync = GroupSync(transport)
        self.initiatives = Initiatives(transport)
        self.invitations = Invitations(transport)
        self.members = WorkspaceMembers(transport)
        self.permission_schemes = PermissionSchemes(transport)
        self.permissions = WorkspacePermissions(transport)
        self.roles = Roles(transport)
        self.stickies = Stickies(transport)
        self.teamspaces = Teamspaces(transport)
        self.views = WorkspaceViews(transport)
        self.webhooks = Webhooks(transport)
        self.work_item_properties = WorkspaceWorkItemProperties(transport)
        self.work_item_relation_definitions = WorkItemRelationDefinitions(transport)
        self.work_item_templates = WorkspaceWorkItemTemplates(transport)
        self.work_item_types = WorkspaceWorkItemTypes(transport)
        self.work_items = WorkspaceWorkItems(transport)

    def retrieve(
        self, slug: str, *, fields: Sequence[WorkspacesRetrieveField] | None = None
    ) -> Workspace:
        """The workspace detail route has no pk -- the slug is the key -- so this is a
        singleton read, not `_retrieve` (which would append a `None` pk segment)."""
        return self._retrieve_singleton(action="retrieve", params={"fields": fields}, slug=slug)
