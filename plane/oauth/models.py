from typing import Optional

from pydantic import BaseModel


class PlaneOAuthTokenResponse(BaseModel):
    access_token: str
    expires_in: Optional[int] = None
    token_type: str = "Bearer"
    scope: Optional[str] = None
    refresh_token: Optional[str] = None


class WorkspaceDetail(BaseModel):
    name: str
    slug: str
    id: str
    logo_url: Optional[str] = None


class PlaneOAuthAppInstallation(BaseModel):
    id: str
    workspace_detail: WorkspaceDetail
    created_at: str
    updated_at: str
    deleted_at: Optional[str] = None
    status: str
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    workspace: str
    application: str
    installed_by: str
    app_bot: str
    webhook: Optional[str] = None
