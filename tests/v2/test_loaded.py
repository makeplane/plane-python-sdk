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


def test_with_no_fields_argument_presence_still_follows_the_response() -> None:
    """The API defers fields on collection reads with no `fields=` in play, so
    presence must come from the response, not from "the caller asked for nothing,
    therefore everything"."""
    row = State(id="1", name="Todo")  # the server sent exactly these two keys
    loaded = LoadedState.build(row, ids=("acme",), fields=None)

    assert loaded.name == "Todo"
    assert loaded._present == frozenset({"id", "name"})
    with pytest.raises(FieldNotRequested, match="group"):
        _ = loaded.group


def test_a_field_the_server_sent_but_the_caller_did_not_ask_for_stays_hidden() -> None:
    """`fields=` narrows presence further: asking for less than the server sent
    must not smuggle the extra keys back in."""
    row = State(id="1", name="Todo", group="backlog")
    loaded = LoadedState.build(row, ids=("acme",), fields=["id"])

    assert loaded._present == frozenset({"id"})
    with pytest.raises(FieldNotRequested, match="name"):
        _ = loaded.name


# -- Forward compatibility ---------------------------------------------------------
# The v2 read models are `extra="allow"` so a field the API starts sending stays
# readable before the SDK declares it (CLAUDE.md, "Response models"). `Loaded`
# shadows `BaseModel.__getattr__`, which is where pydantic keeps those extras, so
# without a fall-through the guarantee held on a plain row and silently died on a
# loaded one -- while `model_dump()` and `_present` both still reported the field.


def test_a_field_the_server_sent_but_the_model_does_not_declare_is_readable() -> None:
    row = State.model_validate({"id": "1", "name": "Todo", "brand_new_field": "x"})
    loaded = LoadedState.build(row, ids=("acme",), fields=None)

    assert loaded.brand_new_field == "x"
    assert "brand_new_field" in loaded._present
    assert loaded.model_dump()["brand_new_field"] == "x"


def test_an_undeclared_field_the_caller_narrowed_away_stays_hidden() -> None:
    """`fields=` narrows extras exactly as it narrows declared fields -- the
    fall-through must not smuggle back a key the caller excluded."""
    row = State.model_validate({"id": "1", "name": "Todo", "brand_new_field": "x"})
    loaded = LoadedState.build(row, ids=("acme",), fields=["id", "name"])

    assert loaded._present == frozenset({"id", "name"})
    with pytest.raises(AttributeError, match="brand_new_field"):
        _ = loaded.brand_new_field


def test_a_name_that_is_neither_a_field_nor_an_extra_is_still_an_attribute_error() -> None:
    """The fall-through must not turn a typo into something other than
    `AttributeError` -- `hasattr` and duck typing both depend on it."""
    row = State(id="1", name="Todo")
    loaded = LoadedState.build(row, ids=("acme",), fields=None)

    with pytest.raises(AttributeError, match="not_a_field_at_all"):
        _ = loaded.not_a_field_at_all


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
