"""Webhook models for api_v2."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

WebhookContentType = Literal["application/json", "application/x-www-form-urlencoded"]


class Webhook(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    content_type: WebhookContentType | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    is_active: bool | None = None
    name: str | None = None
    scopes: list[str] | None = None
    url: str | None = None
    version: str | None = None


class CreateWebhook(BaseModel):
    """POST body. The golden names no required field for `WebhookWriteRequest`,
    but `url` is what makes the call meaningful."""

    model_config = ConfigDict(extra="ignore")

    url: str | None = None
    content_type: WebhookContentType | None = None
    is_active: bool | None = None
    name: str | None = None
    scopes: list[str] | None = None
    version: str | None = None


class UpdateWebhook(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    url: str | None = None
    content_type: WebhookContentType | None = None
    is_active: bool | None = None
    name: str | None = None
    scopes: list[str] | None = None
    version: str | None = None


class WebhookCreateResult(BaseModel):
    """Response to `create`/`regenerate`; carries `secret_key` once and never again -- modeled on
    the golden's `WebhookCreateResponse` component, not independently verified live."""

    model_config = ConfigDict(extra="allow")

    id: str
    secret_key: str
    content_type: WebhookContentType | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    is_active: bool | None = None
    name: str | None = None
    scopes: list[str] | None = None
    url: str | None = None
    version: str | None = None
