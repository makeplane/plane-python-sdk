import pytest

from plane.api.v2._kernel.errors import FieldNotRequested
from plane.api.v2._kernel.loaded import Loaded, Owned
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
        _ = loaded.group


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


# -- Owned ---------------------------------------------------------------------------


class _StubResource:
    """A minimal resource whose leading positional-or-keyword parameters mirror a
    parent's path ids, `("slug", "project_id")`, for exercising `Owned`."""

    label = "not-callable"

    def retrieve(
        self, slug: str, project_id: str, item_id: str, *, expand: list[str] | None = None
    ) -> tuple[str, str, str, list[str] | None]:
        return (slug, project_id, item_id, expand)

    def summary(self, slug: str, project_id: str) -> tuple[str, str]:
        return (slug, project_id)


@pytest.fixture
def owned() -> Owned:
    return Owned(_StubResource(), ids=("acme", "ENG"), names=("slug", "project_id"))


def test_owned_prepends_ids_in_order_ahead_of_the_callers_own_argument(owned: Owned) -> None:
    assert owned.retrieve("ITEM-1") == ("acme", "ENG", "ITEM-1", None)


def test_owned_supports_a_call_with_no_caller_arguments(owned: Owned) -> None:
    assert owned.summary() == ("acme", "ENG")


def test_owned_passes_keyword_arguments_through_untouched(owned: Owned) -> None:
    assert owned.retrieve("ITEM-1", expand=["state"]) == ("acme", "ENG", "ITEM-1", ["state"])


def test_owned_returns_a_non_callable_attribute_as_is(owned: Owned) -> None:
    assert owned.label == "not-callable"


def test_owned_raises_when_the_methods_leading_parameters_are_out_of_order() -> None:
    mismatched = Owned(_StubResource(), ids=("acme", "ENG"), names=("project_id", "slug"))
    with pytest.raises(TypeError, match=r"\('project_id', 'slug'\).*\('slug', 'project_id'\)"):
        mismatched.retrieve("ITEM-1")
