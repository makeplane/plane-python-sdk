"""Customer properties against a real server; requires the workspace's
`is_customer_enabled` feature flag, else the endpoint 403s/404s. Not
verified against a live server yet."""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any

import pytest

from plane.api.v2 import LoadedWorkspace
from plane.models.v2.customer_properties import CreateCustomerProperty, UpdateCustomerProperty

from .helpers import unique_name


@pytest.fixture
def property_row(workspace: LoadedWorkspace) -> Iterator[Any]:
    created = workspace.customer_properties.create(
        CreateCustomerProperty(display_name=unique_name("tier"), property_type="TEXT")
    )
    yield created
    try:
        workspace.customer_properties.delete(created.id)
    except Exception:
        pass


def test_list(workspace: LoadedWorkspace) -> None:
    page = workspace.customer_properties.list()
    assert isinstance(page.data, list)


def test_create_retrieve_patch_delete(
    workspace: LoadedWorkspace, property_row: Any
) -> None:
    fetched = workspace.customer_properties.retrieve(property_row.id)
    assert fetched.property_type == "TEXT"

    updated = workspace.customer_properties.update(property_row.id, UpdateCustomerProperty(is_active=False))
    assert updated.is_active is False


def test_sparse_fields(workspace: LoadedWorkspace, property_row: Any) -> None:
    fetched = workspace.customer_properties.retrieve(property_row.id, fields=["id"])
    assert fetched.id == property_row.id
    assert fetched.display_name is None
