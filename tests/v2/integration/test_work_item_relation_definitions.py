"""Work item relation definitions against a real server; no feature gate --
this suite creates and deletes its own custom row since writes to seeded
defaults are blocked. Not verified against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2.work_item_relation_definitions import WorkItemRelationDefinitions
from plane.client import PlaneClient
from plane.models.v2.work_item_relation_definitions import (
    CreateWorkItemRelationDefinition,
    UpdateWorkItemRelationDefinition,
)

from .helpers import unique_name


@pytest.fixture(scope="module")
def relation_definitions(client: PlaneClient) -> WorkItemRelationDefinitions:
    return client.v2.workspaces.work_item_relation_definitions


@pytest.fixture
def relation_definition(
    relation_definitions: WorkItemRelationDefinitions, workspace_slug: str
) -> Iterator[Any]:
    name = unique_name("relates-to")
    created = relation_definitions.create(
        workspace_slug, CreateWorkItemRelationDefinition(name=name, inward=name, outward=name)
    )
    yield created
    try:
        relation_definitions.delete(workspace_slug, created.id)
    except Exception:
        pass


def test_list_includes_seeded_defaults(
    relation_definitions: WorkItemRelationDefinitions, workspace_slug: str
) -> None:
    page = relation_definitions.list(workspace_slug)
    assert any(row.is_default for row in page.data)


def test_create_retrieve_patch_delete(
    relation_definitions: WorkItemRelationDefinitions,
    relation_definition: Any,
    workspace_slug: str,
) -> None:
    assert relation_definition.is_default is not True

    fetched = relation_definitions.retrieve(workspace_slug, relation_definition.id)
    assert fetched.id == relation_definition.id

    updated = relation_definitions.update(
        workspace_slug, relation_definition.id, UpdateWorkItemRelationDefinition(color="#abcdef")
    )
    assert updated.color == "#abcdef"


def test_find_by_name(
    relation_definitions: WorkItemRelationDefinitions,
    relation_definition: Any,
    workspace_slug: str,
) -> None:
    found = relation_definitions.find_by_name(workspace_slug, relation_definition.name)
    assert found.id == relation_definition.id
