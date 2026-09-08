"""Offline coverage for the two feature-toggle singletons; neither has an `id` in the URL."""

import pytest
import responses

from plane.api.v2._kernel.transport import V2Transport
from plane.api.v2.features import ProjectFeatures, WorkspaceFeatures
from plane.config import Configuration
from plane.models.v2.features import UpdateProjectFeature, UpdateWorkspaceFeature

WORKSPACE_URL = "https://api.example.com/api/v2/workspaces/acme/features/"
PROJECT_URL = "https://api.example.com/api/v2/workspaces/acme/projects/ENG/features/"


@pytest.fixture
def workspace_features(config: Configuration) -> WorkspaceFeatures:
    return WorkspaceFeatures(V2Transport(config))


@pytest.fixture
def project_features(config: Configuration) -> ProjectFeatures:
    return ProjectFeatures(V2Transport(config))


@responses.activate
def test_workspace_features_get_hits_the_bare_collection_url(
    workspace_features: WorkspaceFeatures,
) -> None:
    responses.get(WORKSPACE_URL, json={"id": "1", "is_wiki_enabled": True})

    feature = workspace_features.get("acme")

    assert responses.calls[0].request.url == WORKSPACE_URL
    assert feature.is_wiki_enabled is True


@responses.activate
def test_workspace_features_update(workspace_features: WorkspaceFeatures) -> None:
    responses.patch(WORKSPACE_URL, json={"id": "1", "is_wiki_enabled": False})

    feature = workspace_features.update("acme", UpdateWorkspaceFeature(is_wiki_enabled=False))

    assert feature.is_wiki_enabled is False


@responses.activate
def test_project_features_retrieve_has_no_id(project_features: ProjectFeatures) -> None:
    """`ProjectFeature` carries no `id` field at all in the golden."""
    responses.get(PROJECT_URL, json={"is_epic_enabled": True})

    feature = project_features.retrieve("acme", "ENG")

    assert responses.calls[0].request.url == PROJECT_URL
    assert feature.is_epic_enabled is True
    assert not hasattr(feature, "id")


@responses.activate
def test_project_features_update(project_features: ProjectFeatures) -> None:
    responses.patch(PROJECT_URL, json={"is_epic_enabled": False})

    feature = project_features.update("acme", "ENG", UpdateProjectFeature(is_epic_enabled=False))

    assert feature.is_epic_enabled is False
