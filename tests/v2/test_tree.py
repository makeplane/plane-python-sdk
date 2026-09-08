import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2.artifacts import Artifacts
from plane.api.v2.assets import WorkspaceAssets
from plane.api.v2.audit_logs import AuditLogs
from plane.api.v2.customer_properties import CustomerProperties
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
from plane.api.v2.work_item_relation_definitions import WorkItemRelationDefinitions
from plane.api.v2.work_item_templates import WorkspaceWorkItemTemplates
from plane.api.v2.work_item_templates.project import ProjectWorkItemTemplates
from plane.api.v2.work_items import WorkspaceWorkItems
from plane.api.v2.worklogs import ProjectWorklogs
from plane.config import Configuration


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


# -- Wired but not yet migrated ---------------------------------------------------
# `Workspaces` wires `Releases`, and `Releases` is now fully migrated -- its own
# CRUD plus all six children (`labels`, `tags`, `comments`, `links`, `changelog`,
# `work_items`) accept the leading path ids their URLs need. `wiki.collections` is
# the one branch still a placeholder: `Collections` was migrated to the flat shape
# by an earlier plan, but wiring it onto `Wiki` is separate follow-on work -- see
# `plane/api/v2/wiki_node.py`.
# (`WorkItems`' own seven children are all migrated now -- see
# `tests/v2/test_work_items_resource.py`.)


@pytest.mark.parametrize(
    ("reach", "expected"),
    [
        (lambda v2: v2.workspaces.wiki.collections.list(), "Collections"),
    ],
)
def test_unmigrated_branches_name_themselves_instead_of_raising_keyerror(
    config: Configuration, reach, expected: str
) -> None:
    with pytest.raises(NotImplementedError) as raised:
        reach(V2Namespace(config))

    message = str(raised.value)
    assert expected in message
    assert "not migrated to the flat v2 shape yet" in message


@responses.activate
def test_the_migrated_sibling_on_an_unmigrated_branch_still_works(config: Configuration) -> None:
    """`releases.labels` is why `Releases` is wired at all -- placeholders next to it
    must not take it down."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.releases.labels.list("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/releases/labels/"
    )


@responses.activate
def test_releases_own_crud_and_all_six_children_are_reachable(config: Configuration) -> None:
    """`Releases` and its full family (`labels`, `tags`, `comments`, `links`,
    `changelog`, `work_items`) are migrated now -- none of them raise
    `NotImplementedError` any more."""
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


def test_wiki_collections_is_present_rather_than_a_bare_attribute_error(
    config: Configuration,
) -> None:
    """Leaving the attribute off gave `AttributeError`, which reads like a typo."""
    assert hasattr(V2Namespace(config).workspaces.wiki, "collections")


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
    ("releases.tags", lambda ws: ws.releases.tags, ReleaseTags, "/workspaces/acme/releases/tags/"),
    ("webhooks", lambda ws: ws.webhooks, Webhooks, "/workspaces/acme/webhooks/"),
    (
        "webhooks.logs",
        lambda ws: ws.webhooks.logs,
        WebhookLogs,
        None,  # its collection URL carries the webhook id -- see the test below
    ),
]


# The four attributes `Workspaces` already had before this batch: `projects` and `wiki`
# carry their own subtrees (covered by the tests above and by `test_loaded_project.py`),
# `features` is the singleton exemplar, `releases` is wired only for the sake of its
# migrated `labels`/`tags` children (which do have rows).
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
def test_release_tags_is_wired_onto_releases_not_workspaces(config: Configuration) -> None:
    """`ReleaseTags` attaches to `Releases`, not `Workspaces` -- the other four
    release placeholders (comments, links, changelog, work_items) stay pending."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    V2Namespace(config).workspaces.releases.tags.list("acme")

    assert responses.calls[0].request.url.startswith(
        "https://api.example.com/api/v2/workspaces/acme/releases/tags/"
    )


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
