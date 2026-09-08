"""A fetched workspace row that is also the place its children live.

The design's navigable row #1 and the SDK's most-used entry point: every family in
api_v2 hangs off a workspace, so `client.v2.workspaces.retrieve("acme")` handing
back a bare `Workspace` meant `workspace.projects` was an `AttributeError` while
every other fetch in the SDK returned a navigable row.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, cast

from ....models.v2.workspaces import Workspace
from .._kernel.loaded import Loaded, Owned, bind1

if TYPE_CHECKING:
    from ..artifacts import Artifacts
    from ..assets import WorkspaceAssets
    from ..audit_logs import AuditLogs
    from ..automations import WorkspaceAutomations
    from ..customer_properties import CustomerProperties
    from ..customers.customers import Customers
    from ..features import WorkspaceFeatures
    from ..initiatives.initiatives import Initiatives
    from ..invitations import Invitations
    from ..members import WorkspaceMembers
    from ..permission_schemes import PermissionSchemes
    from ..permissions import WorkspacePermissions
    from ..projects import Projects
    from ..releases import Releases
    from ..releases.tags import ReleaseTags
    from ..roles import Roles
    from ..stickies import Stickies
    from ..teamspaces import Teamspaces
    from ..views.workspace import WorkspaceViews
    from ..webhooks import Webhooks
    from ..work_item_properties import WorkspaceWorkItemProperties
    from ..work_item_relation_definitions import WorkItemRelationDefinitions
    from ..work_item_templates.workspace import WorkspaceWorkItemTemplates
    from ..work_item_types import WorkspaceWorkItemTypes
    from ..work_items.workspace import WorkspaceWorkItems
    from ..workspaces import Workspaces

    # Typed views on `Owned`: the child resource's own methods with `slug` already
    # supplied -- `bind1`, because a workspace binds exactly one path id (it is the
    # root of the tree, so there is no ancestor above it). One line per method.
    # Evaluated only by a type checker -- at runtime these properties return a plain
    # `Owned`.
    #
    # There is one view per resource `Workspaces.__init__` attaches, and
    # `tests/v2/test_loaded_navigation.py` sweeps that correspondence rather than
    # trusting it: a child attached without a property here fails by name.

    class _OwnedProjects(Owned["Projects"]):
        list = staticmethod(bind1(Projects.list))
        iterate = staticmethod(bind1(Projects.iterate))
        retrieve = staticmethod(bind1(Projects.retrieve))
        find_by_name = staticmethod(bind1(Projects.find_by_name))
        create = staticmethod(bind1(Projects.create))
        update = staticmethod(bind1(Projects.update))
        delete = staticmethod(bind1(Projects.delete))
        upsert = staticmethod(bind1(Projects.upsert))
        bulk_create = staticmethod(bind1(Projects.bulk_create))
        bulk_update = staticmethod(bind1(Projects.bulk_update))
        archive = staticmethod(bind1(Projects.archive))
        unarchive = staticmethod(bind1(Projects.unarchive))
        summary = staticmethod(bind1(Projects.summary))
        role_distribution = staticmethod(bind1(Projects.role_distribution))

    class _OwnedWorkspaceFeatures(Owned["WorkspaceFeatures"]):
        get = staticmethod(bind1(WorkspaceFeatures.get))
        update = staticmethod(bind1(WorkspaceFeatures.update))

    class _OwnedReleases(Owned["Releases"]):
        list = staticmethod(bind1(Releases.list))
        iterate = staticmethod(bind1(Releases.iterate))
        retrieve = staticmethod(bind1(Releases.retrieve))
        find_by_name = staticmethod(bind1(Releases.find_by_name))
        create = staticmethod(bind1(Releases.create))
        update = staticmethod(bind1(Releases.update))
        delete = staticmethod(bind1(Releases.delete))

    class _OwnedReleaseTags(Owned["ReleaseTags"]):
        list = staticmethod(bind1(ReleaseTags.list))
        iterate = staticmethod(bind1(ReleaseTags.iterate))
        retrieve = staticmethod(bind1(ReleaseTags.retrieve))
        find_by_version = staticmethod(bind1(ReleaseTags.find_by_version))
        create = staticmethod(bind1(ReleaseTags.create))
        update = staticmethod(bind1(ReleaseTags.update))
        delete = staticmethod(bind1(ReleaseTags.delete))

    class _OwnedArtifacts(Owned["Artifacts"]):
        create = staticmethod(bind1(Artifacts.create))
        retrieve = staticmethod(bind1(Artifacts.retrieve))
        publish = staticmethod(bind1(Artifacts.publish))
        update = staticmethod(bind1(Artifacts.update))

    class _OwnedWorkspaceAssets(Owned["WorkspaceAssets"]):
        list = staticmethod(bind1(WorkspaceAssets.list))
        iterate = staticmethod(bind1(WorkspaceAssets.iterate))
        retrieve = staticmethod(bind1(WorkspaceAssets.retrieve))
        create = staticmethod(bind1(WorkspaceAssets.create))
        update = staticmethod(bind1(WorkspaceAssets.update))
        delete = staticmethod(bind1(WorkspaceAssets.delete))

    class _OwnedAuditLogs(Owned["AuditLogs"]):
        list = staticmethod(bind1(AuditLogs.list))
        iterate = staticmethod(bind1(AuditLogs.iterate))
        retrieve = staticmethod(bind1(AuditLogs.retrieve))

    class _OwnedWorkspaceAutomations(Owned["WorkspaceAutomations"]):
        list = staticmethod(bind1(WorkspaceAutomations.list))
        iterate = staticmethod(bind1(WorkspaceAutomations.iterate))
        retrieve = staticmethod(bind1(WorkspaceAutomations.retrieve))
        find_by_name = staticmethod(bind1(WorkspaceAutomations.find_by_name))
        create = staticmethod(bind1(WorkspaceAutomations.create))
        update = staticmethod(bind1(WorkspaceAutomations.update))
        delete = staticmethod(bind1(WorkspaceAutomations.delete))
        set_status = staticmethod(bind1(WorkspaceAutomations.set_status))

    class _OwnedCustomerProperties(Owned["CustomerProperties"]):
        list = staticmethod(bind1(CustomerProperties.list))
        iterate = staticmethod(bind1(CustomerProperties.iterate))
        retrieve = staticmethod(bind1(CustomerProperties.retrieve))
        find_by_name = staticmethod(bind1(CustomerProperties.find_by_name))
        find_by_display_name = staticmethod(bind1(CustomerProperties.find_by_display_name))
        create = staticmethod(bind1(CustomerProperties.create))
        update = staticmethod(bind1(CustomerProperties.update))
        delete = staticmethod(bind1(CustomerProperties.delete))

    class _OwnedCustomers(Owned["Customers"]):
        list = staticmethod(bind1(Customers.list))
        iterate = staticmethod(bind1(Customers.iterate))
        retrieve = staticmethod(bind1(Customers.retrieve))
        find_by_name = staticmethod(bind1(Customers.find_by_name))
        create = staticmethod(bind1(Customers.create))
        update = staticmethod(bind1(Customers.update))
        delete = staticmethod(bind1(Customers.delete))
        upsert = staticmethod(bind1(Customers.upsert))

    class _OwnedInitiatives(Owned["Initiatives"]):
        list = staticmethod(bind1(Initiatives.list))
        iterate = staticmethod(bind1(Initiatives.iterate))
        retrieve = staticmethod(bind1(Initiatives.retrieve))
        find_by_name = staticmethod(bind1(Initiatives.find_by_name))
        create = staticmethod(bind1(Initiatives.create))
        update = staticmethod(bind1(Initiatives.update))
        delete = staticmethod(bind1(Initiatives.delete))

    class _OwnedInvitations(Owned["Invitations"]):
        list = staticmethod(bind1(Invitations.list))
        iterate = staticmethod(bind1(Invitations.iterate))
        retrieve = staticmethod(bind1(Invitations.retrieve))
        create = staticmethod(bind1(Invitations.create))
        delete = staticmethod(bind1(Invitations.delete))
        bulk = staticmethod(bind1(Invitations.bulk))

    class _OwnedWorkspaceMembers(Owned["WorkspaceMembers"]):
        list = staticmethod(bind1(WorkspaceMembers.list))
        iterate = staticmethod(bind1(WorkspaceMembers.iterate))
        remove = staticmethod(bind1(WorkspaceMembers.remove))

    class _OwnedPermissionSchemes(Owned["PermissionSchemes"]):
        list = staticmethod(bind1(PermissionSchemes.list))
        iterate = staticmethod(bind1(PermissionSchemes.iterate))
        retrieve = staticmethod(bind1(PermissionSchemes.retrieve))

    class _OwnedWorkspacePermissions(Owned["WorkspacePermissions"]):
        me = staticmethod(bind1(WorkspacePermissions.me))

    class _OwnedRoles(Owned["Roles"]):
        list = staticmethod(bind1(Roles.list))
        iterate = staticmethod(bind1(Roles.iterate))
        retrieve = staticmethod(bind1(Roles.retrieve))
        find_by_name = staticmethod(bind1(Roles.find_by_name))
        find_by_slug = staticmethod(bind1(Roles.find_by_slug))

    class _OwnedStickies(Owned["Stickies"]):
        list = staticmethod(bind1(Stickies.list))
        iterate = staticmethod(bind1(Stickies.iterate))
        retrieve = staticmethod(bind1(Stickies.retrieve))
        create = staticmethod(bind1(Stickies.create))
        update = staticmethod(bind1(Stickies.update))
        delete = staticmethod(bind1(Stickies.delete))

    class _OwnedTeamspaces(Owned["Teamspaces"]):
        list = staticmethod(bind1(Teamspaces.list))
        iterate = staticmethod(bind1(Teamspaces.iterate))
        retrieve = staticmethod(bind1(Teamspaces.retrieve))
        find_by_name = staticmethod(bind1(Teamspaces.find_by_name))
        create = staticmethod(bind1(Teamspaces.create))
        update = staticmethod(bind1(Teamspaces.update))
        delete = staticmethod(bind1(Teamspaces.delete))

    class _OwnedWorkspaceViews(Owned["WorkspaceViews"]):
        list = staticmethod(bind1(WorkspaceViews.list))
        iterate = staticmethod(bind1(WorkspaceViews.iterate))
        retrieve = staticmethod(bind1(WorkspaceViews.retrieve))
        create = staticmethod(bind1(WorkspaceViews.create))
        update = staticmethod(bind1(WorkspaceViews.update))
        delete = staticmethod(bind1(WorkspaceViews.delete))

    class _OwnedWebhooks(Owned["Webhooks"]):
        list = staticmethod(bind1(Webhooks.list))
        iterate = staticmethod(bind1(Webhooks.iterate))
        retrieve = staticmethod(bind1(Webhooks.retrieve))
        find_by_name = staticmethod(bind1(Webhooks.find_by_name))
        create = staticmethod(bind1(Webhooks.create))
        update = staticmethod(bind1(Webhooks.update))
        delete = staticmethod(bind1(Webhooks.delete))
        regenerate = staticmethod(bind1(Webhooks.regenerate))

    class _OwnedWorkspaceWorkItemProperties(Owned["WorkspaceWorkItemProperties"]):
        list = staticmethod(bind1(WorkspaceWorkItemProperties.list))
        iterate = staticmethod(bind1(WorkspaceWorkItemProperties.iterate))
        retrieve = staticmethod(bind1(WorkspaceWorkItemProperties.retrieve))
        find_by_name = staticmethod(bind1(WorkspaceWorkItemProperties.find_by_name))
        find_by_display_name = staticmethod(bind1(WorkspaceWorkItemProperties.find_by_display_name))
        create = staticmethod(bind1(WorkspaceWorkItemProperties.create))
        update = staticmethod(bind1(WorkspaceWorkItemProperties.update))
        delete = staticmethod(bind1(WorkspaceWorkItemProperties.delete))

    class _OwnedWorkItemRelationDefinitions(Owned["WorkItemRelationDefinitions"]):
        list = staticmethod(bind1(WorkItemRelationDefinitions.list))
        iterate = staticmethod(bind1(WorkItemRelationDefinitions.iterate))
        retrieve = staticmethod(bind1(WorkItemRelationDefinitions.retrieve))
        find_by_name = staticmethod(bind1(WorkItemRelationDefinitions.find_by_name))
        create = staticmethod(bind1(WorkItemRelationDefinitions.create))
        update = staticmethod(bind1(WorkItemRelationDefinitions.update))
        delete = staticmethod(bind1(WorkItemRelationDefinitions.delete))

    class _OwnedWorkspaceWorkItemTemplates(Owned["WorkspaceWorkItemTemplates"]):
        list = staticmethod(bind1(WorkspaceWorkItemTemplates.list))
        iterate = staticmethod(bind1(WorkspaceWorkItemTemplates.iterate))
        retrieve = staticmethod(bind1(WorkspaceWorkItemTemplates.retrieve))
        create = staticmethod(bind1(WorkspaceWorkItemTemplates.create))
        update = staticmethod(bind1(WorkspaceWorkItemTemplates.update))
        delete = staticmethod(bind1(WorkspaceWorkItemTemplates.delete))

    class _OwnedWorkspaceWorkItemTypes(Owned["WorkspaceWorkItemTypes"]):
        list = staticmethod(bind1(WorkspaceWorkItemTypes.list))
        iterate = staticmethod(bind1(WorkspaceWorkItemTypes.iterate))
        retrieve = staticmethod(bind1(WorkspaceWorkItemTypes.retrieve))
        find_by_name = staticmethod(bind1(WorkspaceWorkItemTypes.find_by_name))
        create = staticmethod(bind1(WorkspaceWorkItemTypes.create))
        update = staticmethod(bind1(WorkspaceWorkItemTypes.update))
        delete = staticmethod(bind1(WorkspaceWorkItemTypes.delete))
        mark_default = staticmethod(bind1(WorkspaceWorkItemTypes.mark_default))

    class _OwnedWorkspaceWorkItems(Owned["WorkspaceWorkItems"]):
        list = staticmethod(bind1(WorkspaceWorkItems.list))
        iterate = staticmethod(bind1(WorkspaceWorkItems.iterate))
        retrieve_by_identifier = staticmethod(bind1(WorkspaceWorkItems.retrieve_by_identifier))


class LoadedWorkspace(Loaded, Workspace):
    """A workspace row that is also the place its children live.

    Every one of the twenty-five resources `Workspaces.__init__` attaches is
    reachable here, so `workspace.projects.list()` works exactly the way
    `workspace.roles.list()` does, with the slug supplied once at fetch time.

    The two grouping nodes -- `wiki` and `group_sync` -- are deliberately absent.
    Neither holds a `V2Resource` base of its own (they consume no path id), so
    neither is a child in the sense a loaded row can bind: their children each take
    `slug` themselves. Reach them through `client.v2.workspaces.wiki.pages` and
    `client.v2.workspaces.group_sync.config` directly.
    """

    model_config = {**Workspace.model_config, "arbitrary_types_allowed": True}

    if TYPE_CHECKING:
        # Type-checker-only declaration; `Workspaces._load` sets it with
        # `object.__setattr__`. A runtime annotation would become a pydantic
        # private attribute.
        _resources: Workspaces

    @property
    def projects(self) -> _OwnedProjects:
        return cast(
            "_OwnedProjects",
            Owned(self._resources.projects, self._ids, self._id_names),
        )

    @property
    def features(self) -> _OwnedWorkspaceFeatures:
        return cast(
            "_OwnedWorkspaceFeatures",
            Owned(self._resources.features, self._ids, self._id_names),
        )

    @property
    def releases(self) -> _OwnedReleases:
        return cast(
            "_OwnedReleases",
            Owned(self._resources.releases, self._ids, self._id_names),
        )

    @property
    def release_tags(self) -> _OwnedReleaseTags:
        return cast(
            "_OwnedReleaseTags",
            Owned(self._resources.release_tags, self._ids, self._id_names),
        )

    @property
    def artifacts(self) -> _OwnedArtifacts:
        return cast(
            "_OwnedArtifacts",
            Owned(self._resources.artifacts, self._ids, self._id_names),
        )

    @property
    def assets(self) -> _OwnedWorkspaceAssets:
        return cast(
            "_OwnedWorkspaceAssets",
            Owned(self._resources.assets, self._ids, self._id_names),
        )

    @property
    def audit_logs(self) -> _OwnedAuditLogs:
        return cast(
            "_OwnedAuditLogs",
            Owned(self._resources.audit_logs, self._ids, self._id_names),
        )

    @property
    def automations(self) -> _OwnedWorkspaceAutomations:
        return cast(
            "_OwnedWorkspaceAutomations",
            Owned(self._resources.automations, self._ids, self._id_names),
        )

    @property
    def customer_properties(self) -> _OwnedCustomerProperties:
        return cast(
            "_OwnedCustomerProperties",
            Owned(self._resources.customer_properties, self._ids, self._id_names),
        )

    @property
    def customers(self) -> _OwnedCustomers:
        return cast(
            "_OwnedCustomers",
            Owned(self._resources.customers, self._ids, self._id_names),
        )

    @property
    def initiatives(self) -> _OwnedInitiatives:
        return cast(
            "_OwnedInitiatives",
            Owned(self._resources.initiatives, self._ids, self._id_names),
        )

    @property
    def invitations(self) -> _OwnedInvitations:
        return cast(
            "_OwnedInvitations",
            Owned(self._resources.invitations, self._ids, self._id_names),
        )

    @property
    def members(self) -> _OwnedWorkspaceMembers:
        return cast(
            "_OwnedWorkspaceMembers",
            Owned(self._resources.members, self._ids, self._id_names),
        )

    @property
    def permission_schemes(self) -> _OwnedPermissionSchemes:
        return cast(
            "_OwnedPermissionSchemes",
            Owned(self._resources.permission_schemes, self._ids, self._id_names),
        )

    @property
    def permissions(self) -> _OwnedWorkspacePermissions:
        return cast(
            "_OwnedWorkspacePermissions",
            Owned(self._resources.permissions, self._ids, self._id_names),
        )

    @property
    def roles(self) -> _OwnedRoles:
        return cast(
            "_OwnedRoles",
            Owned(self._resources.roles, self._ids, self._id_names),
        )

    @property
    def stickies(self) -> _OwnedStickies:
        return cast(
            "_OwnedStickies",
            Owned(self._resources.stickies, self._ids, self._id_names),
        )

    @property
    def teamspaces(self) -> _OwnedTeamspaces:
        return cast(
            "_OwnedTeamspaces",
            Owned(self._resources.teamspaces, self._ids, self._id_names),
        )

    @property
    def views(self) -> _OwnedWorkspaceViews:
        return cast(
            "_OwnedWorkspaceViews",
            Owned(self._resources.views, self._ids, self._id_names),
        )

    @property
    def webhooks(self) -> _OwnedWebhooks:
        return cast(
            "_OwnedWebhooks",
            Owned(self._resources.webhooks, self._ids, self._id_names),
        )

    @property
    def work_item_properties(self) -> _OwnedWorkspaceWorkItemProperties:
        return cast(
            "_OwnedWorkspaceWorkItemProperties",
            Owned(self._resources.work_item_properties, self._ids, self._id_names),
        )

    @property
    def work_item_relation_definitions(self) -> _OwnedWorkItemRelationDefinitions:
        return cast(
            "_OwnedWorkItemRelationDefinitions",
            Owned(self._resources.work_item_relation_definitions, self._ids, self._id_names),
        )

    @property
    def work_item_templates(self) -> _OwnedWorkspaceWorkItemTemplates:
        return cast(
            "_OwnedWorkspaceWorkItemTemplates",
            Owned(self._resources.work_item_templates, self._ids, self._id_names),
        )

    @property
    def work_item_types(self) -> _OwnedWorkspaceWorkItemTypes:
        return cast(
            "_OwnedWorkspaceWorkItemTypes",
            Owned(self._resources.work_item_types, self._ids, self._id_names),
        )

    @property
    def work_items(self) -> _OwnedWorkspaceWorkItems:
        return cast(
            "_OwnedWorkspaceWorkItems",
            Owned(self._resources.work_items, self._ids, self._id_names),
        )
