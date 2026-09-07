import responses

from plane.api.v2 import V2Namespace
from plane.config import Configuration


@responses.activate
def test_fetched_project_navigates_to_states_without_repeating_ids(
    config: Configuration,
) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Engineering"},
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={
            "data": [{"id": "s1", "name": "Todo"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")
    page = project.states.list()

    assert project.name == "Engineering"
    assert page.data[0].name == "Todo"


@responses.activate
def test_listed_projects_are_navigable(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={
            "data": [{"id": "p1", "identifier": "ENG", "name": "Engineering"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    page = V2Namespace(config).workspaces.projects.list("acme")
    page.data[0].labels.list()

    assert responses.calls[1].request.url.endswith("/projects/ENG/labels/")


@responses.activate
def test_fetched_project_reaches_a_work_items_comments_two_levels_deep(
    config: Configuration,
) -> None:
    """The design's own showcase chain: `project.work_items.retrieve(...)` must
    itself come back as a `LoadedWorkItem` so `.comments` works with no ids
    repeated at any level."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Engineering"},
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items/ENG-12/",
        json={"id": "w1", "sequence_id": 12},
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items/w1/comments/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")
    project.work_items.retrieve("ENG-12").comments.list()

    assert (
        responses.calls[-1].request.url
        == "https://api.example.com/api/v2/workspaces/acme/projects/ENG/work-items/w1/comments/"
    )
