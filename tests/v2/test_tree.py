import importlib.util

import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2.artifacts import Artifacts
from plane.api.v2.assets import WorkspaceAssets
from plane.api.v2.audit_logs import AuditLogs
from plane.api.v2.automations import (
    ProjectAutomationActivities,
    ProjectAutomationEdges,
    ProjectAutomationNodes,
    ProjectAutomations,
    WorkspaceAutomationActivities,
    WorkspaceAutomationEdges,
    WorkspaceAutomationNodes,
    WorkspaceAutomations,
)
from plane.api.v2.collections import CollectionMembers, CollectionPages, Collections
from plane.api.v2.customer_properties import CustomerProperties
from plane.api.v2.customers import (
    CustomerPropertyValues,
    CustomerRequests,
    Customers,
    CustomerWorkItems,
)
from plane.api.v2.cycles import Cycles, CycleWorkItems
from plane.api.v2.estimates import Estimates
from plane.api.v2.estimates.points import EstimatePoints
from plane.api.v2.features import ProjectFeatures
from plane.api.v2.group_sync import (
    GroupSync,
    GroupSyncConfigResource,
    GroupSyncProjectMappings,
    GroupSyncWorkspaceMappings,
)
from plane.api.v2.initiatives import (
    InitiativeLabels,
    InitiativeProjects,
    Initiatives,
    InitiativeWorkItems,
)
from plane.api.v2.intakes import Intakes
from plane.api.v2.invitations import Invitations
from plane.api.v2.labels import Labels
from plane.api.v2.members import ProjectMembers, WorkspaceMembers
from plane.api.v2.milestones import Milestones, MilestoneWorkItems
from plane.api.v2.modules import Modules, ModuleWorkItems
from plane.api.v2.pages import ProjectPages
from plane.api.v2.permission_schemes import PermissionSchemes
from plane.api.v2.permissions import ProjectPermissions, WorkspacePermissions
from plane.api.v2.releases.tags import ReleaseTags
from plane.api.v2.roles import Roles
from plane.api.v2.states import States
from plane.api.v2.stickies import Stickies
from plane.api.v2.teamspaces import Teamspaces
from plane.api.v2.views import WorkspaceViews
from plane.api.v2.views.project import ProjectViews
from plane.api.v2.webhook_logs import WebhookLogs
from plane.api.v2.webhooks import Webhooks
from plane.api.v2.work_item_properties import (
    WorkItemProperties,
    WorkItemPropertyContexts,
    WorkItemPropertyOptions,
    WorkspaceWorkItemProperties,
    WorkspaceWorkItemPropertyOptions,
)
from plane.api.v2.work_item_relation_definitions import WorkItemRelationDefinitions
from plane.api.v2.work_item_templates import WorkspaceWorkItemTemplates
from plane.api.v2.work_item_templates.project import ProjectWorkItemTemplates
from plane.api.v2.work_item_types import (
    WorkItemTypeProperties,
    WorkItemTypes,
    WorkspaceWorkItemTypeProperties,
    WorkspaceWorkItemTypes,
)
from plane.api.v2.work_items import WorkspaceWorkItems
from plane.api.v2.workflows import Workflows, WorkflowStates, WorkflowTransitions
from plane.api.v2.worklogs import ProjectWorklogs
from plane.config import Configuration
from tests.v2.tree_walk import all_resource_classes, reachable_resources


def test_tree_reaches_states_by_attribute(config: Configuration) -> None:
    v2 = V2Namespace(config)
    assert isinstance(v2.workspaces.projects.states, States)
    assert isinstance(v2.workspaces.projects.labels, Labels)


def test_locators_are_gone(config: Configuration) -> None:
    v2 = V2Namespace(config)
    assert not hasattr(v2, "workspace")


def test_namespace_exposes_exactly_the_expected_attributes(config: Configuration) -> None:
    """No flat resource attributes survive on `V2Namespace` -- everything but
    `users`/`user_assets` is reached through `workspaces`."""
    v2 = V2Namespace(config)
    assert set(vars(v2).keys()) == {"transport", "users", "user_assets", "workspaces"}


