"""Feature-toggle singletons against a real server; no gate needed since they
exist for any workspace/project. Restores whatever it flips so this suite is
safe to run repeatedly. Not verified against a live server yet."""

from __future__ import annotations

import pytest

from plane.api.v2.features import ProjectFeatures, WorkspaceFeatures
from plane.client import PlaneClient
from plane.models.v2.features import UpdateProjectFeature, UpdateWorkspaceFeature


@pytest.fixture(scope="module")
def workspace_features(client: PlaneClient, workspace_slug: str) -> WorkspaceFeatures:
    return client.v2.workspace(workspace_slug).features


@pytest.fixture(scope="module")
def project_features(client: PlaneClient, workspace_slug: str, project_id: str) -> ProjectFeatures:
    return client.v2.workspace(workspace_slug).project(project_id).features


def test_workspace_features_retrieve(workspace_features: WorkspaceFeatures) -> None:
    feature = workspace_features.retrieve()
    assert feature.id


def test_workspace_features_round_trip_toggle(workspace_features: WorkspaceFeatures) -> None:
    original = workspace_features.retrieve()
    original_value = bool(original.is_wiki_enabled)
    try:
        flipped = workspace_features.update(
            UpdateWorkspaceFeature(is_wiki_enabled=not original_value)
        )
        assert flipped.is_wiki_enabled is (not original_value)
    finally:
        workspace_features.update(UpdateWorkspaceFeature(is_wiki_enabled=original_value))


def test_project_features_retrieve_has_no_id(project_features: ProjectFeatures) -> None:
    feature = project_features.retrieve()
    assert not hasattr(feature, "id")


def test_project_features_round_trip_toggle(
    client: PlaneClient,
    project_features: ProjectFeatures,
    workspace_slug: str,
) -> None:
    # `is_epic_enabled` cannot be re-enabled at the project level once the
    # workspace owns work item types (`ProjectFeature.save()`) -- detect that
    # via the same `is_work_item_types_enabled` flag `test_work_item_types.py` guards.
    workspace_owns_types = bool(
        client.v2.transport.request("GET", f"/workspaces/{workspace_slug}/features/").get(
            "is_work_item_types_enabled"
        )
    )
    original = project_features.retrieve()
    original_value = bool(original.is_epic_enabled)
    try:
        flipped = project_features.update(UpdateProjectFeature(is_epic_enabled=not original_value))
        if workspace_owns_types:
            # Coerced back off regardless of what was requested.
            assert flipped.is_epic_enabled is False
        else:
            assert flipped.is_epic_enabled is (not original_value)
    finally:
        project_features.update(UpdateProjectFeature(is_epic_enabled=original_value))
