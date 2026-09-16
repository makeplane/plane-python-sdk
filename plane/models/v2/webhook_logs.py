"""Webhook delivery log models for api_v2."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict


class WebhookLog(BaseModel):
    """A webhook delivery attempt (`WebhookEvent`); read-only, every field but `id` optional."""

    model_config = ConfigDict(extra="allow")

    id: str
    created_at: datetime | None = None
    duration_ms: int | None = None
    error_message: str | None = None
    event_type: str | None = None
    request_body: str | None = None
    request_headers: str | None = None
    request_method: str | None = None
    response_body: str | None = None
    response_headers: str | None = None
    response_status: str | None = None
    retry_count: int | None = None
    status_text: str | None = None
    webhook_id: str | None = None
