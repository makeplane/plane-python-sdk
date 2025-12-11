from __future__ import annotations

from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict


class AgentRunStatus(str, Enum):
    """Agent run status enum."""

    CREATED = "created"
    IN_PROGRESS = "in_progress"
    AWAITING = "awaiting"
    COMPLETED = "completed"
    STOPPING = "stopping"
    STOPPED = "stopped"
    FAILED = "failed"
    STALE = "stale"


class AgentRunType(str, Enum):
    """Agent run type enum."""

    COMMENT_THREAD = "comment_thread"


class AgentRunActivitySignal(str, Enum):
    """Agent run activity signal enum."""

    AUTH_REQUEST = "auth_request"
    CONTINUE = "continue"
    SELECT = "select"
    STOP = "stop"


class AgentRunActivityType(str, Enum):
    """Agent run activity type enum."""

    ACTION = "action"
    ELICITATION = "elicitation"
    ERROR = "error"
    PROMPT = "prompt"
    RESPONSE = "response"
    THOUGHT = "thought"


class AgentRun(BaseModel):
    """Agent Run model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    agent_user: str
    comment: str | None = None
    source_comment: str | None = None
    creator: str
    stopped_at: str | None = None
    stopped_by: str | None = None
    started_at: str
    ended_at: str | None = None
    external_link: str | None = None
    issue: str | None = None
    workspace: str
    project: str | None = None
    status: AgentRunStatus
    error_metadata: dict[str, Any] | None = None
    type: AgentRunType
    created_at: str | None = None
    updated_at: str | None = None


class CreateAgentRun(BaseModel):
    """Create agent run request model."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    agent_slug: str
    issue: str | None = None
    project: str | None = None
    comment: str | None = None
    source_comment: str | None = None
    external_link: str | None = None
    type: AgentRunType | None = None


class AgentRunActivityActionContent(BaseModel):
    """Agent run activity content for action type."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: Literal["action"]
    action: str
    parameters: dict[str, str]


class AgentRunActivityTextContent(BaseModel):
    """Agent run activity content for non-action types."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    type: Literal["elicitation", "error", "prompt", "response", "thought"]
    body: str


AgentRunActivityContent = AgentRunActivityActionContent | AgentRunActivityTextContent


class AgentRunActivity(BaseModel):
    """Agent Run Activity model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    agent_run: str
    content: AgentRunActivityContent
    content_metadata: dict[str, Any] | None = None
    ephemeral: bool
    signal: AgentRunActivitySignal
    signal_metadata: dict[str, Any] | None = None
    comment: str | None = None
    actor: str | None = None
    type: AgentRunActivityType
    project: str | None = None
    workspace: str
    created_at: str | None = None
    updated_at: str | None = None


class CreateAgentRunActivity(BaseModel):
    """Create agent run activity request model."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    content: AgentRunActivityContent
    content_metadata: dict[str, Any] | None = None
    signal: AgentRunActivitySignal | None = None
    signal_metadata: dict[str, Any] | None = None
    type: Literal["action", "elicitation", "error", "response", "thought"]
    project: str | None = None


class PaginatedAgentRunActivityResponse(BaseModel):
    """Paginated agent run activity response."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[AgentRunActivity]
    next_cursor: str | None = None
    prev_cursor: str | None = None
    next_page_results: bool | None = None
    prev_page_results: bool | None = None
    count: int | None = None
    total_pages: int | None = None
    total_results: int | None = None
    extra_stats: dict[str, Any] | None = None

