import pytest

from plane.api.v2._kernel.resource import V2Resource
from plane.api.v2._kernel.transport import V2Transport
from plane.config import Configuration
from plane.models.v2.states import State


class _Probe(V2Resource[State, State, State]):
    path = "/workspaces/{slug}/projects/{project_id}/states/"
    model = State
    operations = {"list": "states_list"}


@pytest.fixture
def probe(config: Configuration) -> _Probe:
    return _Probe(V2Transport(config))


def test_constructor_takes_only_transport(config: Configuration) -> None:
    with pytest.raises(TypeError):
        _Probe(V2Transport(config), slug="acme")


def test_collection_url_comes_only_from_call_arguments(probe: _Probe) -> None:
    url = probe._collection_url(slug="acme", project_id="ENG")
    assert url == "/workspaces/acme/projects/ENG/states/"


def test_missing_path_parameter_is_a_clear_error(probe: _Probe) -> None:
    with pytest.raises(KeyError, match="project_id"):
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
