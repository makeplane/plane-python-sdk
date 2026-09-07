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
