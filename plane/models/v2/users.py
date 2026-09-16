"""Calling-principal model for api_v2 (`GET /users/me/`)."""

from __future__ import annotations

import builtins
from typing import Literal

from pydantic import BaseModel, ConfigDict

PrincipalKind = Literal["oauth", "api_key", "other"]


class WhoAmI(BaseModel):
    """The authenticated principal (API key or OAuth token, not necessarily human);
    `principal_kind`/`scopes` distinguish the two."""

    model_config = ConfigDict(extra="allow")

    id: str
    display_name: str | None = None
    email: str | None = None
    principal_kind: PrincipalKind | None = None
    scopes: builtins.list[str] | None = None
