"""`PendingMigration.__getattr__` must let Python's own dunder protocol probes
through as `AttributeError`, not swallow them into `NotImplementedError`.

A loaded row (`LoadedProject`, `LoadedWorkItem`, ...) holds placeholders among its
live child resources (`WorkItems.attachments` and friends), so `copy.deepcopy` and
pydantic's `model_copy(deep=True)` -- both of which probe dunders like
`__deepcopy__`/`__reduce_ex__` while walking an object graph -- used to blow up the
moment they reached one, with a `NotImplementedError` naming an unrelated resource
instead of copying normally."""

from __future__ import annotations

import copy

import pytest
import responses

from plane.api.v2 import V2Namespace
from plane.api.v2._kernel.pending import PendingMigration
from plane.config import Configuration


def test_dunder_probe_raises_attribute_error_not_not_implemented_error() -> None:
    placeholder = PendingMigration("WorkItemAttachments", reached_as="work_items.attachments")

    with pytest.raises(AttributeError) as raised:
        _ = placeholder.__deepcopy__

    assert not isinstance(raised.value, NotImplementedError)


def test_bare_placeholder_is_deepcopyable() -> None:
    placeholder = PendingMigration("WorkItemAttachments", reached_as="work_items.attachments")

    copied = copy.deepcopy(placeholder)

    assert copied._resource == "WorkItemAttachments"
    assert copied._reached_as == "work_items.attachments"


def test_touching_a_real_placeholder_attribute_still_raises_not_implemented_error() -> None:
    placeholder = PendingMigration("WorkItemAttachments", reached_as="work_items.attachments")

    with pytest.raises(NotImplementedError, match="WorkItemAttachments"):
        _ = placeholder.list


@responses.activate
def test_deepcopy_succeeds_on_a_loaded_row_holding_placeholder_children(
    config: Configuration,
) -> None:
    """Regression repro: `project.work_items` wires seven children, six of them
    `PendingMigration` placeholders (`.attachments`, `.links`, ...); `copy.deepcopy`
    walking the fetched row's `_resources` used to reach one and raise
    `NotImplementedError` instead of copying."""
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Engineering"},
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")

    copied = copy.deepcopy(project)

    assert copied.name == "Engineering"


@responses.activate
def test_model_copy_deep_succeeds_on_a_loaded_row_holding_placeholder_children(
    config: Configuration,
) -> None:
    responses.get(
        "https://api.example.com/api/v2/workspaces/acme/projects/ENG/",
        json={"id": "p1", "identifier": "ENG", "name": "Engineering"},
    )

    project = V2Namespace(config).workspaces.projects.retrieve("acme", "ENG")

    copied = project.model_copy(deep=True)

    assert copied.name == "Engineering"
