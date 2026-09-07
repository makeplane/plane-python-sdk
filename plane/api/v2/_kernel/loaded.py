"""Rows that carry their data and know where they live (variant F)."""

from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel

from .errors import FieldNotRequested


class Loaded:
    """Mixin over a pydantic row: absent fields raise instead of reading as `None`."""

    _ids: tuple[Any, ...]
    _present: frozenset[str]

    @classmethod
    def build(
        cls, row: BaseModel, ids: tuple[Any, ...], fields: Sequence[str] | None = None
    ) -> Any:
        data = row.model_dump()
        if fields is not None:
            keep = set(fields) | {"id"}
            data = {key: value for key, value in data.items() if key in keep}
        obj = cls.model_construct(**data)  # type: ignore[attr-defined]
        # `model_construct` back-fills declared defaults, so a field the server never
        # sent would read as `None` and look like real data. Drop those, so reading one
        # reaches `__getattr__`.
        for absent in [key for key in obj.__dict__ if key not in data]:
            del obj.__dict__[absent]
        object.__setattr__(obj, "_ids", tuple(ids))
        object.__setattr__(obj, "_present", frozenset(data))
        return obj

    def __getattr__(self, name: str) -> Any:
        if name.startswith("_"):
            raise AttributeError(name)
        if name in type(self).model_fields:  # type: ignore[attr-defined]
            present = object.__getattribute__(self, "_present")
            raise FieldNotRequested(
                f"{type(self).__name__}.{name} was not returned: "
                f"fields={sorted(present - {'id'})!r} did not include it"
            )
        raise AttributeError(name)


class Owned:
    """A child resource with its parent's path ids already supplied.

    `ids` is a tuple in URL order; a call prepends them *positionally* to the
    wrapped method, since every kernel resource takes its path ids as leading
    positional-or-keyword parameters. Passing them as keywords instead would
    collide with a caller's own positional argument for the same parameter
    (e.g. `project.work_items.retrieve("ENG-12")` sending `"ENG-12"`
    positionally into `slug` while `slug=` also arrived as a keyword)."""

    def __init__(self, resource: Any, ids: tuple[Any, ...]) -> None:
        self._resource = resource
        self._ids = ids

    def __getattr__(self, name: str) -> Any:
        attribute = getattr(self._resource, name)
        if not callable(attribute):
            return attribute

        def bound(*args: Any, **kwargs: Any) -> Any:
            return attribute(*self._ids, *args, **kwargs)

        return bound
