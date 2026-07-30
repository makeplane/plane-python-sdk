from pydantic import BaseModel, ConfigDict

from .enums import CatalogGroupEnum, GroupEnum
from .pagination import PaginatedResponse


class State(BaseModel):
    """State model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None
    name: str
    description: str | None = None
    color: str
    sequence: float | None = None
    group: GroupEnum | None = None
    is_triage: bool | None = None
    default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None
    created_by: str | None = None
    updated_by: str | None = None
    project: str | None = None
    workspace: str | None = None


class StateLite(BaseModel):
    """Lite state information."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str | None = None
    name: str | None = None
    color: str | None = None
    group: GroupEnum | None = None


class CreateState(BaseModel):
    """Request model for creating a state."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    description: str | None = None
    color: str
    sequence: float | None = None
    group: GroupEnum | None = None
    is_triage: bool | None = None
    default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None


class UpdateState(BaseModel):
    """Request model for updating a state."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    color: str | None = None
    sequence: float | None = None
    group: GroupEnum | None = None
    is_triage: bool | None = None
    default: bool | None = None
    external_source: str | None = None
    external_id: str | None = None


class CreateWorkspaceState(BaseModel):
    """Request model for creating a workspace (catalog) state.

    Only accepted when the workspace owns states and workflows (workspace
    governance). ``group`` is required and must be one of the five lifecycle
    groups — the triage state is system-managed and cannot be created. Catalog
    states carry no ``default`` flag; the workspace default lives on the
    workflow's default state.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str
    color: str
    group: CatalogGroupEnum
    description: str | None = None
    external_source: str | None = None
    external_id: str | None = None


class UpdateWorkspaceState(BaseModel):
    """Request model for updating a workspace (catalog) state.

    ``default`` is not accepted for catalog states — the API rejects it with
    code ``workspace_managed``.
    """

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    name: str | None = None
    color: str | None = None
    group: CatalogGroupEnum | None = None
    description: str | None = None
    external_source: str | None = None
    external_id: str | None = None


class PaginatedStateResponse(PaginatedResponse):
    """Paginated response for states."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[State]
