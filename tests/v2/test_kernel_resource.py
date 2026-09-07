import pytest
import responses

from plane.api.v2._kernel.errors import MissingPathId
from plane.api.v2._kernel.loaded import Loaded, LoadsNavigableRows
from plane.api.v2._kernel.resource import V2Resource
from plane.api.v2._kernel.transport import V2Transport
from plane.config import Configuration
from plane.models.v2.states import State


class _Probe(V2Resource[State, State, State]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = State
    operations = {"list": "states_list"}

    def list(self, slug: str, project: str | None = None) -> object:
        """Deliberately lets `project` be omitted, to reach the kernel with a path
        id missing the way an unmigrated resource does."""
        return self._list(slug=slug, **({} if project is None else {"project_id": project}))


@pytest.fixture
def probe(config: Configuration) -> _Probe:
    return _Probe(V2Transport(config))


def test_constructor_takes_only_transport(config: Configuration) -> None:
    with pytest.raises(TypeError):
        _Probe(V2Transport(config), slug="acme")


def test_collection_url_comes_only_from_call_arguments(probe: _Probe) -> None:
    url = probe._collection_url(slug="acme", project_id="ENG")
    assert url == "/workspaces/acme/projects/ENG/states/"


def test_missing_path_parameter_names_the_resource_method_and_template(probe: _Probe) -> None:
    """`str.format_map` would raise a bare `KeyError('project_id')`. That is the
    first failure most callers hit -- a leading id forgotten on the flat path, or a
    resource whose flat migration is still pending -- so it is wrapped."""
    with pytest.raises(MissingPathId) as raised:
        probe.list("acme")

    message = str(raised.value)
    assert "_Probe.list()" in message
    assert "'project_id'" in message
    assert "/workspaces/{slug}/projects/{project_id}/states/" in message
    assert "ids supplied: slug" in message


def test_missing_path_parameter_is_raised_from_url_building_too(probe: _Probe) -> None:
    with pytest.raises(MissingPathId, match="project_id"):
        probe._collection_url(slug="acme")


class _Catalog(V2Resource[State, State, State]):
    path = "/workspaces/{slug}/releases/labels/"
    model = State
    operations = {"list": "release_labels_list"}
    extra_paths = {"add": "/workspaces/{slug}/releases/{release_id}/labels/"}


def test_url_for_uses_the_primary_path_by_default(config: Configuration) -> None:
    catalog = _Catalog(V2Transport(config))
    assert catalog.url_for("list", slug="acme") == "/workspaces/acme/releases/labels/"


def test_url_for_uses_the_override_when_declared(config: Configuration) -> None:
    catalog = _Catalog(V2Transport(config))
    url = catalog.url_for("add", slug="acme", release_id="r1")
    assert url == "/workspaces/acme/releases/r1/labels/"


class _Stale(V2Resource[State, State, State]):
    """A throwaway subclass still declaring the retired `bridge_path` -- exercises
    `url_for`'s call-time guard. Does not rely on the three real classes that used to
    declare this, since they no longer do."""

    path = "/workspaces/{slug}/things/"
    model = State
    operations = {}
    bridge_path = "/workspaces/{slug}/things/{thing_id}/labels/"


def test_url_for_raises_for_a_subclass_still_declaring_bridge_path(
    config: Configuration,
) -> None:
    stale = _Stale(V2Transport(config))
    with pytest.raises(TypeError, match="extra_paths"):
        stale.url_for("add", slug="acme", thing_id="t1")


# -- Promoted machinery -----------------------------------------------------------
# `_load`/`_load_page`, the singleton GET/PATCH pair and the 204 POST were each
# hand-written per resource. They live on the kernel now, so they are exercised here
# once rather than in every resource's own tests.


class _LoadedState(Loaded, State):
    model_config = {**State.model_config, "arbitrary_types_allowed": True}


class _Navigable(V2Resource[State, State, State], LoadsNavigableRows[_LoadedState]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = State
    operations = {"list": "states_list", "retrieve": "states_retrieve"}
    loaded_model = _LoadedState
    loaded_names = ("slug", "project", "state")


@responses.activate
def test_load_page_keeps_the_envelope_and_loads_every_row(config: Configuration) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/",
        json={
            "data": [{"id": "s1", "name": "Todo"}, {"id": "s2", "name": "Done"}],
            "pagination": {"style": "offset"},
            "total_count": 2,
            "next": 2,
        },
    )
    navigable = _Navigable(V2Transport(config))

    page = navigable._load_page(
        navigable._list(slug="acme", project_id="ENG"), "acme", "ENG", fields=None
    )

    assert page.total_count == 2
    assert page.next == 2
    assert [row.id for row in page.data] == ["s1", "s2"]
    assert page.data[0]._ids == ("acme", "ENG", "s1")
    assert page.data[0]._id_names == ("slug", "project", "state")


class _ForgotLoadedModel(V2Resource[State, State, State], LoadsNavigableRows[_LoadedState]):
    """Mixes the loading machinery in but never says what to load rows into."""

    path = "/workspaces/{slug}/states/"
    model = State
    operations = {}


def test_load_refuses_a_resource_that_declares_no_loaded_model(config: Configuration) -> None:
    with pytest.raises(TypeError, match="no `loaded_model`"):
        _ForgotLoadedModel(V2Transport(config))._load(State(id="s1"), "acme")


class _Singleton(V2Resource[State, State, State]):
    """A row that *is* its collection -- no pk in the URL."""

    path = "/workspaces/{slug}/features/"
    model = State
    operations = {"get": "states_list", "update": "states_list"}


@responses.activate
def test_singleton_get_and_update_hit_the_bare_collection_url(config: Configuration) -> None:
    responses.get("https://api.example.com/api/v2/workspaces/acme/features/", json={"id": "f1"})
    responses.patch("https://api.example.com/api/v2/workspaces/acme/features/", json={"id": "f1"})
    singleton = _Singleton(V2Transport(config))

    assert singleton._retrieve_singleton(action="get", slug="acme").id == "f1"
    assert singleton._update_singleton(State(id="f1"), action="update", slug="acme").id == "f1"

    assert [call.request.method for call in responses.calls] == ["GET", "PATCH"]
    for call in responses.calls:
        assert call.request.url.endswith("/workspaces/acme/features/")


@responses.activate
def test_void_action_posts_to_the_sub_path_and_returns_none(probe: _Probe) -> None:
    responses.post(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/states/s1/archive/",
        status=204,
    )

    assert probe._void_action("archive", pk="s1", slug="acme", project_id="ENG") is None
    assert responses.calls[0].request.url.endswith("/states/s1/archive/")
