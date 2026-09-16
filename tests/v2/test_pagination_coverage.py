"""`?paginate=` and `?count=` must be reachable wherever the API offers them.

The third sibling of `test_expand_coverage.py` and `test_fields_coverage.py`, and the
one whose absence cost the most. `paginate` and `count` are *reserved* query params in
`scripts/generate_v2_constants.py`: deliberately kept out of every `*Filters` TypedDict
because each belongs on the method as an explicit typed parameter. Reserving them is
where it stopped. Not one of the 68 list methods offered either, for the whole life of
the v2 surface, and no sweep could see it -- `FIELDS` and `EXPAND` are the only golden
tables the generator emitted, so the two rules that *are* swept were the only two that
could be.

What that cost:

* **`AuditLogs` could not be listed at all.** `AuditLogViewSet.count_styles_enabled` is
  `False` server-side, so the offset envelope is refused with `count_pagination_disabled`
  and `?paginate=cursor` is the only way in. The SDK had no way to send it. The resource
  shipped, has offline tests, is wired onto the tree, is swept by every rule test -- and
  every call it can make 400s.
* **No resource could be traversed deeply.** The cursor envelope exists precisely to
  drop the `COUNT(*)`; `_kernel/pagination.py` parses it, `iterate` follows it, and
  `parse_page`'s `CursorPage` branch was unreachable from any public method.
* **`count=false` was unreachable** while `_find_one` had been sending it internally
  since it was written -- the kernel knew the parameter was real and callers could not
  say it.

Found by refreshing the live integration suite: `test_audit_logs.py` and
`test_pagination.py` were written against `paginate="cursor"`, they have never once
been executed, and they do not compile against the SDK they test.
"""

from __future__ import annotations

import inspect

from plane.api.v2._generated.constants import PAGINATION
from plane.api.v2.states import States
from tests.v2.tree_walk import migrated_resource_classes, public_methods

ACTION_ALIASES = {"iterate": "list"}
"""Methods that answer with another action's operation: `iterate` pages `list`."""

AUTO_PAGER_OWNS = {"offset", "count"}
"""What `iterate` deliberately does not expose, and why.

`offset` is the auto-pager's own walk state -- `_kernel/pagination.iterate` advances it
per page, and a caller setting it would be steering a loop it does not own (`cursor` is
different: it is a resume token the caller can legitimately hold from a previous
`CursorPage`, and `iterate` accepts it). `count` asks the server for a `COUNT(*)` on
every page of a full traversal, which is the exact cost the cursor envelope exists to
avoid. `per_page` and `paginate` are the caller's: page size and envelope choice change
what a traversal costs, and `iterate` cannot guess either."""


def _envelope_gaps(resource_classes: list[type]) -> list[str]:
    """Shared by the real sweep and by `test_the_sweep_bites`, so the failure the rule
    describes is one that has been watched happen rather than assumed."""
    gaps = []
    for resource_class in resource_classes:
        operation_id = (getattr(resource_class, "operations", {}) or {}).get("list")
        declared = PAGINATION.get(operation_id) if operation_id else None
        if not declared:
            continue
        method = getattr(resource_class, "list", None)
        if method is None:
            continue
        absent = sorted(declared - set(inspect.signature(method).parameters))
        if absent:
            gaps.append(f"{resource_class.__name__}.list() -- {operation_id} omits {absent}")
    return gaps


def _paginated_methods() -> list[tuple[type, str, str, frozenset[str]]]:
    """(class, method name, operationId, declared envelope params) for every migrated
    `list`/`iterate` whose operation declares pagination."""
    found = []
    for resource_class in migrated_resource_classes():
        for name in public_methods(resource_class):
            if name not in ACTION_ALIASES and name != "list":
                continue
            action = ACTION_ALIASES.get(name, name)
            operation_id = resource_class.operations.get(action)
            declared = PAGINATION.get(operation_id) if operation_id is not None else None
            if declared:
                found.append((resource_class, name, operation_id, declared))
    return found


PAGINATED = _paginated_methods()


def test_the_sweep_actually_finds_methods_to_check() -> None:
    """A floor, not a pin: this sweep passing vacuously is how the gap lasted."""
    assert len(PAGINATED) >= 130, (
        f"Only {len(PAGINATED)} paginated methods were found -- the enumeration in "
        "tests/v2/tree_walk.py, the `operations` lookup or the generated PAGINATION "
        "table is broken, and the sweep below is passing vacuously."
    )


def test_every_list_exposes_every_envelope_param_its_operation_declares() -> None:
    missing = _envelope_gaps(migrated_resource_classes())

    assert missing == [], (
        f"{len(missing)} list method(s) omit an envelope parameter their own operation "
        "declares, making it unreachable from the SDK:\n  " + "\n  ".join(missing)
    )


