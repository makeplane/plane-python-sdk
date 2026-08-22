"""Every resource's `operations` mapping must point at real operationIds. Lesson: validate against
`OPERATION_IDS`, not `FIELDS` -- `FIELDS` only covers the ~316 operations with `?fields=`, so
membership there alone can't tell a fields-less operation from a typo."""

from __future__ import annotations

import importlib
import inspect
import pkgutil
from types import ModuleType

import plane.api.v2 as v2_package
import tests.v2.fixtures as fixtures_package
from plane.api.v2._generated.constants import OPERATION_IDS
from plane.api.v2._kernel.resource import V2Resource


def _iter_resource_classes(package: ModuleType) -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """Every `V2Resource` subclass under `package` (recursing via `pkgutil.walk_packages`);
    anything under an underscore-prefixed module/subpackage is excluded."""
    found: list[type[V2Resource]] = []  # type: ignore[type-arg]
    prefix = f"{package.__name__}."
    for module_info in pkgutil.walk_packages(package.__path__, prefix=prefix):
        relative_parts = module_info.name[len(prefix) :].split(".")
        if any(part.startswith("_") for part in relative_parts):
            continue
        module = importlib.import_module(module_info.name)
        for _, obj in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(obj, V2Resource)
                and obj is not V2Resource
                and obj.__module__ == module.__name__
            ):
                found.append(obj)
    return found


def test_every_resource_class_is_discovered() -> None:
    # Sanity check on discovery itself; not pinned to today's exact resource set.
    names = {cls.__name__ for cls in _iter_resource_classes(v2_package)}
    assert {"States", "Labels"}.issubset(names)


def test_every_declared_operation_id_exists_in_the_golden() -> None:
    for resource_class in _iter_resource_classes(v2_package):
        for action, operation_id in resource_class.operations.items():
            assert operation_id in OPERATION_IDS, (
                f"{resource_class.__name__}.operations[{action!r}] = {operation_id!r} is not "
                "a real operationId in the golden (OPERATION_IDS) -- check for a typo. Note: "
                "this does NOT mean the operation lacks a `fields`/`order_by`/`expand` enum -- "
                "plenty of real operations legitimately have none of those; that case is fine "
                "and is exactly why this checks OPERATION_IDS, not FIELDS."
            )


def test_every_resource_class_discovery_finds_at_least_70() -> None:
    # Floor, not a pin: below 70 means discovery broke or resources were mass-removed.
    count = len(_iter_resource_classes(v2_package))
    assert count >= 70, (
        f"Only {count} V2Resource subclasses were discovered under {v2_package.__name__} "
        "(expected at least 70) -- either resource discovery is broken, or a large "
        "number of resources were removed. Either way, the coverage tests in this "
        "file would otherwise be silently checking far fewer classes than intended."
    )


def test_every_operation_id_in_the_golden_is_declared_by_some_resource() -> None:
    """Every real operationId must be declared by some resource's `operations` mapping (the other
    direction of coverage) -- ~123 implemented operations once had none."""
    declared_ids: set[str] = set()
    for resource_class in _iter_resource_classes(v2_package):
        declared_ids.update(resource_class.operations.values())

    golden_ids = set(OPERATION_IDS)
    missing = sorted(golden_ids - declared_ids)
    extra = sorted(declared_ids - golden_ids)
    assert not missing and not extra, (
        f"{len(missing)} golden operationId(s) are not declared by any resource's "
        f"`operations` mapping: {missing}. "
        f"{len(extra)} declared operationId(s) are not in the golden: {extra} "
        "(the previous test should already have caught these as typos)."
    )


def test_no_operation_id_is_declared_by_two_resources() -> None:
    """Each operationId must be declared by exactly one resource; a duplicate would make `_query`'s
    `fields`/`expand`/`order_by` validation nondeterministic."""
    owner_by_id: dict[str, str] = {}
    duplicates: list[tuple[str, str, str]] = []
    for resource_class in _iter_resource_classes(v2_package):
        for operation_id in resource_class.operations.values():
            owner = owner_by_id.get(operation_id)
            if owner is not None and owner != resource_class.__name__:
                duplicates.append((operation_id, owner, resource_class.__name__))
            else:
                owner_by_id[operation_id] = resource_class.__name__

    assert not duplicates, (
        "The following operationId(s) are declared by more than one resource class "
        f"(operationId, first owner, duplicate owner): {duplicates}"
    )


def test_discovery_recurses_into_subpackages() -> None:
    """Regression check using `tests/v2/fixtures/`: a subclass two packages deep must be found, one
    under an underscore-prefixed subpackage must stay excluded."""
    names = {cls.__name__ for cls in _iter_resource_classes(fixtures_package)}
    assert "DummyNestedResource" in names
    assert "ShouldNotBeDiscovered" not in names
