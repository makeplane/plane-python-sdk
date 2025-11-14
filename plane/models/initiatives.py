from pydantic import BaseModel, ConfigDict

from .enums import InitiativeState


class Initiative(BaseModel):
    """Initiative model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    description: str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: bytes | None = None
    start_date: str | None = None
    end_date: str | None = None
    logo_props: dict
    state: InitiativeState | None = None
    lead: str | None = None
    workspace: str
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


class CreateInitiative(BaseModel):
    """Create initiative model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str
    description_html: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    logo_props: dict | None = None
    state: InitiativeState | None = None
    lead: str | None = None


class UpdateInitiative(BaseModel):
    """Update initiative model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    description_html: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    logo_props: dict | None = None
    state: InitiativeState | None = None
    lead: str | None = None


class PaginatedInitiativeResponse(BaseModel):
    """Paginated initiative response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Initiative]


class InitiativeLabel(BaseModel):
    """Initiative label model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    description: str | None = None
    color: str | None = None
    sort_order: float | None = None
    workspace: str
    created_at: str | None = None
    updated_at: str | None = None
    deleted_at: str | None = None


class CreateInitiativeLabel(BaseModel):
    """Create initiative label model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str
    description: str | None = None
    color: str | None = None
    sort_order: float | None = None


class UpdateInitiativeLabel(BaseModel):
    """Update initiative label model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    description: str | None = None
    color: str | None = None
    sort_order: float | None = None


class PaginatedInitiativeLabelResponse(BaseModel):
    """Paginated initiative label response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[InitiativeLabel]
