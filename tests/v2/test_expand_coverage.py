"""`?expand=` must be reachable wherever the API offers it.

The golden declares, per operation, which relations that operation can expand
(`EXPAND` in `_generated/constants.py`). A method that simply omits an `expand`
parameter makes that capability unreachable from the SDK -- not wrong, just
invisible, and invisible in a way no test noticed: eleven methods across two
migrations shipped without it -- `Teamspaces.create/update` and
`WorkspaceViews.create/update` from the workspace-resources batch, plus
`ProjectPages.create/update`, `WikiPages.create/update` and
`WorkItemComments.create/update/upsert` from the foundation.

So this sweeps rather than lists: it walks the derived set of migrated resources
(`tests/v2/tree_walk.py`) and fails naming any method that omits a parameter its
own operation offers. Later plans inherit the check instead of repeating the
omission 59 more times.

Not in scope here: the `Literal` typing of `expand` (today it is `Sequence[str]`
on most methods). That is generator work -- the kernel already validates the
values at runtime via `encode_expand`, so the cost is autocomplete, not
correctness.
"""

from __future__ import annotations

import inspect

from plane.api.v2._generated.constants import EXPAND
from tests.v2.tree_walk import migrated_resource_classes, public_methods

ACTION_ALIASES = {"iterate": "list"}
"""Methods that answer with another action's operation: `iterate` pages `list`."""

NO_RESPONSE_BODY = {"delete"}
"""`delete` answers 204 with no body, so a query parameter that shapes the response
has nothing to shape -- even though the golden happily declares `expand` (and
`fields`) on every `*_destroy` operation. Excluded deliberately, not overlooked."""


def _expandable_methods() -> list[tuple[type, str, str, tuple[str, ...]]]:
    """(class, method name, operationId, relations) for every migrated method whose
    own operation declares `expand` and that returns a body."""
    found = []
    for resource_class in migrated_resource_classes():
        for name in public_methods(resource_class):
            action = ACTION_ALIASES.get(name, name)
            if action in NO_RESPONSE_BODY:
                continue
            operation_id = resource_class.operations.get(action)
            relations = EXPAND.get(operation_id) if operation_id is not None else None
            if relations:
                found.append((resource_class, name, operation_id, tuple(relations)))
    return found


EXPANDABLE = _expandable_methods()


def test_the_sweep_actually_finds_methods_to_check() -> None:
    """A floor, not a pin: if the derivation or the `operations` lookup breaks, the
    sweep below would pass by checking nothing."""
    assert len(EXPANDABLE) >= 20, (
        f"Only {len(EXPANDABLE)} expandable methods were found across the migrated "
        "resources -- the derivation in tests/v2/tree_walk.py or the `operations` "
        "lookup is broken, and the sweep below is passing vacuously."
    )


def test_every_method_whose_operation_offers_expand_exposes_it() -> None:
    missing = [
        f"{resource_class.__name__}.{name}() -- {operation_id} expands " f"{', '.join(relations)}"
        for resource_class, name, operation_id, relations in EXPANDABLE
        if "expand" not in inspect.signature(getattr(resource_class, name)).parameters
    ]

    assert missing == [], (
        f"{len(missing)} method(s) omit an `expand` parameter their own operation "
        "offers, making the capability unreachable from the SDK. Add "
        "`expand: Sequence[str] | None = None` and pass it through the existing "
        f"`params` dict so the kernel validates it:\n  " + "\n  ".join(missing)
    )


def test_expand_is_keyword_only_and_passed_through_params() -> None:
    """Two shape rules the fix has to keep: `expand` is keyword-only (it is an option,
    never a positional path id), and it reaches the wire through `params` so
    `_query`/`encode_expand` reject unknown relations rather than forwarding them."""
    offenders = []
    for resource_class, name, _, _ in EXPANDABLE:
        function = getattr(resource_class, name)
        parameter = inspect.signature(function).parameters.get("expand")
        if parameter is None:
            continue  # reported by the sweep above
        if parameter.kind is not parameter.KEYWORD_ONLY:
            offenders.append(f"{resource_class.__name__}.{name}(): expand is positional")
        source = inspect.getsource(function)
        if '"expand": expand' not in source and "**filters" not in source:
            offenders.append(
                f"{resource_class.__name__}.{name}(): expand is not passed through `params`"
            )

    assert offenders == [], offenders