@responses.activate
def test_labels_list_filters_reach_the_query_string(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.projects.labels.list("acme", "ENG", name="bug")

    assert "name=bug" in responses.calls[0].request.url


def test_constructing_the_tree_makes_no_request(config: Configuration) -> None:
    with responses.RequestsMock():  # fails the test if any HTTP call happens
        V2Namespace(config)


@responses.activate
def test_workspaces_retrieve(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/",
        json={"id": "w1", "slug": "acme", "name": "Acme Corp"},
    )

    workspace = V2Namespace(config).workspaces.retrieve("acme")

    assert workspace.slug == "acme"


# -- Nothing is pending any more --------------------------------------------------
# Every `V2Resource` subclass in the package is migrated *and* wired now, so the
# placeholder mechanism that used to stand in for an unwired branch
# (`PendingMigration`, `plane/api/v2/_kernel/pending.py`) is gone rather than idle --
# proved by `test_no_placeholders_remain` and
# `test_the_pending_migration_mechanism_is_deleted` below.


@responses.activate
def test_a_catalog_sibling_next_to_a_family_still_works(config: Configuration) -> None:
    """`releases.labels` is the workspace-level catalog reached as `Releases`'
    sibling -- attaching more children next to it must not take it down."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.releases.labels.list("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/"
    )


@responses.activate
def test_releases_own_crud_and_all_five_children_are_reachable(config: Configuration) -> None:
    """`Releases` and its full family (`labels`, `comments`, `links`, `changelog`,
    `work_items`) are migrated now -- none of them raise `NotImplementedError` any
    more. `tags` is deliberately not among them: see
    `test_release_tags_is_a_workspace_catalog_not_a_release_child` below."""
    base = "https://api.example.com/api/v2/workspaces/acme/releases"
    responses.get(f"{base}/", json={"data": [], "pagination": {"style": "offset"}})
    responses.get(f"{base}/r1/", json={"id": "r1"})
    responses.get(f"{base}/r1/comments/", json={"data": [], "pagination": {"style": "offset"}})
    responses.get(f"{base}/r1/links/", json={"data": [], "pagination": {"style": "offset"}})
    responses.get(f"{base}/r1/changelog/", json={"id": "chg-1"})
    responses.post(f"{base}/r1/work-items/", json={"added": ["w1"], "removed": []})

    v2 = V2Namespace(config)
    v2.workspaces.releases.list("acme")
    v2.workspaces.releases.retrieve("acme", "r1")
    v2.workspaces.releases.comments.list("acme", "r1")
    v2.workspaces.releases.links.list("acme", "r1")
    v2.workspaces.releases.changelog.retrieve("acme", "r1")
    v2.workspaces.releases.work_items.add("acme", "r1", ["w1"])

    assert len(responses.calls) == 6


@responses.activate
def test_a_fetched_release_reaches_its_children_with_no_ids_repeated(
    config: Configuration,
) -> None:
    base = "https://api.example.com/api/v2/workspaces/acme/releases"
    responses.get(f"{base}/r1/", json={"id": "r1", "name": "v1.0"})
    responses.get(f"{base}/r1/comments/", json={"data": [], "pagination": {"style": "offset"}})

    release = V2Namespace(config).workspaces.releases.retrieve("acme", "r1")
    release.comments.list()

    assert responses.calls[1].request.url == f"{base}/r1/comments/"


@responses.activate
def test_wiki_collections_is_the_real_resource_now(config: Configuration) -> None:
    """`wiki.collections` was a `PendingMigration` placeholder for two plans -- present
    so it did not read like a typo, but raising on use. It is the real `Collections`."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/collections/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.wiki.collections.list("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/collections/"
    )


