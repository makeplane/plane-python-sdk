"""Placeholders for v2 resources that are wired onto the tree but not yet migrated.

Roughly 85 of the ~120 v2 resource groups still use the retired pre-flat shape: their
methods omit the leading path ids (`slug`, `project`, ...) that their URL template
names. Attaching one to the flat tree anyway meant every call failed inside the kernel
-- a bare `KeyError('slug')` before `MissingPathId` existed, and an unhelpful one after.

Dropping the attribute instead would only trade that for `AttributeError`, which reads
like a typo rather than like unfinished work. So the attribute stays, holding a
placeholder that says exactly what is going on the moment it is used.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from typing import Any, TypeVar

F = TypeVar("F", bound=Callable[..., Any])

_TRACKING = "Migration is pending; it is tracked in the variant-F follow-on plans."


class PendingMigration:
    """Stands in for a child resource whose flat migration has not happened yet.

    Any attribute access raises `NotImplementedError` naming the resource class, the
    attribute that was reached and where on the tree it sits."""

    def __init__(self, resource: str, *, reached_as: str) -> None:
        self._resource = resource
        self._reached_as = reached_as

    def __getattr__(self, name: str) -> Any:
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        raise NotImplementedError(
            f"{self._resource} is not migrated to the flat v2 shape yet, so "
            f"`{self._reached_as}.{name}` cannot be used: its methods do not accept "
            f"the leading path ids their URL needs. It is wired as a placeholder so "
            f"the gap is visible rather than silent. {_TRACKING}"
        )

    def __repr__(self) -> str:
        return f"<PendingMigration {self._resource} at {self._reached_as!r}>"


def pending_flat_migration(method: F) -> F:
    """Mark a method whose body is still the pre-flat implementation.

    The original body is kept in the source as the starting point for the migration,
    but calling the method raises instead of building a URL from path ids it never
    took. Use this where a class is reachable on the tree for some *other* reason --
    `Releases` is wired because `releases.labels` is migrated -- so unwiring the whole
    class is not an option."""

    @functools.wraps(method)
    def unmigrated(self: Any, *args: Any, **kwargs: Any) -> Any:
        raise NotImplementedError(
            f"{type(self).__name__}.{method.__name__}() is not migrated to the flat v2 "
            f"shape yet: it does not accept the leading path ids its URL needs "
            f"(`{type(self).path}`). {_TRACKING}"
        )

    return unmigrated  # type: ignore[return-value]
