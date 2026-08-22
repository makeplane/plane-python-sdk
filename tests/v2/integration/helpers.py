"""Harness shared by CRUD-style tests across states/labels/cycles/modules/milestones
via `SPECS`. `CONVERTED_SPECS` is the subset whose bound, zero-argument methods
actually work live today; the rest still take `(workspace_slug, project, ...)`."""

from __future__ import annotations

import uuid
from dataclasses import dataclass
from typing import Any

from plane.models.v2.cycles import CreateCycle, Cycle, UpdateCycle
from plane.models.v2.labels import CreateLabel, Label, UpdateLabel
from plane.models.v2.milestones import CreateMilestone, Milestone, UpdateMilestone
from plane.models.v2.modules import CreateModule, Module, UpdateModule
from plane.models.v2.states import CreateState, State, UpdateState

DEFAULT_COLOR = "#336699"


def unique_name(prefix: str) -> str:
    """Unique name; state/label names are unique per project
    (case-sensitively) on the server."""
    return f"{prefix}-{uuid.uuid4().hex[:10]}"


@dataclass(frozen=True)
class ResourceSpec:
    """Everything a generic test needs to drive one v2 resource by name."""

    key: str  # attribute name on `Project` (see `ResourceSpec.ops`)
    write_model: type[Any]
    patch_model: type[Any]
    read_model: type[Any]
    name_field: str = "name"  # the write/read model's own identifying field
    has_color: bool = False  # only states/labels carry a `color` field
    converted: bool = True  # False for cycles/modules/milestones -- see module docstring

    def make_write(self, name: str, **overrides: Any) -> Any:
        body: dict[str, Any] = {self.name_field: name}
        if self.has_color:
            body["color"] = DEFAULT_COLOR
        body.update(overrides)
        return self.write_model(**body)

    def make_patch(self, **fields: Any) -> Any:
        return self.patch_model(**fields)

    def make_patch_name(self, value: str) -> Any:
        """A patch that renames the row, whatever the underlying field is called."""
        return self.patch_model(**{self.name_field: value})

    def ops(self, client: Any, workspace_slug: str, project: str) -> Any:
        """The chained resource for this spec -- the only way to reach it now
        that the flat form is gone. `project` accepts a project id or its key."""
        scope = client.v2.workspace(workspace_slug).project(project)
        return getattr(scope, self.key)


SPECS: dict[str, ResourceSpec] = {
    "states": ResourceSpec(
        key="states",
        write_model=CreateState,
        patch_model=UpdateState,
        read_model=State,
        has_color=True,
    ),
    "labels": ResourceSpec(
        key="labels",
        write_model=CreateLabel,
        patch_model=UpdateLabel,
        read_model=Label,
        has_color=True,
    ),
    "cycles": ResourceSpec(
        key="cycles",
        write_model=CreateCycle,
        patch_model=UpdateCycle,
        read_model=Cycle,
        converted=False,
    ),
    "modules": ResourceSpec(
        key="modules",
        write_model=CreateModule,
        patch_model=UpdateModule,
        read_model=Module,
        converted=False,
    ),
    "milestones": ResourceSpec(
        key="milestones",
        write_model=CreateMilestone,
        patch_model=UpdateMilestone,
        read_model=Milestone,
        name_field="title",
        converted=False,
    ),
}

# The subset whose classes have actually dropped `(workspace_slug, project, ...)`
# from every method (this phase's exemplars) -- `ops()` only works zero-argument
# for these today. C1 should widen this set as it converts cycles/modules/milestones.
CONVERTED_SPECS: dict[str, ResourceSpec] = {k: v for k, v in SPECS.items() if v.converted}