def test_every_iterate_exposes_page_size_and_envelope_choice() -> None:
    """`iterate` owns the walk, not the page size or the envelope."""
    missing = []
    for resource_class, name, operation_id, declared in PAGINATED:
        if name != "iterate":
            continue
        parameters = inspect.signature(getattr(resource_class, name)).parameters
        absent = sorted((declared - AUTO_PAGER_OWNS) - set(parameters))
        if absent:
            missing.append(f"{resource_class.__name__}.iterate() -- {operation_id} omits {absent}")

    assert missing == [], (
        f"{len(missing)} iterate method(s) leave the caller unable to choose page size "
        "or envelope:\n  " + "\n  ".join(missing)
    )


def test_iterate_does_not_expose_the_walk_state_it_owns() -> None:
    """The other direction: handing a caller `offset` on an auto-pager invites them to
    fight the loop, and `count` bills a `COUNT(*)` per page of a full traversal."""
    offenders = [
        f"{resource_class.__name__}.iterate() exposes {sorted(overlap)}"
        for resource_class, name, _, _ in PAGINATED
        if name == "iterate"
        and (
            overlap := AUTO_PAGER_OWNS
            & set(inspect.signature(getattr(resource_class, name)).parameters)
        )
    ]

    assert offenders == [], offenders


def test_envelope_params_are_keyword_only_and_reach_the_wire_through_params() -> None:
    """The same two shape rules `fields` is held to: an option is never a positional
    path id, and it goes through `params` so `_query` drops it when it is `None`
    instead of sending `paginate=None` on every call."""
    offenders = []
    for resource_class, name, _, declared in PAGINATED:
        function = getattr(resource_class, name)
        signature = inspect.signature(function)
        source = inspect.getsource(function)
        for parameter_name in sorted(declared):
            parameter = signature.parameters.get(parameter_name)
            if parameter is None:
                continue  # reported by the sweeps above
            if parameter.kind is not parameter.KEYWORD_ONLY:
                offenders.append(
                    f"{resource_class.__name__}.{name}(): {parameter_name} is positional"
                )
            if f'"{parameter_name}": {parameter_name}' not in source:
                offenders.append(
                    f"{resource_class.__name__}.{name}(): {parameter_name} is not passed "
                    "through `params`"
                )

    assert offenders == [], offenders


def test_a_cursor_page_can_actually_be_walked_by_hand() -> None:
    """`list(paginate="cursor")` answers a `CursorPage` carrying `next_cursor`. A caller
    holding one must be able to spend it, or the envelope is a dead end and `iterate` is
    the only way to see page 2."""
    without_cursor = [
        f"{resource_class.__name__}.{name}()"
        for resource_class, name, _, declared in PAGINATED
        if "paginate" in declared
        and "cursor" not in inspect.signature(getattr(resource_class, name)).parameters
    ]

    assert without_cursor == [], (
        "these methods let a caller ask for the cursor envelope but not spend the "
        f"`next_cursor` it returns: {without_cursor}"
    )


def test_the_one_operation_without_paginate_is_not_given_one() -> None:
    """`work_item_relation_definitions_list` is the one list operation of the 68 that
    declares `count`/`offset`/`per_page` but *not* `paginate`. Pinning it keeps the fix
    golden-driven rather than blanket-applied: the SDK must not invent a query param the
    API does not accept, which is the mirror image of the gap this file closed."""
    from plane.api.v2 import WorkItemRelationDefinitions

    declared = PAGINATION["work_item_relation_definitions_list"]
    assert "paginate" not in declared, (
        "the golden now declares `paginate` here -- expose it on the methods and "
        "delete this test's premise"
    )

    for name in ("list", "iterate"):
        parameters = inspect.signature(getattr(WorkItemRelationDefinitions, name)).parameters
        assert "paginate" not in parameters, (
            f"WorkItemRelationDefinitions.{name}() offers `paginate`, which its operation "
            "does not declare -- the SDK must not invent query params."
        )
        assert "cursor" not in parameters


def test_the_sweep_bites() -> None:
    """A class shaped exactly like the 68 that shipped broken: a real list operation,
    `per_page`/`offset` exposed, `paginate`/`count` silently absent. This is what the
    whole package looked like, and what nothing could see."""

    class SilentlyUnpaginated(States):
        def list(  # type: ignore[override]
            self,
            slug: str,
            project: str,
            *,
            per_page: int | None = None,
            offset: int | None = None,
        ) -> None:
            return None

    gaps = _envelope_gaps([SilentlyUnpaginated])
    assert gaps, "the sweep did not fail on a class built to violate it"
    assert "omits ['count', 'paginate']" in gaps[0], gaps
