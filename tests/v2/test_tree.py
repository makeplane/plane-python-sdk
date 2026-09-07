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
