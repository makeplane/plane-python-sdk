"""Audit log models for api_v2."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict

ActorType = Literal["user", "api_token", "system", "anonymous"]
AuditCategory = Literal[
    "auth",
    "member",
    "role",
    "settings",
    "integration",
    "webhook",
    "security",
    "instance",
    "project",
]
AuditOutcome = Literal["success", "failure"]
AuditLogSource = Literal["platform", "api", "graphql", "auth", "system"]


class AuditLog(BaseModel):
    """A workspace audit-log entry; read-only, every field but `id` optional, hash-chain internals
    omitted."""

    model_config = ConfigDict(extra="allow")

    id: str
    actor_display_name: str | None = None
    actor_email: str | None = None
    actor_id: str | None = None
    actor_type: ActorType | None = None
    category: AuditCategory | None = None
    created_at: datetime | None = None
    event_id: str | None = None
    event_name: str | None = None
    ip_address: str | None = None
    metadata: Any | None = None
    new_value: Any | None = None
    old_value: Any | None = None
    outcome: AuditOutcome | None = None
    project_id: str | None = None
    reason: str | None = None
    sequence_number: int | None = None
    source: AuditLogSource | None = None
    target_display_name: str | None = None
    target_id: str | None = None
    target_type: str | None = None
    user_agent: str | None = None
    workspace_id: str | None = None