def test_no_placeholders_remain(config: Configuration) -> None:
    """Walk the whole live tree and refuse any placeholder standing in for a resource.

    Written against the *name* rather than the class because the class no longer
    exists: this task deleted `plane/api/v2/_kernel/pending.py` once its last user
    (`wiki.collections`) became real. Anything reintroducing the mechanism -- under
    that name or wired at a fresh branch -- fails here."""
    seen: set[int] = set()

    def walk(node: object, path: str) -> None:
        for name in dir(node):
            if name.startswith("_"):
                continue
            value = getattr(node, name, None)
            assert type(value).__name__ != "PendingMigration", f"{path}.{name} is a placeholder"
        for name, child in vars(node).items():
            if name.startswith("_") or name == "transport" or id(child) in seen:
                continue
            seen.add(id(child))
            if type(child).__module__.startswith("plane.api.v2"):
                walk(child, f"{path}.{name}")

    walk(V2Namespace(config), "v2")


def test_the_pending_migration_mechanism_is_deleted() -> None:
    """A mechanism for tracking unfinished work must not outlive the work. The walk
    above only proves no *instance* is wired; this proves the module is gone, so a
    later plan cannot quietly reach for it instead of finishing a migration."""
    assert importlib.util.find_spec("plane.api.v2._kernel.pending") is None


def test_every_resource_class_is_reachable_from_the_namespace(config: Configuration) -> None:
    """The point of this task, stated once: every `V2Resource` subclass in the package
    is reachable by plain attribute access from `client.v2`. Direct import used to be
    the only way into the families migrated by this plan."""
    unreachable = sorted(
        cls.__name__ for cls in all_resource_classes() if cls not in reachable_resources()
    )

    assert unreachable == [], (
        "these resource classes exist but nothing on the tree reaches them, so only a "
        f"direct import can use them: {unreachable}"
    )


# -- Task 5: wiring the migrated resources onto the tree ---------------------------


