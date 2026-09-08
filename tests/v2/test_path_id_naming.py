"""The path-id naming rule, enforced rather than left to be inferred.

Every path id a v2 method takes is named after the resource it identifies, singular,
with no `_id` suffix -- `slug`, `project`, `work_item`, `state`, `label`, `page`,
`comment`, `release`. The rule matters mechanically, not just cosmetically: `Owned`
matches a child method's leading parameter names against the parent's `loaded_names`
exactly, so a resource that suffixes its own pk breaks navigation from its parent the
day it gains one. The URL *templates* keep the golden's own keys (`{project_id}`,
`{work_item_id}`), and so do model field names; this is about parameters only.

**The set under test is derived, never listed.** This file used to carry a
hand-written `MIGRATED` list of ten classes. A batch of nineteen more resources was
then migrated, every one of them broke the rule, and the test stayed green because
nobody appended to the list. A list of what to check drifts by construction, so the
set now comes from `tests/v2/tree_walk.py`: everything reachable on the live tree
plus every flat-shaped class in the package. Later plans inherit the check for free.

See the "path ids" rule in CLAUDE.md.
"""

from __future__ import annotations

import inspect

import pytest

from tests.v2.tree_walk import migrated_resource_classes, public_methods, reachable_resources

MIGRATED = migrated_resource_classes()


def test_the_derived_set_is_not_empty_or_tiny() -> None:
    """A floor, not a pin: if the derivation ever breaks, every sweep below would pass
    vacuously, which is the failure mode this rewrite exists to prevent."""
    assert len(MIGRATED) >= 30, (
        f"Only {len(MIGRATED)} migrated resource classes were derived -- the tree walk "
        "or the flat-shape discovery in tests/v2/tree_walk.py is broken, and every "
        "rule sweep built on it is now passing vacuously."
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

    Parent/child pairs are read off the live tree too -- a resource that gains a child
    is checked the moment it is wired, with no row to remember to add here."""
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
