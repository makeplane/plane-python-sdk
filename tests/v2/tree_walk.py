"""Derive the set of migrated v2 resources instead of hand-listing it.

Not a test module (no `test_` prefix, so pytest never collects it): a helper the
rule-enforcing sweeps import. Every hand-written "these are the migrated classes"
list drifts the moment a migration plan lands a batch and nobody remembers to
append to it -- which is exactly how a batch of nineteen resources shipped past
`test_path_id_naming.py`. So the set is computed twice over, from the code itself:

* `reachable_resources()` walks the live tree from `V2Namespace`, through grouping
  nodes (`Wiki`, `GroupSync`) as well as resources, and yields every `V2Resource`
  instance a caller can actually reach by attribute access.
* `flat_resource_classes()` walks the package instead, and keeps the classes whose
  `list` already takes every path id its own URL template names -- the mechanical
  definition of "migrated to the flat shape". This catches a migrated resource that
  is not (yet) wired onto the tree; `ProjectPages` is one today.

`migrated_resource_classes()` is the union, which is what the sweeps assert on.
"""

from __future__ import annotations

import importlib
import inspect
import pkgutil
import re
from types import ModuleType
from typing import Any

import plane.api.v2 as v2_package
from plane.api.v2 import V2Namespace
from plane.api.v2._kernel.resource import V2Resource
from plane.config import Configuration

_TEMPLATE_KEY = re.compile(r"{(\w+)}")

WALK_CONFIG = Configuration(base_path="https://api.example.com", api_key="secret")
"""Constructing the tree makes no request (see `test_tree.py`), so any config works."""


def is_pending(function: Any) -> bool:
    """True for a method still carrying its pre-flat body behind
    `@pending_flat_migration` -- it is documented as unmigrated, so the rules that
    apply to migrated code do not apply to it yet."""
    return getattr(function, "__pending_flat_migration__", False) is True


def public_methods(resource_class: type) -> dict[str, Any]:
    """The class's own public, non-pending methods (not inherited kernel helpers)."""
    return {
        name: function
        for name, function in vars(resource_class).items()
        if not name.startswith("_") and inspect.isfunction(function) and not is_pending(function)
    }


def reachable_resources(namespace: V2Namespace | None = None) -> dict[type, str]:
    """Every `V2Resource` class reachable by attribute access from `V2Namespace`,
    mapped to the dotted path it was first reached by (`v2.workspaces.roles`).

    Grouping nodes (`Wiki`, `GroupSync`) hold no `V2Resource` base of their own but
    do hold children, so they are descended into rather than skipped.
    `PendingMigration` placeholders hold nothing public, so they fall out on their
    own."""
    found: dict[type, str] = {}

    def walk(node: object, prefix: str) -> None:
        for name, child in vars(node).items():
            if name.startswith("_") or name == "transport":
                continue
            path = f"{prefix}.{name}"
            if isinstance(child, V2Resource):
                if type(child) not in found:
                    found[type(child)] = path
                    walk(child, path)
            elif type(child).__module__.startswith(v2_package.__name__):
                walk(child, path)

    walk(namespace if namespace is not None else V2Namespace(WALK_CONFIG), "v2")
    return found


def _iter_resource_classes(package: ModuleType) -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """Every `V2Resource` subclass defined under `package`; underscore-prefixed
    modules and subpackages are excluded (same discovery as
    `test_operations_coverage.py`)."""
    found: list[type[V2Resource]] = []  # type: ignore[type-arg]
    prefix = f"{package.__name__}."
    for module_info in pkgutil.walk_packages(package.__path__, prefix=prefix):
        if any(part.startswith("_") for part in module_info.name[len(prefix) :].split(".")):
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


def _leading_path_ids(function: Any) -> int:
    """How many positional-or-keyword parameters a method takes before its `*`."""
    return sum(
        1
        for parameter in inspect.signature(function).parameters.values()
        if parameter.kind is parameter.POSITIONAL_OR_KEYWORD and parameter.name != "self"
    )


def flat_resource_classes() -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """Classes whose `list` already consumes exactly the path ids its URL template
    names -- i.e. migrated to the flat shape.

    The pre-flat shape is precisely the one that omits them (`Releases.list()` takes
    none while `/workspaces/{slug}/releases/` names one), so the count is the
    discriminator; a class with no `list` of its own (singletons like
    `WorkspacePermissions`) is left to `reachable_resources` to contribute."""
    flat = []
    for resource_class in _iter_resource_classes(v2_package):
        function = vars(resource_class).get("list")
        if not inspect.isfunction(function) or is_pending(function):
            continue
        if _leading_path_ids(function) == len(set(_TEMPLATE_KEY.findall(resource_class.path))):
            flat.append(resource_class)
    return flat


def migrated_resource_classes() -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """The derived set the rule sweeps run over: reachable on the tree, or flat-shaped
    in the package. Sorted by name so parametrized ids are stable."""
    classes = set(reachable_resources()) | set(flat_resource_classes())
    return sorted(classes, key=lambda cls: cls.__name__)
