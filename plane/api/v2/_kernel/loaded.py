"""Rows that carry their data and know where they live (variant F)."""

from __future__ import annotations

import functools
import inspect
from collections.abc import Callable, Sequence
from typing import TYPE_CHECKING, Any, Concatenate, Generic, ParamSpec, TypeVar

from pydantic import BaseModel

from .errors import FieldNotRequested

TResource = TypeVar("TResource")
P = ParamSpec("P")
R = TypeVar("R")


class Loaded:
    """Mixin over a pydantic row: absent fields raise instead of reading as `None`."""

    _ids: tuple[Any, ...]
    _id_names: tuple[str, ...]
    _present: frozenset[str]

    @classmethod
    def build(
        cls,
        row: BaseModel,
        ids: tuple[Any, ...],
        fields: Sequence[str] | None = None,
        names: tuple[str, ...] | None = None,
    ) -> Any:
        # Presence is what the *server returned*, never what the caller asked for.
        # The API defers fields on collection reads even when no `fields=` was passed,
        # so deriving presence from the request would mark every field present and hand
        # back a silent `None` for one the response never carried. `model_fields_set` is
        # the response's own record of which keys actually arrived.
        returned = set(row.model_fields_set)
        if fields is not None:
            # A caller that asked for fewer fields than the server sent still sees only
            # what it asked for; `id` is always available.
            returned &= set(fields) | {"id"}
        data = {key: value for key, value in row.model_dump().items() if key in returned}
        obj = cls.model_construct(**data)  # type: ignore[attr-defined]
        # `model_construct` back-fills declared defaults, so a field the server never
        # sent would read as `None` and look like real data. Drop those, so reading one
        # reaches `__getattr__`.
        for absent in [key for key in obj.__dict__ if key not in data]:
            del obj.__dict__[absent]
        object.__setattr__(obj, "_ids", tuple(ids))
        # Recorded alongside the values so a child `Owned` can be built from a loaded
        # row without the caller re-stating which path id is which.
        object.__setattr__(obj, "_id_names", tuple(names) if names is not None else ())
        object.__setattr__(obj, "_present", frozenset(data))
        return obj

    if not TYPE_CHECKING:
        # Deliberately invisible to type checkers. A declared `__getattr__ -> Any`
        # would make *every* attribute on a loaded row `Any` -- which is how the
        # navigation properties lost their types in the first place. Hidden, a type
        # checker resolves reads against the row model's real fields and flags a
        # misspelling; at runtime this still turns an absent field into
        # `FieldNotRequested`.
        def __getattr__(self, name: str) -> Any:
            if name.startswith("_"):
                raise AttributeError(name)
            if name in type(self).model_fields:
                present = object.__getattribute__(self, "_present")
                raise FieldNotRequested(
                    f"{type(self).__name__}.{name} is not available on this row: the "
                    f"server returned {sorted(present)!r}. Reading it would look like "
                    f"real data, so it raises instead -- request it with `fields=`, or "
                    f"re-fetch the row if the collection deferred it."
                )
            raise AttributeError(name)


class Owned(Generic[TResource]):
    """A child resource with its parent's path ids already supplied.

    `ids` is a tuple in URL order; a call prepends them *positionally* to the
    wrapped method, since every kernel resource takes its path ids as leading
    positional-or-keyword parameters. Passing them as keywords instead would
    collide with a caller's own positional argument for the same parameter
    (e.g. `project.work_items.retrieve("ENG-12")` sending `"ENG-12"`
    positionally into `slug` while `slug=` also arrived as a keyword).

    `names` is the parameter name each entry of `ids` is meant to fill, in the
    same order. Positional prepending has no way to notice on its own if a
    resource's leading parameters are ever ordered differently from `ids` --
    the wrong values would flow into a well-formed but wrong URL with no
    error at all. So before making the call, `__getattr__` checks (via
    `inspect.signature`) that the resolved method's first `len(ids)`
    parameters are named exactly `names`, and raises `TypeError` if not.

    Generic over the resource it wraps so a loaded row's navigation property can
    declare `Owned[States]`, and so the per-child `if TYPE_CHECKING` view classes
    (`_OwnedStates` and friends, built with `bind1`/`bind2`/`bind3` below) inherit
    from a type that names their resource. Those views -- not this class -- are what
    give `project.states.list()` a real type: see `_loaded/project.py`."""

    def __init__(self, resource: TResource, ids: tuple[Any, ...], names: tuple[str, ...]) -> None:
        self._resource = resource
        self._ids = ids
        self._names = names

    if not TYPE_CHECKING:
        # Hidden from type checkers for the same reason as `Loaded.__getattr__`: a
        # declared `-> Any` would silently make every navigation call untyped, and
        # would swallow a misspelled method name instead of flagging it. Callers see
        # the per-child view classes' declared methods instead.
        def __getattr__(self, name: str) -> Any:
            attribute = getattr(self._resource, name)
            if not callable(attribute):
                return attribute

            expected = self._names
            actual = tuple(
                parameter.name
                for parameter in list(inspect.signature(attribute).parameters.values())[
                    : len(expected)
                ]
            )
            if actual != expected:
                raise TypeError(
                    f"{type(self._resource).__name__}.{name} does not take its leading "
                    f"parameters in the order {expected!r} that {type(self).__name__} was "
                    f"built with -- found {actual!r} instead. Refusing to prepend ids that "
                    f"would silently land in the wrong parameters."
                )

            @functools.wraps(attribute)
            def bound(*args: Any, **kwargs: Any) -> Any:
                return attribute(*self._ids, *args, **kwargs)

            return bound


# -- Typed views on an `Owned` ------------------------------------------------------
#
# `Owned` prepends N path ids at runtime, so the method a caller reaches through it has
# the *same* signature as the resource's own method minus `self` and those N leading
# ids. Python's type system can express exactly that with `Concatenate`, which is what
# these helpers do. They are only ever evaluated by a type checker -- each per-child
# view class lives inside `if TYPE_CHECKING` -- and each entry is one line:
#
#     if TYPE_CHECKING:
#         class _OwnedStates(Owned[States]):
#             list = staticmethod(bind2(States.list))
#             retrieve = staticmethod(bind2(States.retrieve))
#
# `staticmethod` stops the checker from re-binding `self` onto the already-bound
# callable. The result is a real type: `project.states.list()` is `Page[State]`, an
# unknown keyword is rejected, and `project.states.lst()` is an attribute error.
#
# Follow-on migrations copy this block verbatim, changing only the arity and the
# method list -- see the "loaded rows" rule in CLAUDE.md.


def bind1(method: Callable[Concatenate[Any, Any, P], R]) -> Callable[P, R]:
    """The type of `method` with `self` and one leading path id already supplied."""
    raise NotImplementedError("bind1 exists for type checkers only")


def bind2(method: Callable[Concatenate[Any, Any, Any, P], R]) -> Callable[P, R]:
    """The type of `method` with `self` and two leading path ids already supplied."""
    raise NotImplementedError("bind2 exists for type checkers only")


def bind3(method: Callable[Concatenate[Any, Any, Any, Any, P], R]) -> Callable[P, R]:
    """The type of `method` with `self` and three leading path ids already supplied."""
    raise NotImplementedError("bind3 exists for type checkers only")
