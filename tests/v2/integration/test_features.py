"""Feature-toggle singletons against a real server; no gate needed since they
exist for any workspace/project. Restores whatever it flips so this suite is
safe to run repeatedly. Not verified against a live server yet.

Both singletons are reached off loaded rows, which is the point: `workspace.features`
and `project.features` are the same operation at two scopes, and they now answer to
the same verb. They did not -- `WorkspaceFeatures` spelled the read `get` while
`ProjectFeatures`, three lines below it in the same module, spelled it `retrieve`.
This file was written against `retrieve` on both and had never run.
See `tests/v2/test_singleton_verbs.py`."""

from __future__ import annotations

from plane.api.v2 import LoadedProject, LoadedWorkspace
from plane.models.v2.features import UpdateProjectFeature, UpdateWorkspaceFeature


def test_workspace_features_retrieve(workspace: LoadedWorkspace) -> None:
    feature = workspace.features.retrieve()
    assert feature.id


def test_workspace_features_round_trip_toggle(workspace: LoadedWorkspace) -> None:
    original = workspace.features.retrieve()
    original_value = bool(original.is_wiki_enabled)
    try:
        flipped = workspace.features.update(
            UpdateWorkspaceFeature(is_wiki_enabled=not original_value)
        )
        assert flipped.is_wiki_enabled is (not original_value)
    finally:
        workspace.features.update(UpdateWorkspaceFeature(is_wiki_enabled=original_value))


def test_project_features_retrieve_has_no_id(project: LoadedProject) -> None:
    feature = project.features.retrieve()
    assert not hasattr(feature, "id")


def test_project_features_round_trip_toggle(
    workspace: LoadedWorkspace,
    project: LoadedProject,
) -> None:
    # `is_epic_enabled` cannot be re-enabled at the project level once the
    # workspace owns work item types (`ProjectFeature.save()`) -- detect that
    # via the same `is_work_item_types_enabled` flag `test_work_item_types.py` guards.
    # Through the resource, not `transport.request`: a hand-rolled request skips the
    # kernel's own query validation, and this is the very singleton under test.
    workspace_owns_types = bool(workspace.features.retrieve().is_work_item_types_enabled)
    original = project.features.retrieve()
    original_value = bool(original.is_epic_enabled)
    try:
        flipped = project.features.update(UpdateProjectFeature(is_epic_enabled=not original_value))
        if workspace_owns_types:
            # Coerced back off regardless of what was requested.
            assert flipped.is_epic_enabled is False
        else:
            assert flipped.is_epic_enabled is (not original_value)
    finally:
        project.features.update(UpdateProjectFeature(is_epic_enabled=original_value))
