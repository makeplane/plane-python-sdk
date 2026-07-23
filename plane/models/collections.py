from enum import IntEnum
from typing import Any

from pydantic import BaseModel, ConfigDict

from .pagination import PaginatedResponse


class CollectionAccessEnum(IntEnum):
    """Access level of a collection."""

    PUBLIC = 0
    PRIVATE = 1


class CollectionMemberAccessEnum(IntEnum):
    """Access level of a member within a collection."""

    VIEW = 0
    COMMENT = 1
    EDIT = 2


class Collection(BaseModel):
    """Collection model (a folder that groups workspace pages)."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    owned_by_id: str | None = None
    access: CollectionAccessEnum | None = None
    current_user_access: CollectionMemberAccessEnum | None = None
    has_pages: bool | None = None
    is_default: bool | None = None
    is_global: bool | None = None
    logo_props: Any | None = None
    sort_order: float | None = None
    workspace: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None


class CreateCollection(BaseModel):
    """Request model for creating a collection."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    access: CollectionAccessEnum | None = None
    logo_props: Any | None = None


class UpdateCollection(BaseModel):
    """Request model for updating a collection.

    Deliberately has no `access` field -- the API rejects (400) any attempt to
    change a collection's access level after creation.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    logo_props: Any | None = None
    sort_order: float | None = None


class CollectionMember(BaseModel):
    """Collection membership record."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    collection: str | None = None
    member: str | None = None
    access: CollectionMemberAccessEnum | None = None
    workspace: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None


class CreateCollectionMember(BaseModel):
    """Request model for adding a collection member."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    member: str
    access: CollectionMemberAccessEnum


class UpdateCollectionMember(BaseModel):
    """Request model for updating a collection member's access level."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    access: CollectionMemberAccessEnum


class CollectionPage(BaseModel):
    """Flat page-collection membership record, returned by the move/reorder endpoint."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    collection: str | None = None
    page: str | None = None
    workspace: str | None = None
    sort_order: float | None = None
    created_at: str | None = None
    updated_at: str | None = None
    created_by: str | None = None
    updated_by: str | None = None


class CollectionBranchPage(BaseModel):
    """A row in the list-pages-in-collection response, with a nested page object."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    page_collection_id: str | None = None
    collection_id: str | None = None
    parent_id: str | None = None
    sort_order: float | None = None
    page: dict[str, Any] | None = None


class AddCollectionPages(BaseModel):
    """Request model for adding existing page(s) to a collection."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    page_ids: list[str]
    sort_orders: dict[str, float] | None = None
    placement: dict[str, Any] | None = None


class UpdateCollectionPage(BaseModel):
    """Request model for moving/reordering a page within or between collections.

    Omit `collection` entirely (leave it unset, do not pass None) to reorder the
    page within its current collection -- setting it triggers a move to that
    target collection.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    collection: str | None = None
    sort_order: float | None = None
    placement: dict[str, Any] | None = None


class CollectionPageSearchResult(BaseModel):
    """A page eligible to be added to a collection."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    logo_props: Any | None = None


class PaginatedCollectionPageResponse(PaginatedResponse):
    """Paginated response for pages within a collection."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[CollectionBranchPage]
