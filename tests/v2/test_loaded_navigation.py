"""A loaded row must reach every child its resource attaches.

`tests/v2/test_tree.py` proves the *resource* side: `PROJECT_TREE_ATTACHMENTS`
compares its table against `vars(Projects(...))`, so a child attached without a row
fails by name. Nothing compared either of those to the *row* side, and the gap that
left was not theoretical: `Projects.__init__` attached fifteen children while
`LoadedProject` exposed three, so `workspaces.projects.cycles.list(slug, project)`
worked and `project.cycles.list()` raised `AttributeError` -- half the design
missing on its most important row, with every sweep green.

This closes it, by derivation rather than by table: for every resource that declares
a `loaded_model`, the navigation properties on its `Loaded` type must be exactly the
child resources the resource itself attaches. Seven families are navigable today and
plan 4 brings the count to fourteen; without this the same gap reopens once per
family, seven more times.

Two things the sweep checks that a name-only comparison would miss:

* each property must wrap *its own* child resource, so a copy-pasted
  `Owned(self._resources.states, ...)` under `def modules` is caught;
* each property must hand back an `Owned`, not the bare resource -- a bare resource
  would still need every id repeated, which is the whole thing loaded rows exist to
  avoid.

**And one thing selection made it structurally unable to see at all.** The two
sweeps above run over `navigable_resource_classes()`, which *selects* the classes
that declare a `loaded_model`. A resource with children and no `loaded_model` is
therefore invisible to them: it has nothing to compare, so it passes by not being
looked at. That is not hypothetical either -- `Workspaces` sat exactly there,
attaching 24 children while `client.v2.workspaces.retrieve("acme")` answered a bare
`Workspace`, so `workspace.projects` raised `AttributeError` on the design's
navigable row #1 with all three assertions green. It is the same failure mode that
let the path-id rule break across 16 classes: a rule enforced over an opportunistic
subset holds only for the members that opted in.

`test_every_resource_with_children_declares_a_loaded_model` closes it by
*enumeration*: over every resource class in the package, having child resources and
having a `loaded_model` must be the same thing. It is the durable half of the fix --
without it the hole reopens for whichever family somebody adds next -- and
`test_the_child_bearing_sweep_bites` proves it fails on a class shaped like the
regression rather than leaving that to a reviewer's word.
"""

from __future__ import annotations

from typing import ClassVar

import pytest

from plane.api.v2._kernel.loaded import Loaded, Owned
from plane.api.v2._kernel.resource import V2Resource
from plane.api.v2._kernel.transport import V2Transport
from tests.v2.tree_walk import (
    WALK_CONFIG,
    child_resources,
    migrated_resource_classes,
    navigable_resource_classes,
)

NAVIGATION_ALIASES: dict[str, dict[str, str]] = {
    "LoadedEstimate": {"points": "estimate_points"},
    "LoadedWorkItemProperty": {"options": "property_options"},
    "LoadedWorkspaceWorkItemProperty": {"options": "property_options"},
}
"""Child attribute name -> navigation property name, where the two must differ.

`Estimate.points` is a real API field (the inline point data `expand=["points"]`
returns), so `LoadedEstimate` cannot name its navigation property `points` without
shadowing it -- it is `estimate_points`. `WorkItemProperty.options` is the same
shape of collision (the inlined choices for OPTION-type properties), so both
`LoadedWorkItemProperty` and `LoadedWorkspaceWorkItemProperty` expose their
`options` child as `property_options`. Any other divergence is a bug, not an
alias; add a row here only with a reason of the same kind."""

NAVIGABLE = navigable_resource_classes()


def _navigation_properties(loaded_model: type) -> set[str]:
    """The navigation properties a `Loaded` subclass declares in its own body.

    Read off the class rather than off an instance: calling one needs a row, and the
    point is to know what exists before anything is fetched."""
    return {name for name, value in vars(loaded_model).items() if isinstance(value, property)}


def _row_of(resource: V2Resource) -> Loaded:  # type: ignore[type-arg]
    """An empty loaded row wired to `resource`, so its navigation properties can be
    read without a fetch. Ids are stand-ins: nothing here reaches the wire."""
    loaded_model = type(resource).loaded_model
    assert loaded_model is not None
    row = loaded_model.model_construct()  # type: ignore[attr-defined]
    names = tuple(type(resource).loaded_names)
    object.__setattr__(row, "_ids", tuple(f"id-{name}" for name in names))
    object.__setattr__(row, "_id_names", names)
    object.__setattr__(row, "_present", frozenset())
    object.__setattr__(row, "_resources", resource)
    return row  # type: ignore[no-any-return]


def test_the_sweep_actually_finds_navigable_resources() -> None:
    """A floor, not a pin: if `loaded_model` discovery breaks, every assertion below
    would pass by checking nothing."""
    assert len(NAVIGABLE) >= 7, (
        f"Only {len(NAVIGABLE)} navigable resource classes were found -- the walk in "
        "tests/v2/tree_walk.py or the `loaded_model` declaration is broken, and the "
        "sweep below is passing vacuously."
    )


