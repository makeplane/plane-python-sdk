"""`?fields=` must be reachable wherever the API offers it.

The twin of `tests/v2/test_expand_coverage.py`, and the reason it exists: the
naming rule and the `expand` rule are both enumerated sweeps over every migrated
class, while the `fields` rule was enforced by prose in CLAUDE.md alone. That is
exactly the hole this batch closed twice elsewhere -- a rule nobody sweeps holds
only as long as somebody re-reads it, and plan 4 copies the pattern seven more
times.

The golden declares, per operation, which field names that operation will project
(`FIELDS` in `_generated/constants.py`). A method that omits the parameter makes
the capability unreachable from the SDK.

**The one class of exception is a response that cannot be re-fetched.** Where the
body is one-time -- a secret shown once, or a presigned-upload envelope whose data
exists only in that one reply -- a projection could silently and irrecoverably drop
data the caller has no second chance at, so the parameter is deliberately not
offered. Those are named in `ONE_TIME_RESPONSES` below with their reason, and each
must also carry the reason in its own docstring, or the next reader "fixes" the
omission back. Everything else is a bug.
"""

from __future__ import annotations

import inspect

from plane.api.v2._generated.constants import FIELDS
from tests.v2.tree_walk import migrated_resource_classes, public_methods

ACTION_ALIASES = {"iterate": "list"}
"""Methods that answer with another action's operation: `iterate` pages `list`."""

NO_RESPONSE_BODY = {"delete"}
"""`delete` answers 204 with no body, so a query parameter that shapes the response
has nothing to shape -- even though the golden declares `fields` (and `expand`) on
every `*_destroy` operation. Excluded deliberately, not overlooked -- the same
exclusion `test_expand_coverage.py` makes."""

ONE_TIME_RESPONSES = {
    "Webhooks.regenerate": (
        "the response's `secret_key` is minted once and is never returned again, so "
        "a projection that dropped it would destroy the only copy"
    ),
    "WorkItemAttachments.create": (
        "the live envelope is richer than the golden documents and its `upload_data` "
        "presigned fields exist only in this reply, so a projection could strand the "
        "caller mid-upload with no way to re-fetch them"
    ),
    "WorkspaceAssets.create": (
        "same presigned-upload envelope as `WorkItemAttachments.create`: `upload_data` "
        "is not re-fetchable, so a projection could drop it beyond recovery"
    ),
    "UserAssets.create": (
        "the user-scoped twin of `WorkspaceAssets.create`, with the same "
        "one-time presigned `upload_data`"
    ),
}
"""The only methods allowed to omit a `fields` their operation offers, each with why.

The ruling in CLAUDE.md named `Webhooks.regenerate` (a one-time secret) and
`WorkItemAttachments.create` (a one-time presigned envelope). The two asset creates
were never named by it, but they are the same envelope for the same reason and fall
on the same side -- writing them down here is what makes that a decision rather than
an oversight. A new entry needs a response that genuinely cannot be re-fetched;
"large response" or "nobody asked for it" is not one."""


def _projectable_methods() -> list[tuple[type, str, str, tuple[str, ...]]]:
    """(class, method name, operationId, field names) for every migrated method whose
    own operation declares `fields` and that returns a body."""
    found = []
    for resource_class in migrated_resource_classes():
        for name in public_methods(resource_class):
            action = ACTION_ALIASES.get(name, name)
            if action in NO_RESPONSE_BODY:
                continue
            operation_id = resource_class.operations.get(action)
            names = FIELDS.get(operation_id) if operation_id is not None else None
            if names:
                found.append((resource_class, name, operation_id, tuple(names)))
    return found


PROJECTABLE = _projectable_methods()


