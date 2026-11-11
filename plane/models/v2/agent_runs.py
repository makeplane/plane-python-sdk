"""Agent run models for api_v2.

A run is one piece of work an agent (an installed app's bot) does in a workspace,
usually in answer to a work item comment. Its activities are the run's append-only
log: the agent's `thought`/`action`/`response`/`elicitation`/`error` output and the
`prompt` replies people send it."""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

AgentRunStatus = Literal[
    "created",
    "in_progress",
    "awaiting",
    "completed",
    "stopping",
    "stopped",
    "failed",
    "stale",
]
AgentRunType = Literal[
    "comment_thread",
    "scheduled",
    "assignment",
    "event_triggered",
    "integration_triggered",
]
AgentRunActivityType = Literal["action", "elicitation", "error", "prompt", "response", "thought"]
AgentRunActivitySignal = Literal["auth_request", "continue", "select", "stop", "upgrade"]


class AgentRun(BaseModel):
    """One agent run. Every field is read-only on the wire; `status` moves as the agent
    reports progress, a person stops the run, or the server marks it `stale`."""

    model_config = ConfigDict(extra="allow")

    id: str
    agent_user_id: str | None = None
    comment_id: str | None = None
    """The top-level comment that is the run's thread root."""
    created_at: datetime | None = None
    created_by_id: str | None = None
    creator_id: str | None = None
    credit_usage: dict[str, Any] | None = None
    ended_at: datetime | None = None
    error_metadata: dict[str, Any] | None = None
    external_link: str | None = None
    external_trigger_id: str | None = None
    external_trigger_source: str | None = None
    native_agent_id: str | None = None
    project_id: str | None = None
    source_comment_id: str | None = None
    started_at: datetime | None = None
    status: AgentRunStatus | None = None
    stopped_at: datetime | None = None
    stopped_by_id: str | None = None
    summary: str | None = None
    title: str | None = None
    token_usage: dict[str, Any] | None = None
    trigger_type: str | None = None
    type: AgentRunType | None = None
    updated_at: datetime | None = None
    updated_by_id: str | None = None
    work_item_id: str | None = None


class CreateAgentRun(BaseModel):
    """POST body: start a run of the agent `agent_slug` (its app's slug) on a top-level
    comment. The run takes its work item and project from the comment; the server sets
    the creator and resolves the agent's bot user."""

    model_config = ConfigDict(extra="ignore")

    agent_slug: str = Field(min_length=1)
    comment_id: str
    title: str | None = None
    summary: str | None = None
    external_link: str | None = None


class UpdateAgentRun(BaseModel):
    """PATCH body. Only the run's own agent (a bot token) may send it: the agent settles
    its run with `status="completed"` and reports its title, summary and usage. A person
    ends a run with `stop` instead."""

    model_config = ConfigDict(extra="ignore")

    title: str | None = None
    summary: str | None = None
    token_usage: dict[str, Any] | None = None
    credit_usage: dict[str, Any] | None = None
    status: Literal["completed"] | None = None


class AgentRunActivity(BaseModel):
    """One entry in a run's activity log.

    `content` is the activity's payload: `{"type": <type>, "body": <text>}` for every
    type but `action`, which is `{"type": "action", "action": <name>, "parameters":
    {...}}`. `content_metadata` is stored and echoed verbatim."""

    model_config = ConfigDict(extra="allow")

    id: str
    actor_id: str | None = None
    agent_run_id: str | None = None
    comment_id: str | None = None
    """The work item comment this activity was mirrored to, if any."""
    content: dict[str, Any] | None = None
    content_metadata: dict[str, Any] | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    ephemeral: bool | None = None
    project_id: str | None = None
    signal: AgentRunActivitySignal | None = None
    signal_metadata: dict[str, Any] | None = None
    type: AgentRunActivityType | None = None
    updated_at: datetime | None = None
    updated_by_id: str | None = None


class CreateAgentRunActivity(BaseModel):
    """POST body. Who posts decides what may be posted:

    - the run's agent (a bot token) posts its output -- `thought`, `action`, `response`,
      `elicitation` or `error` -- and may set `signal`, `ephemeral` and `comment_id`;
    - a person may only reply with a `prompt` (`content={"type": "prompt", "body": ...}`),
      with no signal, not ephemeral and no `comment_id`: the server mirrors the prompt
      into the work item's thread itself. To end a run, a person calls `stop`.

    `content_metadata` is stored and echoed verbatim, so a client can tag an activity
    (an idempotency key, say) and match on it later."""

    model_config = ConfigDict(extra="ignore")

    type: AgentRunActivityType
    content: dict[str, Any] | None = None
    content_metadata: dict[str, Any] | None = None
    ephemeral: bool | None = None
    signal: AgentRunActivitySignal | None = None
    signal_metadata: dict[str, Any] | None = None
    comment_id: str | None = None


class AgentRunLite(BaseModel):
    """The run a comment is the thread root of, as `expand=["agent_run"]` returns it on a
    work item comment."""

    model_config = ConfigDict(extra="allow")

    id: str
    status: AgentRunStatus | None = None
    agent_user_id: str | None = None
    native_agent_id: str | None = None
