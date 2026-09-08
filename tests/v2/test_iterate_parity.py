"""`iterate` must yield what `list` returns, on page 2 as well as page 1.

A cheap guard on the one bug this migration actually shipped: a navigable class
whose `list` was routed through `_load_page` while its `iterate` handed back raw
rows, so `for p in projects.iterate(slug)` gave objects with no navigation and the
type only diverged at the call site. A reviewer executed all 18 navigable listers
by hand and confirmed the two agree today -- there is no live bug here. This exists
so the next person does not have to do that by hand, and so a family added later is
covered the moment it declares a `loaded_model`.

Derived, not tabled: the subjects are every class with a `loaded_model` that has
both `list` and `iterate`, and each one's path ids and collection URL are read off
its own `path` template, so a new navigable family is swept without a row being
added anywhere.

Page 2 is registered deliberately. `iterate` re-fetches with a new `offset` and
re-loads each row from a *different* response, which is where a parent id threaded
through page 1 alone would go missing -- so the sweep asserts the ids on the page-2
row as well as its type.
"""

from __future__ import annotations

from typing import Any

import pytest
import responses

from plane.api.v2._kernel.resource import V2Resource
from plane.api.v2._kernel.transport import V2Transport
from tests.v2.tree_walk import (
    WALK_CONFIG,
    expected_leading_path_ids,
    navigable_resource_classes,
    public_methods,
    template_keys,
)

API_ROOT = "https://api.example.com/api/v2"

NAVIGABLE_LISTERS = [
    resource_class
    for resource_class in navigable_resource_classes()
    if {"list", "iterate"} <= set(public_methods(resource_class))
]


def _stand_in(name: str) -> str:
    """A path-id value that is obviously a placeholder in a failure message."""
    return f"id-{name}"


def _path_ids(resource_class: type[V2Resource]) -> list[str]:  # type: ignore[type-arg]
    """The leading positional arguments `list`/`iterate` take, in path order."""
    return [_stand_in(name) for name in expected_leading_path_ids(resource_class.path)]


def _collection_url(resource_class: type[V2Resource]) -> str:  # type: ignore[type-arg]
    """The URL those arguments build -- the same substitution `_collection_url`
    makes, so the two cannot drift apart in this test."""
    filled = {key: _stand_in(key.removesuffix("_id")) for key in template_keys(resource_class.path)}
    return f"{API_ROOT}{resource_class.path.format_map(filled)}"


def _page(rows: list[dict[str, Any]], *, next_offset: int | None) -> dict[str, Any]:
    return {"data": rows, "pagination": {"style": "offset"}, "next": next_offset}


def test_the_sweep_actually_finds_navigable_listers() -> None:
    """A floor, not a pin: if the derivation breaks, everything below passes by
    checking nothing."""
    assert len(NAVIGABLE_LISTERS) >= 15, (
        f"Only {len(NAVIGABLE_LISTERS)} navigable classes with both `list` and "
        "`iterate` were found -- the walk in tests/v2/tree_walk.py is broken and the "
        "sweep below is passing vacuously."
    )


@pytest.mark.parametrize("resource_class", NAVIGABLE_LISTERS, ids=lambda cls: cls.__name__)
@responses.activate
def test_iterate_yields_the_same_loaded_type_list_returns(
    resource_class: type[V2Resource],  # type: ignore[type-arg]
) -> None:
    url = _collection_url(resource_class)
    ids = _path_ids(resource_class)
    loaded_model = resource_class.loaded_model  # type: ignore[attr-defined]

    responses.get(url, json=_page([{"id": "row-1"}], next_offset=None))  # list
    responses.get(url, json=_page([{"id": "row-1"}], next_offset=1))  # iterate, page 1
    responses.get(url, json=_page([{"id": "row-2"}], next_offset=None))  # iterate, page 2

    resource = resource_class(V2Transport(WALK_CONFIG))
    listed = resource.list(*ids).data  # type: ignore[attr-defined]
    iterated = list(resource.iterate(*ids))  # type: ignore[attr-defined]

    assert [type(row) for row in listed] == [loaded_model], (
        f"{resource_class.__name__}.list returns {[type(r).__name__ for r in listed]}, "
        f"not the {loaded_model.__name__} its `loaded_model` names."
    )
    assert [type(row) for row in iterated] == [loaded_model, loaded_model], (
        f"{resource_class.__name__}.iterate yields "
        f"{[type(r).__name__ for r in iterated]} where `list` returns "
        f"{loaded_model.__name__}. Route it through `self._load(row, *parent_ids, "
        "fields=fields)` the same way `list` goes through `_load_page` -- a raw row "
        "has no navigation, and the divergence only shows up at the call site."
    )


@pytest.mark.parametrize("resource_class", NAVIGABLE_LISTERS, ids=lambda cls: cls.__name__)
@responses.activate
def test_iterate_threads_the_parent_ids_onto_page_two(
    resource_class: type[V2Resource],  # type: ignore[type-arg]
) -> None:
    """The half a type check alone would miss: a second page is loaded from a second
    response, so a parent id captured per-page rather than per-call would be right on
    page 1 and wrong (or absent) on page 2."""
    url = _collection_url(resource_class)
    ids = _path_ids(resource_class)

    responses.get(url, json=_page([{"id": "row-1"}], next_offset=None))  # list
    responses.get(url, json=_page([{"id": "row-1"}], next_offset=1))  # iterate, page 1
    responses.get(url, json=_page([{"id": "row-2"}], next_offset=None))  # iterate, page 2

    resource = resource_class(V2Transport(WALK_CONFIG))
    listed = resource.list(*ids).data[0]  # type: ignore[attr-defined]
    iterated = list(resource.iterate(*ids))  # type: ignore[attr-defined]

    parents = tuple(ids)
    assert listed._ids[:-1] == parents
    for index, row in enumerate(iterated, start=1):
        assert row._ids[:-1] == parents, (
            f"{resource_class.__name__}.iterate row on page {index} carries "
            f"{row._ids[:-1]!r} as its parent ids, not {parents!r} -- children "
            "reached from it would build the wrong URL."
        )
        assert row._id_names == tuple(resource_class.loaded_names)  # type: ignore[attr-defined]
