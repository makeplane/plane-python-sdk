"""Rows that carry their data and know where they live (variant F)."""

from __future__ import annotations

import functools
import inspect
from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel

from .errors import FieldNotRequested


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

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name in type(self).model_fields:  # type: ignore[attr-defined]
            present = object.__getattribute__(self, "_present")
            raise FieldNotRequested(
                f"{type(self).__name__}.{name} is not available on this row: the "
                f"server returned {sorted(present)!r}. Reading it would look like "
                f"real data, so it raises instead -- request it with `fields=`, or "
                f"re-fetch the row if the collection deferred it."
            )
        raise AttributeError(name)


class Owned:
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
    parameters are named exactly `names`, and raises `TypeError` if not."""

    def __init__(self, resource: Any, ids: tuple[Any, ...], names: tuple[str, ...]) -> None:
        self._resource = resource
        self._ids = ids
        self._names = names

    def __getattr__(self, name: str) -> Any:
        attribute = getattr(self._resource, name)
        if not callable(attribute):
            return attribute

        expected = self._names
        actual = tuple(
            parameter.name
            for parameter in list(inspect.signature(attribute).parameters.values())[: len(expected)]
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
