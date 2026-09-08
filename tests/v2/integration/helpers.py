"""Harness shared by CRUD-style tests across states/labels/cycles/modules/milestones
via `SPECS`.

All five families are children of `Projects`, so each is reachable **both ways in**,
and a `ResourceSpec` offers one accessor per way:

* `spec.flat(client)` -- the static tree (`client.v2.workspaces.projects.states`).
  Every call carries `(slug, project, ...)` itself, so the caller chooses what to put
  in the project slot. That is the only way to express the uuid-vs-key parity checks
  (`test_crud.py`, `test_scope_parity.py`): a project id and its identifier must
  address the same rows.
* `spec.on(project)` -- navigation off a `LoadedProject`, zero ids repeated
  (`project.states.list()`). Used by `test_find_one`/`test_upsert`/`test_bulk`/
  `test_errors`/`test_pagination`, so the loaded-row half of the surface is exercised
  against a real server by the same generic scenarios, not just by hand-written
  one-offs.

`spec.on` cannot serve the parity checks: `Projects._row_id` is `identifier`, so a row
fetched by uuid still binds its children with the identifier. Which is the right
behaviour, and exactly why the two accessors are not interchangeable.

Both return `Any`: the attribute is chosen by name at runtime, so this is the one
corner of the suite `tests/v2/test_integration_surface.py` cannot type-check. Keep it
thin for that reason -- the parametrized scenarios stay generic, and anything worth
checking statically gets a hand-written call site elsewhere.
"""

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

    def flat(self, client: Any) -> Any:
        """This spec's resource on the static tree. Every call takes `(slug, project,
        ...)`, and the project slot accepts a project id or its identifier."""
        return getattr(client.v2.workspaces.projects, self.key)

    def on(self, project: Any) -> Any:
        """This spec's resource reached off a fetched `LoadedProject` -- the loaded-row
        way in, with the workspace and project ids already bound."""
        return getattr(project, self.key)


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
    ),
    "modules": ResourceSpec(
        key="modules",
        write_model=CreateModule,
        patch_model=UpdateModule,
        read_model=Module,
    ),
    "milestones": ResourceSpec(
        key="milestones",
        write_model=CreateMilestone,
        patch_model=UpdateMilestone,
        read_model=Milestone,
        name_field="title",
    ),
}