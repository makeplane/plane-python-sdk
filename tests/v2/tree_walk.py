"""Derive the set of v2 resources the rule sweeps run over -- by enumeration, not
by opportunity.

Not a test module (no `test_` prefix, so pytest never collects it): a helper the
rule-enforcing sweeps import.

**The set is every `V2Resource` subclass in the package, minus an explicit opt-out
list.** That inversion is the whole point. The previous derivation was the union of
two *opportunistic* discoveries -- classes wired onto the live tree, plus classes
whose `list` already consumed every path id its URL template names -- and both miss
by construction:

* `flat_resource_classes()` needs a `list` method to judge. Eighteen of the ninety
  `V2Resource` subclasses have none: every membership bridge (`CycleWorkItems`,
  `InitiativeProjects`, ...), every singleton (`ProjectFeatures`,
  `WorkspacePermissions`, ...) and the workspace root itself. They were permanently
  outside both sweeps however they were written.
* `reachable_resources()` needs the class to be wired. A resource migrated by one
  task and wired by a later one is unchecked in between -- exactly the state
  `ProjectPages` sat in for a whole plan.

Enumerating instead makes inclusion the default and exclusion the thing somebody has
to write down: a newly migrated class is swept the moment it exists, wired or not,
`list` or not. `UNMIGRATED_RESOURCES` is the written-down part, and it must shrink
toward empty -- `tests/v2/test_path_id_naming.py` ratchets its size and refuses to
let a name in it stay opted out once the class is wired or flat-shaped.

`flat_resource_classes()` and `reachable_resources()` survive as *guards* on that
list rather than as the source of the set.
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


UNMIGRATED_RESOURCES = frozenset(
    {
        # wiki collections
        "CollectionMembers",
        "CollectionPages",
        "Collections",
        # customers
        "CustomerPropertyValues",
        "CustomerRequests",
        "CustomerWorkItems",
        "Customers",
        # initiatives
        "InitiativeLabels",
        "InitiativeProjects",
        "InitiativeWorkItems",
        "Initiatives",
        # automations (project and workspace flavours)
        "ProjectAutomationActivities",
        "ProjectAutomationEdges",
        "ProjectAutomationNodes",
        "ProjectAutomations",
        "WorkspaceAutomationActivities",
        "WorkspaceAutomationEdges",
        "WorkspaceAutomationNodes",
        "WorkspaceAutomations",
        # the four release children that stayed behind when labels/tags migrated
        "ReleaseChangelogResource",
        "ReleaseComments",
        "ReleaseLinks",
        "ReleaseWorkItems",
        # work item types and properties (both flavours)
        "WorkItemProperties",
        "WorkItemPropertyContexts",
        "WorkItemPropertyOptions",
        "WorkItemTypeProperties",
        "WorkItemTypes",
        "WorkspaceWorkItemProperties",
        "WorkspaceWorkItemPropertyOptions",
        "WorkspaceWorkItemTypeProperties",
        "WorkspaceWorkItemTypes",
        # workflows
        "WorkflowStates",
        "WorkflowTransitions",
        "Workflows",
    }
)
"""Resource classes still on the retired pre-flat shape, excluded from the sweeps.

**This list may only shrink.** It is the plan-4 backlog written down: every family
deferred by this plan's scope ruling (collections, customers, initiatives, the four
remaining release children, both automations flavours, work item types and
properties, workflows). Their methods omit the leading path ids their URL templates
name and still spell their ids `<resource>_id`, so sweeping them would report
dozens of violations that the migration itself is going to rewrite.

Deleting a name from here is part of migrating that class -- and
`tests/v2/test_path_id_naming.py` makes it compulsory rather than optional: it
fails if an opted-out class turns out to be wired onto the tree or flat-shaped, and
it fails if this list ever grows.
"""


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


def template_keys(template: str) -> list[str]:
    """The `{...}` placeholders a URL template names, in path order."""
    return _TEMPLATE_KEY.findall(template)


def reachable_resources(namespace: V2Namespace | None = None) -> dict[type, str]:
    """Every `V2Resource` class reachable by attribute access from `V2Namespace`,
    mapped to the dotted path it was first reached by (`v2.workspaces.roles`).

    Grouping nodes (`Wiki`, `GroupSync`) hold no `V2Resource` base of their own but
    do hold children, so they are descended into rather than skipped.
    `PendingMigration` placeholders hold nothing public, so they fall out on their
    own.

    No longer the source of the swept set -- see the module docstring -- but still
    what pairs a parent with its children for the `Owned` check, and what proves an
    opted-out class is not quietly wired."""
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
    modules and subpackages are excluded (`_generated`, `_kernel`, `_loaded`, and any
    `_experimental` to come -- same discovery as `test_operations_coverage.py`)."""
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


def all_resource_classes() -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """Every `V2Resource` subclass in the package, migrated or not, sorted by name.

    Membership does not depend on having a `list`, on being wired, or on anything
    else a migration might not have got to yet -- which is precisely why it is the
    base of the swept set."""
    return sorted(set(_iter_resource_classes(v2_package)), key=lambda cls: cls.__name__)


def _leading_path_ids(function: Any) -> int:
    """How many positional-or-keyword parameters a method takes before its `*`."""
    return sum(
        1
        for parameter in inspect.signature(function).parameters.values()
        if parameter.kind is parameter.POSITIONAL_OR_KEYWORD and parameter.name != "self"
    )


def flat_resource_classes() -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """Classes whose `list` already consumes exactly the path ids its URL template
    names -- the mechanical signature of the flat shape, for classes that have a
    `list` at all.

    Kept as a *guard*: a class named in `UNMIGRATED_RESOURCES` that shows up here has
    been migrated and the opt-out is now stale. It is no longer used to build the
    swept set, because 18 of the 90 classes have no `list` to judge."""
    flat = []
    for resource_class in all_resource_classes():
        function = vars(resource_class).get("list")
        if not inspect.isfunction(function) or is_pending(function):
            continue
        if _leading_path_ids(function) == len(set(template_keys(resource_class.path))):
            flat.append(resource_class)
    return flat


def navigable_resource_classes() -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """Every resource whose fetches answer with a `Loaded` row -- i.e. every class
    that declares a `loaded_model`.

    The subject set of `tests/v2/test_loaded_navigation.py`: the sweep that ties a
    resource's attached children to its loaded row's navigation properties. Derived,
    not listed, for the same reason as every other set in this module -- a family
    that gains navigable rows is swept the moment it declares `loaded_model`."""
    return [cls for cls in all_resource_classes() if getattr(cls, "loaded_model", None) is not None]


def child_resources(resource: V2Resource) -> dict[str, V2Resource]:  # type: ignore[type-arg]
    """The child resources an instance attaches in its own `__init__`, by attribute
    name (`{"states": States(...), ...}`)."""
    return {
        name: value
        for name, value in vars(resource).items()
        if not name.startswith("_") and isinstance(value, V2Resource)
    }


def migrated_resource_classes() -> list[type[V2Resource]]:  # type: ignore[type-arg]
    """The set the rule sweeps run over: every resource class in the package except
    the ones explicitly opted out as still pre-flat. Sorted by name so parametrized
    ids are stable."""
    return [cls for cls in all_resource_classes() if cls.__name__ not in UNMIGRATED_RESOURCES]