# Single source of truth for every resource this task attached to the tree: one row
# per attachment, not a bare `hasattr`. `hasattr` passes even when an attribute is
# wired to the wrong class -- checking `isinstance` plus the exact collection URL
# for a known slug is what actually catches that. Plans 3 and 4 will attach roughly
# 59 more resources the same way -- add a row here, not a new pattern, when they do,
# or `test_the_attachment_table_covers_every_attachment` below fails by name.
# `expected_url` is `None` only for `group_sync` itself: it is a grouping node like
# `Wiki` (see `plane/api/v2/wiki_node.py`), with no `path` of its own -- its three
# children each get their own row with a real URL instead.
WORKSPACE_TREE_ATTACHMENTS = [
    ("artifacts", lambda ws: ws.artifacts, Artifacts, "/workspaces/acme/artifacts/"),
    ("assets", lambda ws: ws.assets, WorkspaceAssets, "/workspaces/acme/assets/"),
    ("audit_logs", lambda ws: ws.audit_logs, AuditLogs, "/workspaces/acme/audit-logs/"),
    (
        "customer_properties",
        lambda ws: ws.customer_properties,
        CustomerProperties,
        "/workspaces/acme/customer-properties/",
    ),
    ("group_sync", lambda ws: ws.group_sync, GroupSync, None),
    ("invitations", lambda ws: ws.invitations, Invitations, "/workspaces/acme/invitations/"),
    ("members", lambda ws: ws.members, WorkspaceMembers, "/workspaces/acme/members/"),
    (
        "permission_schemes",
        lambda ws: ws.permission_schemes,
        PermissionSchemes,
        "/workspaces/acme/permission-schemes/",
    ),
    (
        "permissions",
        lambda ws: ws.permissions,
        WorkspacePermissions,
        "/workspaces/acme/permissions/me/",
    ),
    ("roles", lambda ws: ws.roles, Roles, "/workspaces/acme/roles/"),
    ("stickies", lambda ws: ws.stickies, Stickies, "/workspaces/acme/stickies/"),
    ("teamspaces", lambda ws: ws.teamspaces, Teamspaces, "/workspaces/acme/teamspaces/"),
    ("views", lambda ws: ws.views, WorkspaceViews, "/workspaces/acme/views/"),
    (
        "work_item_relation_definitions",
        lambda ws: ws.work_item_relation_definitions,
        WorkItemRelationDefinitions,
        "/workspaces/acme/work-item-relation-definitions/",
    ),
    (
        "work_item_templates",
        lambda ws: ws.work_item_templates,
        WorkspaceWorkItemTemplates,
        "/workspaces/acme/work-item-templates/",
    ),
    ("work_items", lambda ws: ws.work_items, WorkspaceWorkItems, "/workspaces/acme/work-items/"),
    (
        "group_sync.config",
        lambda ws: ws.group_sync.config,
        GroupSyncConfigResource,
        "/workspaces/acme/group-sync/config/",
    ),
    (
        "group_sync.project_mappings",
        lambda ws: ws.group_sync.project_mappings,
        GroupSyncProjectMappings,
        "/workspaces/acme/group-sync/project-mappings/",
    ),
    (
        "group_sync.workspace_mappings",
        lambda ws: ws.group_sync.workspace_mappings,
        GroupSyncWorkspaceMappings,
        "/workspaces/acme/group-sync/workspace-mappings/",
    ),
    (
        "release_tags",
        lambda ws: ws.release_tags,
        ReleaseTags,
        "/workspaces/acme/releases/tags/",
    ),
    ("webhooks", lambda ws: ws.webhooks, Webhooks, "/workspaces/acme/webhooks/"),
    (
        "webhooks.logs",
        lambda ws: ws.webhooks.logs,
        WebhookLogs,
        None,  # its collection URL carries the webhook id -- see the test below
    ),
    # -- Task 6: the last five workspace families, plus wiki collections -----------
    # `expected_url` is `None` wherever the child's own URL carries an id of its own
    # (a customer, an initiative, an automation, a property, a type, a collection);
    # `test_the_newly_attached_workspace_children_reach_their_urls` fills those in.
    ("customers", lambda ws: ws.customers, Customers, "/workspaces/acme/customers/"),
    ("customers.requests", lambda ws: ws.customers.requests, CustomerRequests, None),
    (
        "customers.property_values",
        lambda ws: ws.customers.property_values,
        CustomerPropertyValues,
        None,
    ),
    ("customers.work_items", lambda ws: ws.customers.work_items, CustomerWorkItems, None),
    ("initiatives", lambda ws: ws.initiatives, Initiatives, "/workspaces/acme/initiatives/"),
    (
        "initiatives.labels",
        lambda ws: ws.initiatives.labels,
        InitiativeLabels,
        "/workspaces/acme/initiatives/labels/",  # a workspace-wide catalog, like release labels
    ),
    ("initiatives.projects", lambda ws: ws.initiatives.projects, InitiativeProjects, None),
    ("initiatives.work_items", lambda ws: ws.initiatives.work_items, InitiativeWorkItems, None),
    (
        "automations",
        lambda ws: ws.automations,
        WorkspaceAutomations,
        "/workspaces/acme/automations/",
    ),
    ("automations.edges", lambda ws: ws.automations.edges, WorkspaceAutomationEdges, None),
    ("automations.nodes", lambda ws: ws.automations.nodes, WorkspaceAutomationNodes, None),
    (
        "automations.activities",
        lambda ws: ws.automations.activities,
        WorkspaceAutomationActivities,
        None,
    ),
    (
        "work_item_properties",
        lambda ws: ws.work_item_properties,
        WorkspaceWorkItemProperties,
        "/workspaces/acme/work-item-properties/",
    ),
    (
        "work_item_properties.contexts",
        lambda ws: ws.work_item_properties.contexts,
        WorkItemPropertyContexts,
        None,
    ),
    (
        "work_item_properties.options",
        lambda ws: ws.work_item_properties.options,
        WorkspaceWorkItemPropertyOptions,
        None,
    ),
    (
        "work_item_types",
        lambda ws: ws.work_item_types,
        WorkspaceWorkItemTypes,
        "/workspaces/acme/work-item-types/",
    ),
    (
        "work_item_types.properties",
        lambda ws: ws.work_item_types.properties,
        WorkspaceWorkItemTypeProperties,
        None,
    ),
    # `wiki` is a grouping node with no path id of its own, so its subtree is tabled
    # here rather than in a third table -- the same way `group_sync`'s children are.
    (
        "wiki.collections",
        lambda ws: ws.wiki.collections,
        Collections,
        "/workspaces/acme/collections/",
    ),
    ("wiki.collections.members", lambda ws: ws.wiki.collections.members, CollectionMembers, None),
    ("wiki.collections.pages", lambda ws: ws.wiki.collections.pages, CollectionPages, None),
]


