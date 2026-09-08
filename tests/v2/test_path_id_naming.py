"""The path-id naming rule, enforced rather than left to be inferred.

Every path id a v2 method takes is named after the resource it identifies, singular,
with no `_id` suffix -- `slug`, `project`, `work_item`, `state`, `label`, `page`,
`comment`, `release`. The rule matters mechanically, not just cosmetically: `Owned`
matches a child method's leading parameter names against the parent's `loaded_names`
exactly, so a resource that suffixes its own pk breaks navigation from its parent the
day it gains one. The URL *templates* keep the golden's own keys (`{project_id}`,
`{work_item_id}`), and so do model field names; this is about parameters only.

**The set under test is enumerated, never listed.** This file used to carry a
hand-written `MIGRATED` list of ten classes; a batch of nineteen more was migrated,
every one of them broke the rule, and the test stayed green because nobody appended
to the list. Deriving the set from the live tree fixed that and opened a quieter
hole: the derivation only saw classes that were wired, or that had a `list` to judge,
which left 18 of 90 classes -- every bridge, every singleton, the workspace root --
permanently unswept. So the subject set is now *every* `V2Resource` subclass in the
package minus an explicit, shrinking opt-out (`tests/v2/tree_walk.py`), and the
guards below keep that opt-out honest.

See the "path ids" rule in CLAUDE.md.
"""

from __future__ import annotations

import inspect

import pytest

from tests.v2.tree_walk import (
    UNMIGRATED_RESOURCES,
    all_resource_classes,
    flat_resource_classes,
    migrated_resource_classes,
    public_methods,
    reachable_resources,
)

MIGRATED = migrated_resource_classes()

OPT_OUT_CEILING = 35
"""The size of `UNMIGRATED_RESOURCES` when the enumeration landed. A ratchet: the
list is the plan-4 backlog and may only shrink, so growing it fails here."""


def test_the_enumerated_set_is_not_empty_or_tiny() -> None:
    """A floor, not a pin: if the enumeration ever breaks, every sweep below would
    pass vacuously, which is the failure mode this rewrite exists to prevent."""
    assert len(MIGRATED) >= 50, (
        f"Only {len(MIGRATED)} resource classes were enumerated -- the package walk "
        "in tests/v2/tree_walk.py is broken, and every rule sweep built on it is now "
        "passing vacuously."
    )


def test_the_sweep_covers_every_class_that_is_not_explicitly_opted_out() -> None:
    """The inversion, asserted: inclusion is the default. Anything outside the sweep
    is outside it because somebody wrote its name in `UNMIGRATED_RESOURCES`, not
    because it happens to lack a `list` or happens not to be wired yet."""
    unswept = {cls.__name__ for cls in all_resource_classes()} - {cls.__name__ for cls in MIGRATED}

    assert unswept == set(UNMIGRATED_RESOURCES), (
        "classes outside the sweep must be exactly the opted-out ones. Unexpectedly "
        f"unswept: {sorted(unswept - UNMIGRATED_RESOURCES)}; opted out but swept "
        f"anyway: {sorted(UNMIGRATED_RESOURCES - unswept)}."
    )


def test_the_opt_out_list_only_shrinks() -> None:
    assert len(UNMIGRATED_RESOURCES) <= OPT_OUT_CEILING, (
        f"UNMIGRATED_RESOURCES has grown to {len(UNMIGRATED_RESOURCES)} (ceiling "
        f"{OPT_OUT_CEILING}). It is the plan-4 backlog and may only shrink: a new "
        "resource class is swept from the moment it exists. If a genuinely pre-flat "
        "class was just added, lower it into shape instead of opting it out."
    )


def test_the_opt_out_list_names_only_real_classes() -> None:
    """A stale name is an opt-out nobody can see is dead."""
    known = {cls.__name__ for cls in all_resource_classes()}

    assert UNMIGRATED_RESOURCES <= known, (
        "UNMIGRATED_RESOURCES names classes that no longer exist -- delete them: "
        f"{sorted(UNMIGRATED_RESOURCES - known)}"
    )


def test_no_opted_out_class_is_actually_migrated() -> None:
    """The guard that makes the list shrink on its own. A class that has been wired
    onto the live tree, or whose `list` already consumes every path id its template
    names, has been migrated -- leaving it opted out would hide it from every rule
    the way the old derivation did."""
    migrated_signals = {cls.__name__ for cls in flat_resource_classes()} | {
        cls.__name__ for cls in reachable_resources()
    }
    stale = sorted(UNMIGRATED_RESOURCES & migrated_signals)

    assert stale == [], (
        "these classes are wired onto the tree or flat-shaped, so they are migrated "
        f"and must come out of UNMIGRATED_RESOURCES: {stale}"
    )


@pytest.mark.parametrize("resource", MIGRATED, ids=lambda cls: cls.__name__)
def test_no_public_method_names_a_path_id_with_an_id_suffix(resource: type) -> None:
    offenders = [
        f"{resource.__name__}.{name}({parameter})"
        for name, function in public_methods(resource).items()
        for parameter in inspect.signature(function).parameters
        if parameter.endswith("_id")
    ]

    assert offenders == [], (
        "path ids are named after the resource they identify, with no `_id` suffix: " f"{offenders}"
    )


def test_a_childs_leading_parameters_match_what_its_parent_binds() -> None:
    """The rule's whole point: `Owned` compares these names literally, so a navigable
    parent's `loaded_names` and each child's leading parameters have to agree.

    Parent/child pairs are read off the live tree -- a resource that gains a child is
    checked the moment it is wired, with no row to remember to add here."""
    reachable = reachable_resources()
    children_of: dict[str, list[type]] = {}
    for child_class, dotted in reachable.items():
        children_of.setdefault(dotted.rsplit(".", 1)[0], []).append(child_class)

    checked = 0
    for parent_class, dotted in sorted(reachable.items(), key=lambda kv: kv[1]):
        bound = tuple(getattr(parent_class, "loaded_names", ()) or ())
        if not bound:
            continue
        for child_class in children_of.get(dotted, []):
            lister = vars(child_class).get("list")
            if not inspect.isfunction(lister):
                continue
            leading = tuple(inspect.signature(lister).parameters)[1 : 1 + len(bound)]
            assert leading == bound, (
                parent_class.__name__,
                child_class.__name__,
                leading,
                bound,
            )
            checked += 1

    assert checked >= 4, f"Only {checked} parent/child pairs were checked; the walk is broken."
