import pytest

from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.loaded import Loaded
from plane.models.v2.states import State


class LoadedState(Loaded, State):
    pass


def test_requested_fields_read_normally() -> None:
    row = State(id="1", name="Todo")
    loaded = LoadedState.build(row, ids=("acme",), fields=["id", "name"])
    assert loaded.name == "Todo"


def test_unrequested_field_raises_and_names_what_was_asked_for() -> None:
    row = State(id="1", name="Todo")
    loaded = LoadedState.build(row, ids=("acme",), fields=["id", "name"])
    with pytest.raises(FieldNotRequested, match="group"):
        loaded.group


def test_requested_but_null_field_reads_as_none() -> None:
    row = State(id="1", name="Todo", group=None)
    loaded = LoadedState.build(row, ids=("acme",), fields=["id", "name", "group"])
    assert loaded.group is None


def test_no_fields_argument_means_everything_is_present() -> None:
    row = State(id="1", name="Todo")
    loaded = LoadedState.build(row, ids=("acme",), fields=None)
    assert loaded.group is None


def test_ids_are_kept_for_navigation() -> None:
    row = State(id="1", name="Todo")
    loaded = LoadedState.build(row, ids=("acme",), fields=None)
    assert loaded._ids == ("acme",)