# The four attributes `Workspaces` already had before this batch: `projects` and `wiki`
# carry their own subtrees (covered by the tests above and by `test_loaded_project.py`),
# `features` is the singleton exemplar, `releases` is wired only for the sake of its
# migrated `labels` child (which does have a row).
PRE_EXISTING_WORKSPACE_ATTRIBUTES = {"projects", "wiki", "features", "releases"}


def test_the_attachment_table_covers_every_attachment(config: Configuration) -> None:
    """The rows above each prove their own attachment, but nothing proved the table was
    *complete* -- a later plan could attach a resource, forget the row and stay green,
    which is exactly how this batch's path-id violations went unnoticed. Comparing the
    table against the live attribute set closes that: attach without a row and this
    fails by name."""
    attached = set(vars(V2Namespace(config).workspaces)) - {"transport"}
    tabled = {name for name, *_ in WORKSPACE_TREE_ATTACHMENTS if "." not in name}

    assert attached - PRE_EXISTING_WORKSPACE_ATTRIBUTES == tabled, (
        "every attribute on `client.v2.workspaces` needs a row in "
        "WORKSPACE_TREE_ATTACHMENTS (or, for the four that predate this batch, a name in "
        "PRE_EXISTING_WORKSPACE_ATTRIBUTES). Missing rows: "
        f"{sorted(attached - PRE_EXISTING_WORKSPACE_ATTRIBUTES - tabled)}; rows with no "
        f"attachment: {sorted(tabled - attached)}."
    )


@pytest.mark.parametrize(
    ("name", "getter", "expected_class", "expected_url"),
    WORKSPACE_TREE_ATTACHMENTS,
    ids=[row[0] for row in WORKSPACE_TREE_ATTACHMENTS],
)
def test_workspace_tree_attachment_is_the_right_class_at_the_right_url(
    config: Configuration, name, getter, expected_class, expected_url
) -> None:
    resource = getter(V2Namespace(config).workspaces)

    assert isinstance(resource, expected_class), f"{name} is not a {expected_class.__name__}"
    if expected_url is not None:
        assert resource._collection_url(slug="acme") == expected_url, name