@pytest.mark.parametrize("resource_class", NAVIGABLE, ids=lambda cls: cls.__name__)
def test_a_loaded_row_reaches_every_child_its_resource_attaches(
    resource_class: type[V2Resource],  # type: ignore[type-arg]
) -> None:
    resource = resource_class(V2Transport(WALK_CONFIG))
    loaded_model = resource_class.loaded_model
    assert loaded_model is not None

    aliases = NAVIGATION_ALIASES.get(loaded_model.__name__, {})
    expected = {aliases.get(name, name) for name in child_resources(resource)}
    declared = _navigation_properties(loaded_model)

    assert declared == expected, (
        f"{loaded_model.__name__} must expose one navigation property per child "
        f"{resource_class.__name__} attaches. Children with no way to reach them "
        f"from a fetched row: {sorted(expected - declared)}; properties with no "
        f"child behind them: {sorted(declared - expected)}. Add the property (with "
        "its `if TYPE_CHECKING` `Owned` view, so the signatures survive a type "
        f"checker), or add a reasoned entry to NAVIGATION_ALIASES."
    )


@pytest.mark.parametrize("resource_class", NAVIGABLE, ids=lambda cls: cls.__name__)
def test_each_navigation_property_wraps_its_own_child(
    resource_class: type[V2Resource],  # type: ignore[type-arg]
) -> None:
    """Name equality alone would pass a copy-pasted property that returns the wrong
    child -- `Owned(self._resources.states, ...)` under `def modules` builds a
    perfectly well-formed call to the wrong URL."""
    resource = resource_class(V2Transport(WALK_CONFIG))
    loaded_model = resource_class.loaded_model
    assert loaded_model is not None

    aliases = NAVIGATION_ALIASES.get(loaded_model.__name__, {})
    row = _row_of(resource)

    for attribute, child in child_resources(resource).items():
        owned = getattr(row, aliases.get(attribute, attribute))
        assert isinstance(owned, Owned), (
            f"{loaded_model.__name__}.{attribute} must hand back an `Owned` (which "
            "carries the row's ids), not the bare resource."
        )
        assert owned._resource is child, (
            f"{loaded_model.__name__}.{attribute} wraps "
            f"{type(owned._resource).__name__}, not {type(child).__name__}."
        )
        assert owned._ids == row._ids
        assert owned._names == tuple(resource_class.loaded_names)


# -- The gap selection could not see -------------------------------------------------


def _resources_with_children_but_no_loaded_model(
    resource_classes: list[type[V2Resource]],  # type: ignore[type-arg]
) -> list[str]:
    """`"Name (child, child)"` for every class that attaches child resources without
    declaring a `loaded_model`.

    Split out of the test so the sweep can be run over a class built to violate it --
    see `test_the_child_bearing_sweep_bites`. A rule whose failure nobody has ever
    seen is a rule nobody knows the shape of."""
    offenders = []
    for resource_class in resource_classes:
        children = child_resources(resource_class(V2Transport(WALK_CONFIG)))
        if children and getattr(resource_class, "loaded_model", None) is None:
            offenders.append(f"{resource_class.__name__} ({', '.join(sorted(children))})")
    return offenders


def test_every_resource_with_children_declares_a_loaded_model() -> None:
    """Having children and being navigable must be the same thing.

    Enumerated over every class in the package, deliberately: the two sweeps above
    *select* on `loaded_model`, so a resource that has children and does not declare
    one is invisible to them and passes by never being looked at."""
    offenders = _resources_with_children_but_no_loaded_model(migrated_resource_classes())

    assert offenders == [], (
        f"{len(offenders)} resource class(es) attach child resources but declare no "
        "`loaded_model`, so a row they fetch cannot reach any of those children and "
        "the two sweeps above cannot see the gap. Give the class a `Loaded` subclass "
        "in `plane/api/v2/_loaded/` (with `loaded_names`, and one navigation property "
        "per child), and route every row-returning method through `self._load(...)`. "
        "If the attachment is not really a per-row child -- a workspace-level catalog "
        "hung off a family, say -- move it to the scope it belongs to instead:\n  "
        + "\n  ".join(offenders)
    )


def test_the_child_bearing_sweep_bites() -> None:
    """The rule above, run against a class shaped like the regression it exists for:
    children attached, no `loaded_model`. Proves the sweep reports rather than
    silently passes -- which is exactly what its selecting siblings did for
    `Workspaces`."""

    class _SyntheticChild(V2Resource):  # type: ignore[type-arg]
        path = "/workspaces/{slug}/synthetics/{synthetic_id}/leaves/"
        model = Loaded  # type: ignore[assignment]
        operations: ClassVar[dict[str, str]] = {}

    class _SyntheticFamily(V2Resource):  # type: ignore[type-arg]
        path = "/workspaces/{slug}/synthetics/"
        model = Loaded  # type: ignore[assignment]
        operations: ClassVar[dict[str, str]] = {}

        def __init__(self, transport: V2Transport) -> None:
            super().__init__(transport)
            self.leaves = _SyntheticChild(transport)

    assert _resources_with_children_but_no_loaded_model([_SyntheticFamily]) == [
        "_SyntheticFamily (leaves)"
    ]
    # And it is the missing `loaded_model` that is reported, not merely the presence
    # of a child: the childless half of the pair passes.
    assert _resources_with_children_but_no_loaded_model([_SyntheticChild]) == []
