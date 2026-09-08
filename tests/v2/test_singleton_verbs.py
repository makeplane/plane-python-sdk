"""Two names for one operation is one name too many.

A *singleton* resource has no primary key -- the collection URL is the row
(`/workspaces/{slug}/features/`) -- so it goes through the kernel's
`_retrieve_singleton`/`_update_singleton` pair. That is a URL-building detail. It does
not change what the operation *is*, and the read verb is `retrieve`, the same as
everywhere else in the package.

`WorkspaceFeatures` spelled it `get` while `ProjectFeatures`, in the same file, three
lines below, spelled it `retrieve` -- so `workspace.features` and `project.features`
did the same thing under different names, and a caller had to know which side of the
file they were on. `GroupSyncConfigResource` had copied the `get` spelling from the
first one.

Found refreshing the live integration suite: `test_features.py` had been written
calling `workspace_features.retrieve()`, which does not exist, and had never run. The
golden agrees with the test -- its operationIds are `workspace_features_retrieve` and
`group_sync_config_retrieve`.

`me()` is excluded on purpose. `users.me()`, `workspace.permissions.me()` and
`project.permissions.me()` do not read *the* row of a collection; they read the
caller's own, which is a different question with its own established name.
"""

from __future__ import annotations

import inspect

from .tree_walk import all_resource_classes, public_methods

CALLER_SCOPED = {"me"}
"""Reads that answer "…for whoever is asking" rather than "the one row here"."""


def _singleton_reads() -> list[tuple[type, str]]:
    """(class, method) for every method whose body reads a singleton."""
    found = []
    for resource_class in all_resource_classes():
        for name in public_methods(resource_class):
            try:
                source = inspect.getsource(getattr(resource_class, name))
            except (OSError, TypeError):  # pragma: no cover - defensive
                continue
            if "_retrieve_singleton(" in source:
                found.append((resource_class, name))
    return found


SINGLETON_READS = _singleton_reads()


def test_the_sweep_finds_the_singletons() -> None:
    assert len(SINGLETON_READS) >= 6, (
        f"only {len(SINGLETON_READS)} singleton reads found -- the derivation is broken "
        "and the sweep below is passing vacuously"
    )


def test_every_singleton_read_is_spelled_retrieve_or_me() -> None:
    offenders = sorted(
        f"{resource_class.__name__}.{name}()"
        for resource_class, name in SINGLETON_READS
        if name not in {"retrieve", *CALLER_SCOPED}
        # `list`-shaped singletons are a separate case: a collection URL that answers a
        # map or an array rather than one row (`CustomerPropertyValues`,
        # `WorkItemRelations`, `WorkItemDependencies`) is honestly a `list`.
        and name != "list"
    )

    assert offenders == [], (
        "these singleton reads use a verb of their own instead of `retrieve`, so the "
        "same operation has two names depending on which class you reached it "
        f"through: {offenders}"
    )


def test_the_two_features_singletons_agree() -> None:
    """The specific pair that diverged, pinned by name so a rename cannot silently
    reintroduce the split."""
    from plane.api.v2 import ProjectFeatures, WorkspaceFeatures

    for resource_class in (WorkspaceFeatures, ProjectFeatures):
        assert hasattr(resource_class, "retrieve"), f"{resource_class.__name__}.retrieve is gone"
        assert not hasattr(
            resource_class, "get"
        ), f"{resource_class.__name__}.get is back; one read verb, not two"


def test_a_loaded_workspace_reaches_the_renamed_verb() -> None:
    """The navigation view is a hand-written mirror of the resource's methods
    (`bind1(WorkspaceFeatures.retrieve)`), so a rename that missed it would leave the
    row reaching a method that no longer exists."""
    from plane.api.v2 import V2Namespace
    from plane.config import Configuration
    from plane.models.v2.workspaces import Workspace

    namespace = V2Namespace(Configuration(base_path="https://x", api_key="k"))
    row = Workspace.model_validate({"id": "w1", "slug": "acme"})
    workspace_row = namespace.workspaces._load(row)

    assert callable(workspace_row.features.retrieve)
