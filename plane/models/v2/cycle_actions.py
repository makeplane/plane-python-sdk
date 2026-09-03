"""Models for the two cycle custom actions out of scope of `plane.models.v2.cycles`
(`transfer` and the `.work_items` bridge -- see `plane/api/v2/cycles.py`'s docstring)."""

from pydantic import BaseModel, ConfigDict, Field


class CycleTransfer(BaseModel):
    """POST body for `.../cycles/{id}/transfer/` -- move the source cycle's
    incomplete work items into `new_cycle_id` (the source cycle must already be
    completed)."""

    model_config = ConfigDict(extra="ignore")

    new_cycle_id: str


class CycleTransferResult(BaseModel):
    """Response of `transfer` -- echoes back the destination cycle id."""

    model_config = ConfigDict(extra="allow")

    new_cycle_id: str | None = None


class CycleWorkItemManage(BaseModel):
    """POST body for `.../cycles/{id}/work-items/` -- bulk set-style membership:
    `add` moves the listed work items into this cycle (re-homing from any other
    cycle), `remove` takes them out. Both optional; provide at least one."""

    model_config = ConfigDict(extra="ignore")

    add: list[str] | None = Field(default=None, max_length=100)
    remove: list[str] | None = Field(default=None, max_length=100)


class CycleWorkItemManageResult(BaseModel):
    """Response of the `.work_items` bridge (`add`/`remove`) -- the work item ids actually added and
    removed (idempotent no-ops are omitted)."""

    model_config = ConfigDict(extra="allow")

    added: list[str] | None = None
    removed: list[str] | None = None
