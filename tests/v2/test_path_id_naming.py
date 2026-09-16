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

**The check is scoped to path ids, not to every `_id` parameter.** It used to flag
any parameter ending in `_id`, which is broader than the rule: `Cycles.transfer`'s
destination is a *request body* field (the golden sends `new_cycle_id`) that the URL
template never names, and the sweep forced it renamed anyway. `Owned` compares
leading *path* parameters, so a body argument is outside the rule's scope --
`path_id_offenders` therefore only considers parameters that correspond to a
placeholder in the resource's own URL templates, or to the resource's own primary
key (the singular of its collection segment).

See the "path ids" rule in CLAUDE.md.
"""

from __future__ import annotations

import inspect
from typing import ClassVar

import pytest

from plane.api.v2._kernel.resource import V2Resource
from tests.v2.tree_walk import (
    UNMIGRATED_RESOURCES,
    all_resource_classes,
    flat_shaped_resource_classes,
    migrated_resource_classes,
    public_methods,
    reachable_resources,
    template_keys,
)

MIGRATED = migrated_resource_classes()


def _singular(segment: str) -> str:
    """`cycles` -> `cycle`, `properties` -> `property`, `me` -> `me`. Crude on
    purpose: it only has to cover the collection segments api_v2 actually uses."""
    if segment.endswith("ies"):
        return f"{segment[:-3]}y"
    if segment.endswith(("sses", "shes", "ches")):
        return segment[:-2]
    return segment[:-1] if segment.endswith("s") else segment


def path_id_names(resource_class: type[V2Resource]) -> set[str]:  # type: ignore[type-arg]
    """The parameter names that would carry a path id for this resource.

    Two sources, both read off the URL templates the class declares (`path` plus any
    `extra_paths` override):

    * every `{...}` placeholder -- the ancestors' ids, e.g. `{slug}`, `{project_id}`;
    * the resource's own primary key, which never appears as a placeholder in its own
      template (the kernel appends it to the collection URL), derived instead from the
      trailing literal segment: `.../cycles/` -> `cycle`. Both the whole segment and
      its last hyphenated word count, so `.../work-item-types/` admits
      `work_item_type` and `type`.

    Each name is admitted with and without an `_id` suffix, since the point is to
    recognise the suffixed spelling in order to reject it."""
    names: set[str] = set()
    for template in [resource_class.path, *resource_class.extra_paths.values()]:
        for key in template_keys(template):
            names.add(key)
            names.add(key.removesuffix("_id"))
        literals = [part for part in template.strip("/").split("/") if part and "{" not in part]
        if literals:
            words = literals[-1].split("-")
            for candidate in (_singular("_".join(words)), _singular(words[-1])):
                names.add(candidate)
                names.add(f"{candidate}_id")
    return names


def path_id_offenders(resource_class: type[V2Resource]) -> list[str]:  # type: ignore[type-arg]
    """Every parameter on the class that carries a path id under an `_id`-suffixed
    name. Parameters that merely end in `_id` without naming a path id -- request
    body fields such as `new_cycle_id` -- are not the rule's business."""
    known = path_id_names(resource_class)
    return [
        f"{resource_class.__name__}.{name}({parameter})"
        for name, function in public_methods(resource_class).items()
        for parameter in inspect.signature(function).parameters
        if parameter.endswith("_id") and (parameter in known or parameter[: -len("_id")] in known)
    ]


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


