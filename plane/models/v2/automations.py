"""Automation models for api_v2; edited through scoped write requests
(`AutomationWriteRequest`/`AutomationNodeWriteRequest`/etc.), not one unified PATCH."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

AutomationStatus = Literal["draft", "published", "disabled"]
NodeType = Literal["trigger", "action", "condition"]


# -- Automations ----------------------------------------------------------------


class Automation(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    bot_user_id: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    current_version_id: str | None = None
    description: str | None = None
    is_enabled: bool | None = None
    is_global: bool | None = None
    last_run_at: datetime | None = None
    name: str | None = None
    project_ids: list[str] | None = None
    run_count: int | None = None
    scope: str | None = None
    """What entity this automation runs on (e.g. `"WorkItem"`, `"Cycle"`, `"Module"`)."""
    status: AutomationStatus | None = None
    updated_at: datetime | None = None


class CreateAutomation(BaseModel):
    """POST body for the automation shell. Status/enable are owned by
    `set_status`, not this DTO -- see the golden's own note on
    `AutomationWriteRequest`."""

    model_config = ConfigDict(extra="ignore")

    name: str
    scope: str
    description: str | None = None
    project_ids: list[str] | None = None


class UpdateAutomation(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    scope: str | None = None
    description: str | None = None
    project_ids: list[str] | None = None


class SetAutomationStatus(BaseModel):
    """Body for the `status` action -- the only way to enable/disable an
    automation or move it out of draft."""

    model_config = ConfigDict(extra="ignore")

    is_enabled: bool


# -- Edges ------------------------------------------------------------------------


class AutomationEdge(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    created_at: datetime | None = None
    created_by_id: str | None = None
    execution_order: int | None = None
    """Order for evaluation when multiple edges leave the same node."""
    source_node_id: str | None = None
    target_node_id: str | None = None
    updated_at: datetime | None = None
    version_id: str | None = None


class CreateAutomationEdge(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_node_id: str
    target_node_id: str
    execution_order: int | None = None


class UpdateAutomationEdge(BaseModel):
    model_config = ConfigDict(extra="ignore")

    source_node_id: str | None = None
    target_node_id: str | None = None
    execution_order: int | None = None


# -- Nodes ------------------------------------------------------------------------


class AutomationNode(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    config: Any = None
    """Node-specific configuration and parameters -- a free-form JSON blob, shape
    depends on `handler_name`; the golden declares no fixed schema for it."""
    created_at: datetime | None = None
    created_by_id: str | None = None
    handler_name: str | None = None
    """e.g. `"record_created"`, `"send_email"`."""
    is_enabled: bool | None = None
    last_triggered_at: datetime | None = None
    """Last time this scheduled trigger was dispatched."""
    name: str | None = None
    next_scheduled_at: datetime | None = None
    """Next scheduled execution time (UTC). Only for scheduled triggers."""
    node_type: NodeType | None = None
    updated_at: datetime | None = None
    version_id: str | None = None


class CreateAutomationNode(BaseModel):
    model_config = ConfigDict(extra="ignore")

    handler_name: str
    name: str
    node_type: NodeType
    config: Any = None
    is_enabled: bool | None = None


class UpdateAutomationNode(BaseModel):
    model_config = ConfigDict(extra="ignore")

    handler_name: str | None = None
    name: str | None = None
    node_type: NodeType | None = None
    config: Any = None
    is_enabled: bool | None = None


class AutomationWebhookSecret(BaseModel):
    """Response of the `regenerate_webhook_secret` action on a node. Not itself a
    row with an `id` -- the golden's own schema for it declares only `secret`."""

    model_config = ConfigDict(extra="allow")

    secret: str | None = None


# -- Activities (read-only) ------------------------------------------------------


class AutomationActivity(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    actor_id: str | None = None
    automation_edge_id: str | None = None
    automation_id: str | None = None
    automation_node_id: str | None = None
    automation_run_id: str | None = None
    automation_scope: str | None = None
    automation_version_id: str | None = None
    created_at: datetime | None = None
    epoch: float | None = None
    field: str | None = None
    new_identifier: str | None = None
    new_value: str | None = None
    node_execution_id: str | None = None
    old_identifier: str | None = None
    old_value: str | None = None
    verb: str | None = None
