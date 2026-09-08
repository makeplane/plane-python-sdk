import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2.labels import Labels
from plane.api.v2.states import States
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


def test_workspace_exposes_every_migrated_resource(config: Configuration) -> None:
    ws = V2Namespace(config).workspaces
    for name in (
        "artifacts",
        "assets",
        "audit_logs",
        "customer_properties",
        "group_sync",
        "invitations",
        "members",
        "permission_schemes",
        "permissions",
        "roles",
        "stickies",
        "teamspaces",
        "views",
        "work_item_relation_definitions",
        "work_item_templates",
        "work_items",
    ):
        assert hasattr(ws, name), f"workspaces.{name} is not wired"


def test_group_sync_children_are_reachable(config: Configuration) -> None:
    group_sync = V2Namespace(config).workspaces.group_sync
    for name in ("config", "project_mappings", "workspace_mappings"):
        assert hasattr(group_sync, name)


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
