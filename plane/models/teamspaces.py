from pydantic import BaseModel, ConfigDict


class Teamspace(BaseModel):
    """Teamspace model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    id: str
    name: str
    description_json: dict | str | None = None
    description_html: str | None = None
    description_stripped: str | None = None
    description_binary: bytes | None = None
    logo_props: dict | None = None
    lead: str | None = None
    workspace: str
    created_at: str
    updated_at: str
    deleted_at: str | None = None


class CreateTeamspace(BaseModel):
    """Create teamspace model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str
    description_html: str | None = None
    logo_props: dict | None = None
    lead: str | None = None


class UpdateTeamspace(BaseModel):
    """Update teamspace model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    name: str | None = None
    description_html: str | None = None
    logo_props: dict | None = None
    lead: str | None = None


class PaginatedTeamspaceResponse(BaseModel):
    """Paginated teamspace response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    results: list[Teamspace]
