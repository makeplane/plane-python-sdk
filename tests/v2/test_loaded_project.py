import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2._kernel.errors import FieldNotRequested
from plane.config import Configuration
from plane.models.v2.projects import UpdateProject


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


# -- `fields=` must reach `Loaded.build`, not just `Loaded` unit tests -----------
# (regression: `_load` forgot to forward it, so every field read as `None`
# instead of raising for a field never requested from a sparse response)


@responses.activate
def test_retrieve_with_fields_raises_on_an_unrequested_field(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1"},
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG", fields=["id"])

    assert len(project._present) == 1
    with pytest.raises(FieldNotRequested, match="name"):
        _ = project.name


@responses.activate
def test_list_with_fields_raises_on_an_unrequested_field_for_a_page_row(
    config: Configuration,
) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={"data": [{"id": "p1"}], "pagination": {"style": "offset"}, "total_count": 1},
    )

    page = V2Namespace(config).workspaces.projects.list("acme", fields=["id"])
    row = page.data[0]

    assert len(row._present) == 1
    with pytest.raises(FieldNotRequested, match="name"):
        _ = row.name


@responses.activate
def test_retrieve_with_a_comma_joined_fields_string_reads_normally(
    config: Configuration,
) -> None:
    """`fields="id,name"` is the same request as `fields=["id", "name"]`
    (`encode_fields` accepts both); `Loaded.build` must normalise it the same way
    instead of iterating the string character by character, which marked every
    real field name absent."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "name": "Engineering"},
    )

    project = V2Namespace(config).workspaces.projects.retrieve(
        "acme", "ENG", fields="id,name"  # type: ignore[arg-type]
    )

    assert project.name == "Engineering"
    with pytest.raises(FieldNotRequested, match="identifier"):
        _ = project.identifier


@responses.activate
def test_retrieve_with_fields_reads_a_requested_but_null_field_as_none(
    config: Configuration,
) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "name": None},
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG", fields=["id", "name"])

    assert project.name is None


# -- `iterate`/`update`/`upsert` must return navigable rows too, like `retrieve`/
# `create`/`list` -- a caller who switches from `list` to `iterate` to page
# through results must not silently lose navigation.


@responses.activate
def test_iterate_yields_navigable_rows(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={
            "data": [{"id": "p1", "identifier": "ENG", "name": "Engineering"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    row = next(iter(V2Namespace(config).workspaces.projects.iterate("acme")))
    row.states.list()

    assert responses.calls[-1].request.url.endswith("/projects/ENG/states/")


@responses.activate
def test_iterate_is_lazy_and_costs_exactly_one_request_for_one_row(
    config: Configuration,
) -> None:
    """Two pages on offer, one row taken: an eager implementation would make a second
    request. A single mocked page cannot discriminate."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={
            "data": [{"id": "p1", "identifier": "ENG"}, {"id": "p2", "identifier": "OPS"}],
            "pagination": {"style": "offset"},
            "next": 2,
        },
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={
            "data": [{"id": "p3", "identifier": "MKT"}],
            "pagination": {"style": "offset"},
            "next": None,
        },
    )

    rows = V2Namespace(config).workspaces.projects.iterate("acme")
    first = next(iter(rows))

    assert first.id == "p1"
    assert len(responses.calls) == 1

    assert [row.id for row in rows] == ["p2", "p3"]
    assert len(responses.calls) == 2