def test_the_opt_out_list_is_empty() -> None:
    """The ratchet's terminus: `UNMIGRATED_RESOURCES` is the plan-4 backlog, and it
    only ever shrinks (enforced elsewhere by `test_no_opted_out_class_is_actually_migrated`
    below, which fails the moment an opted-out name turns out to be migrated). It has
    now reached empty -- workflows were the last family -- so every `V2Resource`
    subclass in the package is swept by every rule in this module."""
    assert UNMIGRATED_RESOURCES == frozenset(), (
        f"{len(UNMIGRATED_RESOURCES)} classes remain unmigrated: " f"{sorted(UNMIGRATED_RESOURCES)}"
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
    onto the live tree, or whose public methods already open with every path id its
    template names, has been migrated -- leaving it opted out would hide it from
    every rule the way the old derivation did.

    The shape half used to look at `list` alone, so an opted-out bridge or singleton
    (`CustomerWorkItems`, `InitiativeProjects`, `ReleaseChangelogResource`,
    `CollectionPages`) could be migrated and stay opted out unnoticed -- there was no
    `list` to judge and, until somebody wired it, no reachability either. It now
    judges every public method, the same shape rule the naming sweep is about."""
    migrated_signals = {cls.__name__ for cls in flat_shaped_resource_classes()} | {
        cls.__name__ for cls in reachable_resources()
    }
    stale = sorted(UNMIGRATED_RESOURCES & migrated_signals)

    assert stale == [], (
        "these classes are wired onto the tree or flat-shaped, so they are migrated "
        f"and must come out of UNMIGRATED_RESOURCES: {stale}"
    )


@pytest.mark.parametrize("resource", MIGRATED, ids=lambda cls: cls.__name__)
def test_no_public_method_names_a_path_id_with_an_id_suffix(resource: type) -> None:
    assert path_id_offenders(resource) == [], (
        "path ids are named after the resource they identify, with no `_id` suffix: "
        f"{path_id_offenders(resource)}"
    )


def test_the_check_ignores_id_suffixed_parameters_that_are_not_path_ids() -> None:
    """The other half of the repair, proved on a resource built for it.

    `destination_cycle_id` is a request *body* field: the URL template never names it
    and `Owned` never compares it, so flagging it forced renames the rule does not
    ask for (this is what turned `Cycles.transfer`'s `new_cycle_id` into
    `new_cycle`). `cycle_id` on the same class *is* the resource's own primary key
    and must still be caught."""

    class BodyFieldCycles(V2Resource):  # type: ignore[type-arg]
        path = "/workspaces/{slug}/projects/{project_id}/cycles/"
        operations: ClassVar[dict[str, str]] = {}

        def transfer(self, slug: str, project: str, cycle: str, destination_cycle_id: str) -> None:
            """Body field, not a path id -- outside the rule."""

        def retrieve(self, slug: str, project: str, cycle_id: str) -> None:
            """The resource's own pk, suffixed -- the violation the rule exists for."""

    assert path_id_offenders(BodyFieldCycles) == ["BodyFieldCycles.retrieve(cycle_id)"]


CATALOG_SIBLINGS = {
    ("Releases", "ReleaseLabels"),
    ("Initiatives", "InitiativeLabels"),
}
"""(parent, child) pairs where the child's `list` is legitimately shorter than its
parent's `loaded_names` -- exempted rather than made to agree with it.

`ReleaseLabels` lives at `ws.releases.labels` for the sake of its per-release
*bridge* (`add`/`remove`, which do take `(slug, release)` -- the
`_OwnedReleaseLabels` view in `_loaded/release.py`), but it is also a
workspace-level catalog reached as `Releases`' sibling, not its nested child:
`ReleaseLabels.list` lists the whole workspace catalog and so takes only `(slug,)`.
The rule this test enforces is about a *nested* child's own path ids matching what
`Owned` will prepend -- it does not apply to a catalog resource that merely happens
to be attached next to a navigable parent for its bridge.

`ReleaseTags` used to be the second entry here and is not any more. It had no
per-release bridge at all -- no reason to sit under `Releases` -- so the exemption
was carrying an attachment that should not have existed: `release.tags` was a
navigation property on which every call raised. It is `ws.release_tags` now, a
workspace child of a workspace catalog, and needs no exemption. An entry here is
for a class with a *real* per-parent bridge; without one, move the attachment.

`InitiativeLabels` is the third of exactly that shape and joined the set the moment
`Initiatives` was wired onto the tree (`plane/api/v2/initiatives/labels.py` says so
in its own docstring: "same shape as `releases/labels.py` -- copied from it"). Its
catalog CRUD hits `/workspaces/{slug}/initiatives/labels/` and takes `(slug,)`,
while its `add`/`remove` bridge to the per-initiative `extra_paths` override and do
take `(slug, initiative)`. Any *other* divergence is a bug, not a catalog: a nested
child whose `list` disagrees with its parent's `loaded_names` breaks `Owned`."""


def test_a_childs_leading_parameters_match_what_its_parent_binds() -> None:
    """The rule's whole point: `Owned` compares these names literally, so a navigable
    parent's `loaded_names` and each child's leading parameters have to agree.

    Parent/child pairs are read off the live tree -- a resource that gains a child is
    checked the moment it is wired, with no row to remember to add here. Catalog
    siblings reached at a navigable parent's attribute name but scoped one path id
    shorter (see `CATALOG_SIBLINGS`) are exempted, not silently skipped: dropping the
    name from that set without the class actually changing shape fails this test the
    same way an unnoticed regression would."""
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
            if (parent_class.__name__, child_class.__name__) in CATALOG_SIBLINGS:
                continue
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
