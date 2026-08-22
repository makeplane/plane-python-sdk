"""Collection models for api_v2 -- named groups of workspace pages; `CreateCollection.name` is
optional, matching the golden's write schema."""

from __future__ import annotations

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict

CollectionAccess = Literal[0, 1]  # 0 = Public, 1 = Private
CollectionMemberAccess = Literal[0, 1, 2]  # 0 = View, 1 = Comment, 2 = Edit
CollectionMemberSource = Literal["manual", "group_sync"]


class Collection(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str
    access: CollectionAccess | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    is_default: bool | None = None
    is_global: bool | None = None
    logo_props: dict[str, object] | None = None
    name: str | None = None
    owned_by_id: str | None = None
    page_ids: list[str] | None = None
    sort_order: float | None = None


class CreateCollection(BaseModel):
    """POST body. See the module docstring: the golden requires nothing here."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    access: CollectionAccess | None = None
    is_default: bool | None = None
    is_global: bool | None = None
    logo_props: dict[str, object] | None = None
    sort_order: float | None = None


class UpdateCollection(BaseModel):
    """PATCH body -- every field optional. v2 has no PUT."""

    model_config = ConfigDict(extra="ignore")

    name: str | None = None
    access: CollectionAccess | None = None
    is_default: bool | None = None
    is_global: bool | None = None
    logo_props: dict[str, object] | None = None
    sort_order: float | None = None


# -- Members ----------------------------------------------------------------------


class CollectionMember(BaseModel):
    """Sparse collection membership row -- `member_id` + access level."""

    model_config = ConfigDict(extra="allow")

    id: str
    access: CollectionMemberAccess | None = None
    collection_id: str | None = None
    created_at: datetime | None = None
    created_by_id: str | None = None
    member_id: str | None = None
    source: CollectionMemberSource | None = None


class CollectionMemberAdd(BaseModel):
    """One `add` entry for `CollectionMembers.manage` -- `member_id` plus an
    optional access level (defaults to View server-side)."""

    model_config = ConfigDict(extra="ignore")

    member_id: str
    access: CollectionMemberAccess | None = None


class CollectionMembersManage(BaseModel):
    """POST body for `.../collections/{id}/members/` (O5-style): `add` grants
    (or updates) listed workspace members; `remove` drops them by member id.
    Re-adding an existing member with a different `access` updates that row."""

    model_config = ConfigDict(extra="ignore")

    add: list[CollectionMemberAdd] | None = None
    remove: list[str] | None = None


class CollectionMembersManageResult(BaseModel):
    """Member user ids actually added/updated and removed (idempotent no-ops
    omitted from `removed`)."""

    model_config = ConfigDict(extra="allow")

    added: list[str] = []
    removed: list[str] = []


# -- Pages --------------------------------------------------------------------------


class CollectionPagesManage(BaseModel):
    """POST body for `.../collections/{id}/pages/`: page ids to add/remove."""

    model_config = ConfigDict(extra="ignore")

    add: list[str] | None = None
    remove: list[str] | None = None


class CollectionPagesManageResult(BaseModel):
    model_config = ConfigDict(extra="allow")

    added: list[str] = []
    removed: list[str] = []


class CollectionPageSearch(BaseModel):
    """Lite page shape returned by `CollectionPages.search`."""

    model_config = ConfigDict(extra="allow")

    id: str
    logo_props: dict[str, object] | None = None
    name: str | None = None