@responses.activate
def test_iterate_with_fields_raises_on_an_unrequested_field(config: Configuration) -> None:
    """`fields=` must survive the trip through the generator, not just through `list`."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={"data": [{"id": "p1"}], "pagination": {"style": "offset"}},
    )

    row = next(iter(V2Namespace(config).workspaces.projects.iterate("acme", fields=["id"])))

    assert len(row._present) == 1
    with pytest.raises(FieldNotRequested, match="name"):
        _ = row.name


@responses.activate
def test_update_returns_a_navigable_row(config: Configuration) -> None:
    responses.patch(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Eng Team"},
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/labels/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    project = V2Namespace(config).workspaces.projects.update(
        "acme", "ENG", UpdateProject(name="Eng Team")
    )
    project.labels.list()

    assert project.name == "Eng Team"
    assert responses.calls[-1].request.url.endswith("/projects/ENG/labels/")


# -- Presence follows the *response*, not the request ----------------------------
# (regression: `_present` was derived from the caller's `fields=`, so a partial row
# returned with no `fields=` in play -- which is what collection deferral does --
# marked every field present and read back as a silent `None`.)


@responses.activate
def test_retrieve_with_no_fields_argument_raises_for_a_field_the_server_omitted(
    config: Configuration,
) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG"},
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")

    assert project._present == frozenset({"id", "identifier"})
    with pytest.raises(FieldNotRequested, match="name"):
        _ = project.name


@responses.activate
def test_list_with_no_fields_argument_raises_for_a_deferred_field(
    config: Configuration,
) -> None:
    """Collection deferral: the list route returns a narrower row than the detail
    route even though the caller passed no `fields=`."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={
            "data": [{"id": "p1", "identifier": "ENG", "name": "Engineering"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    row = V2Namespace(config).workspaces.projects.list("acme").data[0]

    assert row.name == "Engineering"
    assert row._present == frozenset({"id", "identifier", "name"})
    with pytest.raises(FieldNotRequested, match="description"):
        _ = row.description


@responses.activate
def test_a_field_the_server_returned_but_the_caller_narrowed_away_stays_hidden(
    config: Configuration,
) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Engineering"},
    )

    project = V2Namespace(config).workspaces.projects.retrieve(
        "acme", "ENG", fields=["id", "identifier"]
    )

    assert project._present == frozenset({"id", "identifier"})
    with pytest.raises(FieldNotRequested, match="name"):
        _ = project.name


@responses.activate
def test_find_by_name_returns_a_navigable_row(config: Configuration) -> None:
    """A lookup that answered with a plain `Project` silently dropped navigation."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/",
        json={
            "data": [{"id": "p1", "identifier": "ENG", "name": "Engineering"}],
            "pagination": {"style": "offset"},
        },
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={"data": [], "pagination": {"style": "offset"}, "total_count": 0},
    )

    project = V2Namespace(config).workspaces.projects.find_by_name("acme", "Engineering")
    project.states.list()

    assert responses.calls[-1].request.url.endswith("/projects/ENG/states/")


# -- A fetched project reaches all fifteen of its children ------------------------
# (regression: `Projects.__init__` attached fifteen resources while `LoadedProject`
# exposed three, so `workspaces.projects.cycles.list(slug, project)` worked and
# `project.cycles.list()` raised `AttributeError`. `tests/v2/test_loaded_navigation.py`
# sweeps the correspondence; these two prove the calls actually reach the wire.)


@responses.activate
def test_fetched_project_reaches_its_cycles(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Engineering"},
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/cycles/",
        json={
            "data": [{"id": "c1", "name": "Sprint 1"}],
            "pagination": {"style": "offset"},
            "total_count": 1,
        },
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")
    page = project.cycles.list()

    assert page.data[0].name == "Sprint 1"
    assert (
        responses.calls[-1].request.url
        == "https://api.example.com/api/v2/workspaces/acme/projects/ENG/cycles/"
    )


@responses.activate
def test_fetched_project_reaches_its_singleton_children(config: Configuration) -> None:
    """`permissions` and `worklogs` have no primary key of their own, so their
    navigation properties bind the project's ids and take nothing further."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Engineering"},
    )
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/permissions/me/",
        json={"permissions": []},
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")
    project.permissions.me()

    assert (
        responses.calls[-1].request.url
        == "https://api.example.com/api/v2/workspaces/acme/projects/ENG/permissions/me/"
    )


@responses.activate
def test_fetched_project_reaches_a_cycle_row_that_reaches_its_own_work_items(
    config: Configuration,
) -> None:
    """Two levels through the new properties: `project.cycles.retrieve(...)` must
    itself come back loaded, so the cycle reaches `.work_items` with no ids repeated."""
    base = "https://api.example.com/api/v2/workspaces/acme/projects/ENG"
    responses.get(f"{base}/", json={"id": "p1", "identifier": "ENG"})
    responses.get(f"{base}/cycles/c1/", json={"id": "c1", "name": "Sprint 1"})
    responses.post(f"{base}/cycles/c1/work-items/", json={"added": ["w1"]})

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")
    added = project.cycles.retrieve("c1").work_items.add(["w1"])

    assert added == ["w1"]
    assert responses.calls[-1].request.url == f"{base}/cycles/c1/work-items/"