@responses.activate
def test_a_wired_resource_reaches_its_url(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/teamspaces/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.teamspaces.list("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/teamspaces/"
    )


@responses.activate
def test_permissions_singleton_is_wired_and_reaches_its_url(config: Configuration) -> None:
    """`.permissions` has no primary key of its own; verify the wired instance is
    the real `WorkspacePermissions`, not just any truthy attribute."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/permissions/me/",
        json={"permissions": []},
    )

    V2Namespace(config).workspaces.permissions.me("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/permissions/me/"
    )


@responses.activate
def test_group_sync_project_mappings_child_reaches_its_url(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/group-sync/project-mappings/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.group_sync.project_mappings.list("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/group-sync/project-mappings/"
    )


@responses.activate
def test_release_tags_is_a_workspace_catalog_not_a_release_child(
    config: Configuration,
) -> None:
    """`ReleaseTags` attaches to `Workspaces`, not `Releases` -- the reverse of where
    it started.

    Its URL takes one path id (`/workspaces/{slug}/releases/tags/`) and a release
    points at a tag through its own `tag_id` field, so there is no per-release
    association to reach. Hung off `Releases` -- whose rows *are* navigable -- it
    became a `release.tags` navigation property that bound two ids into a
    one-id resource, so every call through it raised. The property existed only to
    satisfy the navigation sweep. Fixing the attachment is what removes the need for
    it; `LoadedRelease` has no `tags` at all now."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    v2 = V2Namespace(config)
    v2.workspaces.release_tags.list("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/"
    )
    assert not hasattr(v2.workspaces.releases, "tags")


# -- Task 6: wiring the project band onto the tree ---------------------------------


# The project-scoped sibling of `WORKSPACE_TREE_ATTACHMENTS`, same shape and same
# completeness assertion. `expected_url` is filled for the workspace `acme` and the
# project `ENG`, so a row that names the wrong class -- or the right class wired at
# the wrong template -- fails rather than passing on a bare `hasattr`. Rows whose
# name contains a `.` are children of a project-band resource (`cycles.work_items`),
# and are excluded from the completeness comparison the same way the workspace table
# excludes `group_sync.config`.
PROJECT_TREE_ATTACHMENTS = [
    ("cycles", lambda p: p.cycles, Cycles, "/workspaces/acme/projects/ENG/cycles/"),
    (
        "milestones",
        lambda p: p.milestones,
        Milestones,
        "/workspaces/acme/projects/ENG/milestones/",
    ),
    ("modules", lambda p: p.modules, Modules, "/workspaces/acme/projects/ENG/modules/"),
    ("estimates", lambda p: p.estimates, Estimates, "/workspaces/acme/projects/ENG/estimates/"),
    ("intakes", lambda p: p.intakes, Intakes, "/workspaces/acme/projects/ENG/intake-issues/"),
    ("members", lambda p: p.members, ProjectMembers, "/workspaces/acme/projects/ENG/members/"),
    ("views", lambda p: p.views, ProjectViews, "/workspaces/acme/projects/ENG/views/"),
    ("features", lambda p: p.features, ProjectFeatures, "/workspaces/acme/projects/ENG/features/"),
    (
        "permissions",
        lambda p: p.permissions,
        ProjectPermissions,
        "/workspaces/acme/projects/ENG/permissions/me/",
    ),
    (
        "work_item_templates",
        lambda p: p.work_item_templates,
        ProjectWorkItemTemplates,
        "/workspaces/acme/projects/ENG/work-item-templates/",
    ),
    (
        "worklogs",
        lambda p: p.worklogs,
        ProjectWorklogs,
        "/workspaces/acme/projects/ENG/worklogs/summary/",
    ),
    ("pages", lambda p: p.pages, ProjectPages, "/workspaces/acme/projects/ENG/pages/"),
    (
        "cycles.work_items",
        lambda p: p.cycles.work_items,
        CycleWorkItems,
        None,  # needs a cycle id too; `test_cycle_work_items_bridge_url` covers it
    ),
    (
        "milestones.work_items",
        lambda p: p.milestones.work_items,
        MilestoneWorkItems,
        None,
    ),
    ("modules.work_items", lambda p: p.modules.work_items, ModuleWorkItems, None),
    ("estimates.points", lambda p: p.estimates.points, EstimatePoints, None),
    # -- Task 6: the last four project-band families ------------------------------
    (
        "automations",
        lambda p: p.automations,
        ProjectAutomations,
        "/workspaces/acme/projects/ENG/automations/",
    ),
    ("automations.edges", lambda p: p.automations.edges, ProjectAutomationEdges, None),
    ("automations.nodes", lambda p: p.automations.nodes, ProjectAutomationNodes, None),
    (
        "automations.activities",
        lambda p: p.automations.activities,
        ProjectAutomationActivities,
        None,
    ),
    (
        "work_item_types",
        lambda p: p.work_item_types,
        WorkItemTypes,
        "/workspaces/acme/projects/ENG/work-item-types/",
    ),
    (
        "work_item_types.properties",
        lambda p: p.work_item_types.properties,
        WorkItemTypeProperties,
        None,
    ),
    (
        "work_item_properties",
        lambda p: p.work_item_properties,
        WorkItemProperties,
        "/workspaces/acme/projects/ENG/work-item-properties/",
    ),
    (
        "work_item_properties.options",
        lambda p: p.work_item_properties.options,
        WorkItemPropertyOptions,
        None,
    ),
    ("workflows", lambda p: p.workflows, Workflows, "/workspaces/acme/projects/ENG/workflows/"),
    ("workflows.states", lambda p: p.workflows.states, WorkflowStates, None),
    ("workflows.transitions", lambda p: p.workflows.transitions, WorkflowTransitions, None),
]


# The three attributes `Projects` already had before this batch: `states` and `labels`
# are covered by `test_tree_reaches_states_by_attribute`, and `work_items` carries its
# own subtree (`tests/v2/test_work_items_resource.py`).
PRE_EXISTING_PROJECT_ATTRIBUTES = {"states", "labels", "work_items"}


def test_the_project_attachment_table_covers_every_attachment(config: Configuration) -> None:
    """The project-band twin of `test_the_attachment_table_covers_every_attachment`:
    attach a resource in `Projects.__init__` and forget its row here, and this fails
    by name instead of quietly leaving the resource unproven."""
    attached = set(vars(V2Namespace(config).workspaces.projects)) - {"transport"}
    tabled = {name for name, *_ in PROJECT_TREE_ATTACHMENTS if "." not in name}

    assert attached - PRE_EXISTING_PROJECT_ATTRIBUTES == tabled, (
        "every attribute on `client.v2.workspaces.projects` needs a row in "
        "PROJECT_TREE_ATTACHMENTS (or, for the three that predate this batch, a name "
        "in PRE_EXISTING_PROJECT_ATTRIBUTES). Missing rows: "
        f"{sorted(attached - PRE_EXISTING_PROJECT_ATTRIBUTES - tabled)}; rows with no "
        f"attachment: {sorted(tabled - attached)}."
    )


@pytest.mark.parametrize(
    ("name", "getter", "expected_class", "expected_url"),
    PROJECT_TREE_ATTACHMENTS,
    ids=[row[0] for row in PROJECT_TREE_ATTACHMENTS],
)
def test_project_tree_attachment_is_the_right_class_at_the_right_url(
    config: Configuration, name, getter, expected_class, expected_url
) -> None:
    resource = getter(V2Namespace(config).workspaces.projects)

    assert isinstance(resource, expected_class), f"{name} is not a {expected_class.__name__}"
    if expected_url is not None:
        assert resource._collection_url(slug="acme", project_id="ENG") == expected_url, name


def test_the_newly_attached_workspace_children_reach_their_urls(config: Configuration) -> None:
    """The workspace rows above whose `expected_url` is `None`: their templates carry
    an id of their own, so the URL is proved here with that id supplied. Without this
    a wrongly-templated child would pass on the `isinstance` half of its row alone."""
    ws = V2Namespace(config).workspaces

    assert (
        ws.customers.requests._collection_url(slug="acme", customer_id="c1")
        == "/workspaces/acme/customers/c1/requests/"
    )
    assert (
        ws.customers.property_values._collection_url(slug="acme", customer_id="c1")
        == "/workspaces/acme/customers/c1/property-values/"
    )
    assert (
        ws.customers.work_items._collection_url(slug="acme", customer_id="c1")
        == "/workspaces/acme/customers/c1/work-items/"
    )
    assert (
        ws.initiatives.projects._collection_url(slug="acme", initiative_id="i1")
        == "/workspaces/acme/initiatives/i1/projects/"
    )
    assert (
        ws.initiatives.work_items._collection_url(slug="acme", initiative_id="i1")
        == "/workspaces/acme/initiatives/i1/work-items/"
    )
    assert (
        ws.automations.edges._collection_url(slug="acme", automation_id="a1")
        == "/workspaces/acme/automations/a1/edges/"
    )
    assert (
        ws.automations.nodes._collection_url(slug="acme", automation_id="a1")
        == "/workspaces/acme/automations/a1/nodes/"
    )
    assert (
        ws.automations.activities._collection_url(slug="acme", automation_id="a1")
        == "/workspaces/acme/automations/a1/activities/"
    )
    assert (
        ws.work_item_properties.contexts._collection_url(slug="acme", property_id="p1")
        == "/workspaces/acme/work-item-properties/p1/contexts/"
    )
    assert (
        ws.work_item_properties.options._collection_url(slug="acme", property_id="p1")
        == "/workspaces/acme/work-item-properties/p1/options/"
    )
    assert (
        ws.work_item_types.properties._collection_url(slug="acme", type_id="t1")
        == "/workspaces/acme/work-item-types/t1/properties/"
    )
    assert (
        ws.wiki.collections.members._collection_url(slug="acme", collection_id="col1")
        == "/workspaces/acme/collections/col1/members/"
    )


def test_the_newly_attached_project_children_reach_their_urls(config: Configuration) -> None:
    """The project-band twin of the check above."""
    projects = V2Namespace(config).workspaces.projects
    ids = {"slug": "acme", "project_id": "ENG"}

    assert (
        projects.automations.edges._collection_url(**ids, automation_id="a1")
        == "/workspaces/acme/projects/ENG/automations/a1/edges/"
    )
    assert (
        projects.automations.nodes._collection_url(**ids, automation_id="a1")
        == "/workspaces/acme/projects/ENG/automations/a1/nodes/"
    )
    assert (
        projects.automations.activities._collection_url(**ids, automation_id="a1")
        == "/workspaces/acme/projects/ENG/automations/a1/activities/"
    )
    assert (
        projects.work_item_types.properties._collection_url(**ids, type_id="t1")
        == "/workspaces/acme/projects/ENG/work-item-types/t1/properties/"
    )
    assert (
        projects.work_item_properties.options._collection_url(**ids, property_id="p1")
        == "/workspaces/acme/projects/ENG/work-item-properties/p1/options/"
    )
    assert (
        projects.workflows.states._collection_url(**ids, workflow_id="wf1")
        == "/workspaces/acme/projects/ENG/workflows/wf1/states/"
    )
    assert (
        projects.workflows.transitions._collection_url(**ids, workflow_id="wf1")
        == "/workspaces/acme/projects/ENG/workflows/wf1/state-transitions/"
    )


def test_cycle_work_items_bridge_url(config: Configuration) -> None:
    """The four project-band children take an extra id of their own, so their rows
    above carry no `expected_url` -- proved here instead."""
    projects = V2Namespace(config).workspaces.projects

    assert (
        projects.cycles.work_items._collection_url(slug="acme", project_id="ENG", cycle_id="c1")
        == "/workspaces/acme/projects/ENG/cycles/c1/work-items/"
    )
    assert (
        projects.estimates.points._collection_url(slug="acme", project_id="ENG", estimate_id="e1")
        == "/workspaces/acme/projects/ENG/estimates/e1/points/"
    )


@responses.activate
def test_a_wired_project_resource_reaches_its_url(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/cycles/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.projects.cycles.list("acme", "ENG")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/cycles/"
    )


@responses.activate
def test_project_pages_is_wired_at_last(config: Configuration) -> None:
    """`ProjectPages` was migrated by an earlier plan but never attached, so nothing
    could reach it; the completeness assertion above now keeps it attached."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/pages/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.projects.pages.list("acme", "ENG")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/pages/"
    )


@responses.activate
def test_webhook_logs_is_reachable_under_the_workspace(config: Configuration) -> None:
    """`Webhooks` carries `logs`, but nothing wired `Webhooks` itself onto the
    workspace, so `webhooks.logs` was unreachable from `client.v2`."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/webhook-logs/wh1/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.webhooks.logs.list("acme", "wh1")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/webhook-logs/wh1/"
    )
