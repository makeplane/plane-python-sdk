"""A bound navigation property must never hand back an unbound resource.

`Owned.__getattr__` binds the parent's ids onto anything *callable* it forwards, and
returned everything else as-is. A sub-resource of a child -- `project.estimates.points`,
`workspace.customers.requests`, `project.work_item_types.properties` -- is not callable,
so it fell through that branch and came back **raw**: a resource that looks perfectly
usable, is the right class, and has silently dropped every id the row was carrying.

The failure is not a clean one. `project.estimates.points.create(estimate_id, data)` --
the natural spelling, mirroring `project.states.create(data)` -- raises `MissingPathId`
for a `slug` the caller supplied ages ago. And a caller who "fixes" that by passing the
ids again gets a working call, so the same expression means two different things
depending on how many arguments follow it.

Found refreshing the live integration suite, where `test_estimates.py` had been written
as `proj.estimates.points.create(estimate.id, ...)` against the old bound-locator chain
(where it worked) and had never been executed since.

It now raises `AttributeError` naming both routes that *are* typed: the flat path, or
fetching the row in between (`estimate.estimate_points`). Binding it instead would work
at runtime -- a sub-resource's leading path ids are its parent's, by URL nesting -- but
the per-child view classes declare methods, not nested children, so it would be an
untyped navigation hop, which the design rules out.
"""

from __future__ import annotations

import pytest

from plane.api.v2 import V2Namespace
from plane.api.v2._kernel.resource import V2Resource
from plane.models.v2.estimates import Estimate
from plane.models.v2.projects import Project
from plane.models.v2.work_items import WorkItem

from .tree_walk import WALK_CONFIG, child_resources


@pytest.fixture
def namespace() -> V2Namespace:
    return V2Namespace(WALK_CONFIG)


@pytest.fixture
def loaded_project(namespace: V2Namespace) -> object:
    row = Project.model_validate({"id": "p-uuid", "identifier": "ENG", "name": "Eng"})
    return namespace.workspaces.projects._load(row, "acme")


def test_a_sub_resource_of_a_navigated_child_refuses_instead_of_unbinding(
    loaded_project: object,
) -> None:
    with pytest.raises(AttributeError) as exc_info:
        _ = loaded_project.estimates.points  # type: ignore[attr-defined]

    message = str(exc_info.value)
    assert "Estimates.points is a sub-resource" in message
    assert "('acme', 'ENG')" in message, "the message must name the ids that would be lost"
    assert "flat path" in message, "the message must name a route that works"


def test_the_refusal_covers_every_navigable_child_that_has_children(
    namespace: V2Namespace, loaded_project: object
) -> None:
    """Enumerated, not spot-checked: `estimates.points` is the one the integration
    suite happened to use, and the hole was in `Owned`, so it was every one of them."""
    checked = 0
    for child_name, child in child_resources(namespace.workspaces.projects).items():
        grandchildren = child_resources(child)
        if not grandchildren:
            continue
        owned = getattr(loaded_project, child_name)
        for grandchild_name in grandchildren:
            checked += 1
            with pytest.raises(AttributeError, match="is a sub-resource"):
                getattr(owned, grandchild_name)

    assert checked >= 5, f"only {checked} sub-resources were reachable to check"


def test_methods_and_plain_class_attributes_still_come_through(
    loaded_project: object,
) -> None:
    """The guard must be narrow: only a `V2Resource` instance is refused. Methods stay
    bound, and a plain non-callable attribute (`path`) still reads through."""
    estimates = loaded_project.estimates  # type: ignore[attr-defined]
    assert callable(estimates.list)
    assert estimates.path.endswith("/estimates/")


def test_the_typed_route_the_message_points_at_actually_works(
    namespace: V2Namespace,
) -> None:
    """`estimate.estimate_points` is what the refusal recommends, so it had better
    reach a bound resource -- otherwise the error trades one dead end for another."""
    row = Estimate.model_validate({"id": "e-uuid", "name": "Points"})
    estimate = namespace.workspaces.projects.estimates._load(row, "acme", "ENG")

    points = estimate.estimate_points
    assert not isinstance(points, V2Resource), "still unbound"
    assert callable(points.list)


def test_a_work_items_children_are_reached_the_same_way(namespace: V2Namespace) -> None:
    """The second-most-used two-level hop in the suite: a loaded work item's comments."""
    row = WorkItem.model_validate({"id": "w-uuid", "name": "Do the thing"})
    work_item = namespace.workspaces.projects.work_items._load(row, "acme", "ENG")

    assert callable(work_item.comments.list)
    assert callable(work_item.attachments.list)