def test_the_sweep_actually_finds_methods_to_check() -> None:
    """A floor, not a pin: if the derivation or the `operations` lookup breaks, the
    sweep below would pass by checking nothing."""
    assert len(PROJECTABLE) >= 100, (
        f"Only {len(PROJECTABLE)} projectable methods were found across the migrated "
        "resources -- the enumeration in tests/v2/tree_walk.py or the `operations` "
        "lookup is broken, and the sweep below is passing vacuously."
    )


def test_every_method_whose_operation_offers_fields_exposes_it() -> None:
    missing = [
        f"{resource_class.__name__}.{name}() -- {operation_id} projects " f"{', '.join(names)}"
        for resource_class, name, operation_id, names in PROJECTABLE
        if "fields" not in inspect.signature(getattr(resource_class, name)).parameters
        and f"{resource_class.__name__}.{name}" not in ONE_TIME_RESPONSES
    ]

    assert missing == [], (
        f"{len(missing)} method(s) omit a `fields` parameter their own operation "
        "offers, making the capability unreachable from the SDK. Add "
        "`fields: Sequence[<Operation>Field] | None = None` and pass it through the "
        "existing `params` dict so the kernel validates it against the golden -- or, "
        "if the response is genuinely one-time and unrecoverable, add it to "
        f"ONE_TIME_RESPONSES with the reason:\n  " + "\n  ".join(missing)
    )


def test_fields_is_keyword_only_and_passed_through_params() -> None:
    """Two shape rules the fix has to keep: `fields` is keyword-only (it is an
    option, never a positional path id), and it reaches the wire through `params` so
    `_query`/`encode_fields` reject names the operation does not offer rather than
    forwarding them."""
    offenders = []
    for resource_class, name, _, _ in PROJECTABLE:
        function = getattr(resource_class, name)
        parameter = inspect.signature(function).parameters.get("fields")
        if parameter is None:
            continue  # reported by the sweep above, or a named exception
        if parameter.kind is not parameter.KEYWORD_ONLY:
            offenders.append(f"{resource_class.__name__}.{name}(): fields is positional")
        source = inspect.getsource(function)
        if '"fields": fields' not in source and "**filters" not in source:
            offenders.append(
                f"{resource_class.__name__}.{name}(): fields is not passed through `params`"
            )

    assert offenders == [], offenders


def test_every_named_exception_is_a_real_method_that_actually_omits_fields() -> None:
    """A stale exception is an omission nobody can see is dead -- and an exception
    for a method that does expose `fields` reads as a rule that was never met."""
    projectable = {f"{cls.__name__}.{name}" for cls, name, _, _ in PROJECTABLE}
    unknown = sorted(set(ONE_TIME_RESPONSES) - projectable)

    assert unknown == [], (
        "ONE_TIME_RESPONSES names methods that are not migrated methods whose "
        f"operation offers `fields` -- delete them: {unknown}"
    )

    exposed = sorted(
        qualified
        for resource_class, name, _, _ in PROJECTABLE
        if (qualified := f"{resource_class.__name__}.{name}") in ONE_TIME_RESPONSES
        and "fields" in inspect.signature(getattr(resource_class, name)).parameters
    )

    assert exposed == [], (
        "these methods expose `fields` after all, so their exception is stale -- "
        f"delete them from ONE_TIME_RESPONSES: {exposed}"
    )


def test_every_named_exception_documents_its_reason_in_its_own_docstring() -> None:
    """CLAUDE.md's rule: the omission has to name the one-time-response reason where
    a reader of the method will see it, or the next reader "fixes" it back."""
    undocumented = []
    for resource_class, name, _, _ in PROJECTABLE:
        qualified = f"{resource_class.__name__}.{name}"
        if qualified not in ONE_TIME_RESPONSES:
            continue
        docstring = (inspect.getdoc(getattr(resource_class, name)) or "").lower()
        if "fields" not in docstring:
            undocumented.append(qualified)

    assert undocumented == [], (
        "these methods omit `fields` without saying so in their own docstring, so "
        "the omission reads as an oversight rather than the ruling it is: "
        f"{undocumented}"
    )
