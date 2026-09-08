import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2.artifacts import Artifacts
from plane.api.v2.assets import WorkspaceAssets
from plane.api.v2.audit_logs import AuditLogs
from plane.api.v2.customer_properties import CustomerProperties
from plane.api.v2.group_sync import (
    GroupSync,
    GroupSyncConfigResource,
    GroupSyncProjectMappings,
    GroupSyncWorkspaceMappings,
)
from plane.api.v2.invitations import Invitations
from plane.api.v2.labels import Labels
from plane.api.v2.members import WorkspaceMembers
from plane.api.v2.permission_schemes import PermissionSchemes
from plane.api.v2.permissions import WorkspacePermissions
from plane.api.v2.releases.tags import ReleaseTags
from plane.api.v2.roles import Roles
from plane.api.v2.states import States
from plane.api.v2.stickies import Stickies
from plane.api.v2.teamspaces import Teamspaces
from plane.api.v2.views import WorkspaceViews
from plane.api.v2.work_item_relation_definitions import WorkItemRelationDefinitions
from plane.api.v2.work_item_templates import WorkspaceWorkItemTemplates
from plane.api.v2.work_items import WorkspaceWorkItems
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
# `Workspaces` wires `Releases` for the sake of `releases.labels`, and `WorkItems`
# wires seven children of which one is migrated. Everything else on those branches
# used to fail with a bare `KeyError: 'slug'` from inside the kernel; each now says
# what it is and that migration is pending.


@pytest.mark.parametrize(
    ("reach", "expected"),
    [
        (lambda v2: v2.workspaces.releases.list(), "Releases.list()"),
        (lambda v2: v2.workspaces.releases.retrieve("r1"), "Releases.retrieve()"),
        (lambda v2: v2.workspaces.releases.comments.list(), "ReleaseComments"),
        (lambda v2: v2.workspaces.releases.links.list(), "ReleaseLinks"),
        (lambda v2: v2.workspaces.releases.changelog.retrieve("r1"), "ReleaseChangelogResource"),
        (lambda v2: v2.workspaces.releases.work_items.add("r1", ["w1"]), "ReleaseWorkItems"),
        (lambda v2: v2.workspaces.projects.work_items.activities.list("wi1"), "WorkItemActivities"),
        (
            lambda v2: v2.workspaces.projects.work_items.attachments.list("wi1"),
            "WorkItemAttachments",
        ),
        (lambda v2: v2.workspaces.projects.work_items.links.list("wi1"), "WorkItemLinks"),
        (lambda v2: v2.workspaces.projects.work_items.worklogs.list("wi1"), "WorkItemWorklogs"),
        (lambda v2: v2.workspaces.projects.work_items.relations.list("wi1"), "WorkItemRelations"),
        (
            lambda v2: v2.workspaces.projects.work_items.dependencies.list("wi1"),
            "WorkItemDependencies",
        ),
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
# 58 more resources the same way -- add a row here, not a new pattern, when they do.
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
]


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
