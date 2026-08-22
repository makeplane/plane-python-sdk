"""Intake work item models for api_v2; named `IntakeWorkItem*` (golden's `IntakeIssue`), `status`
is an int enum (-2..2: pending/rejected/snoozed/accepted/duplicate)."""

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

IntakeWorkItemPriority = Literal["none", "low", "medium", "high", "urgent"]
IntakeWorkItemStatus = Literal[-2, -1, 0, 1, 2]


class IntakeWorkItem(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    name: str | None = None
    description_html: str | None = None
    priority: str | None = None
    status: IntakeWorkItemStatus | None = None
    snoozed_till: datetime | None = None
    duplicate_to_id: str | None = None
    source: str | None = None
    source_email: str | None = None
    state_id: str | None = None
    work_item_id: str | None = None
    intake_id: str | None = None
    external_id: str | None = None
    external_source: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None


class CreateIntakeWorkItem(BaseModel):
    """POST body. See module docstring: the golden marks every field optional here,
    though the server requires `name` to actually create a row."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description_html: str | None = None
    priority: IntakeWorkItemPriority | None = None
    status: IntakeWorkItemStatus | None = None
    snoozed_till: datetime | None = None
    duplicate_to_id: str | None = None
    source: str | None = None
    source_email: str | None = None
    external_id: str | None = None
    external_source: str | None = None


class UpdateIntakeWorkItem(BaseModel):
    """PATCH body -- every field optional. Folds v1's separate status endpoint:
    set `status`/`snoozed_till`/`duplicate_to_id` in the same call as any other
    field."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    description_html: str | None = None
    priority: IntakeWorkItemPriority | None = None
    status: IntakeWorkItemStatus | None = None
    snoozed_till: datetime | None = None
    duplicate_to_id: str | None = None
    source: str | None = None
    source_email: str | None = None
    external_id: str | None = None
    external_source: str | None = None
