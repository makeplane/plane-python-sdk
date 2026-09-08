"""Workspaces (api_v2) -- the root of the flat tree:
`client.v2.workspaces.projects.states.list(slug, project)`.

Every workspace-scoped family hangs off this class, and
`tests/v2/test_tree.py`'s `WORKSPACE_TREE_ATTACHMENTS` table carries a row per
attachment -- attach one without a row and its completeness assertion fails by
name.

A fetched workspace (`retrieve`) comes back as a `LoadedWorkspace`: it carries the
row's data and reaches every one of those families without the caller repeating the
slug (`workspace.projects.list()`). `tests/v2/test_loaded_navigation.py` proves the
two sides stay in step."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from typing_extensions import Never

from ...models.v2.workspaces import Workspace
from ._generated.constants import WorkspacesRetrieveField
from ._kernel.loaded import LoadsNavigableRows
from ._kernel.resource import V2Resource
from ._kernel.transport import V2Transport
from ._loaded.workspace import LoadedWorkspace
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


class Workspaces(V2Resource[Workspace, Never, Never], LoadsNavigableRows[LoadedWorkspace]):
    path = "/workspaces/{slug}/"
    model = Workspace
    loaded_model = LoadedWorkspace
    loaded_names = ("slug",)
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
    ) -> LoadedWorkspace:
        """Fetch a workspace. The detail route has no pk -- the slug is the key -- so
        this is a singleton read, not `_retrieve` (which would append a `None` pk
        segment).

        Answers a `LoadedWorkspace`, so `workspace.projects.list()` and every other
        family work without repeating the slug."""
        row = self._retrieve_singleton(action="retrieve", params={"fields": fields}, slug=slug)
        if row.slug is None:
            # `fields=` projected the slug away. Every other resource falls back to
            # `id` here; a workspace cannot, because the `{slug}` segment its children
            # open with does not accept the UUID. The caller's own `slug` is the value
            # the row was just fetched by, so fill it in rather than build
            # `/workspaces/None/...` children off the row.
            #
            # This does not widen what the caller can read: `_load` gets their own
            # `fields`, and `Loaded.build` intersects presence with it, so
            # `workspace.slug` still raises `FieldNotRequested` when they did not ask.
            row.slug = slug
        return self._load(row, fields=fields)

    # -- Navigation -----------------------------------------------------------------

    def _row_id(self, row: Workspace) -> Any:
        """Children address a workspace by its slug -- `/workspaces/acme/projects/`,
        never the UUID `id`, which that segment does not accept."""
        return row.slug
