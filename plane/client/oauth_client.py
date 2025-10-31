from __future__ import annotations

from collections.abc import Mapping
from typing import Any
from urllib.parse import urlencode, urljoin

import requests
from pydantic import BaseModel, ConfigDict, Field

from ..errors import ConfigurationError, HttpError


# OAuth Models
class OAuthToken(BaseModel):
    """OAuth token response model."""

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    access_token: str
    token_type: str
    expires_in: int | None = None
    refresh_token: str | None = None
    scope: str | None = None


class OAuthAuthorizationParams(BaseModel):
    """Parameters for OAuth authorization URL generation."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    client_id: str
    redirect_uri: str
    response_type: str = "code"
    scope: str | None = Field(default="read write")
    state: str | None = None


class OAuthTokenExchangeParams(BaseModel):
    """Parameters for exchanging authorization code for token."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    client_id: str
    client_secret: str
    code: str
    redirect_uri: str
    grant_type: str = "authorization_code"


class OAuthRefreshTokenParams(BaseModel):
    """Parameters for refreshing an OAuth token."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    client_id: str
    client_secret: str
    refresh_token: str
    grant_type: str = "refresh_token"


class OAuthClientCredentialsParams(BaseModel):
    """Parameters for client credentials flow."""

    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    client_id: str
    client_secret: str
    grant_type: str = "client_credentials"
    scope: str | None = Field(default="read write")
    app_installation_id: str | None = Field(
        default=None,
        description="Include to receive a bot token for workspace app installations",
    )


# OAuth Client
class OAuthClient:
    """
    OAuth client for Plane API.

    Handles OAuth 2.0 flows including:
    - Authorization code flow
    - Client credentials flow
    - Token refresh

    Example usage for authorization code flow:
        ```python
        oauth_client = OAuthClient(
            base_url="https://api.plane.so",
            client_id="your_client_id",
            client_secret="your_client_secret"
        )

        # Get authorization URL
        auth_url = oauth_client.get_authorization_url(
            redirect_uri="https://your-app.com/callback",
            scope="read write",
            state="random_state_string"
        )

        # After user authorizes, exchange code for token
        token = oauth_client.exchange_code(
            code="authorization_code_from_callback",
            redirect_uri="https://your-app.com/callback"
        )

        # Refresh token when needed
        new_token = oauth_client.refresh_token(token.refresh_token)
        ```

    Example usage for client credentials flow:
        ```python
        oauth_client = OAuthClient(
            base_url="https://api.plane.so",
            client_id="your_client_id",
            client_secret="your_client_secret"
        )

        # Get client credentials token
        token = oauth_client.get_client_credentials_token(
            scope="read write",
            app_installation_id="workspace_app_installation_id"  # Optional
        )
        ```
    """

    def __init__(
        self,
        *,
        base_url: str,
        client_id: str,
        client_secret: str,
        timeout: float | tuple[float, float] | None = 30.0,
    ) -> None:
        """
        Initialize OAuth client.

        Args:
            base_url: Base URL of the Plane API (e.g., "https://api.plane.so")
            client_id: OAuth client ID
            client_secret: OAuth client secret
            timeout: Request timeout in seconds (default: 30.0)

        Raises:
            ConfigurationError: If required parameters are missing
        """
        if not client_id:
            raise ConfigurationError("'client_id' must be provided")
        if not client_secret:
            raise ConfigurationError("'client_secret' must be provided")

        self.base_url = base_url.rstrip("/")
        self.client_id = client_id
        self.client_secret = client_secret
        self.timeout = timeout

        # Initialize session
        self.session = requests.Session()

    def get_authorization_url(
        self,
        *,
        redirect_uri: str,
        scope: str = "read write",
        state: str | None = None,
    ) -> str:
        """
        Generate OAuth authorization URL for authorization code flow.

        Args:
            redirect_uri: URI to redirect to after authorization
            scope: Space-separated list of scopes (default: "read write")
            state: Optional state parameter for CSRF protection

        Returns:
            Authorization URL to redirect user to
        """
        params = OAuthAuthorizationParams(
            client_id=self.client_id,
            redirect_uri=redirect_uri,
            response_type="code",
            scope=scope,
            state=state,
        )

        # Build query string from non-None parameters
        query_params = {k: v for k, v in params.model_dump().items() if v is not None}
        query_string = urlencode(query_params)

        auth_url = urljoin(self.base_url, "/auth/o/authorize-app/")
        return f"{auth_url}?{query_string}"

    def exchange_code(
        self,
        *,
        code: str,
        redirect_uri: str,
    ) -> OAuthToken:
        """
        Exchange authorization code for access token.

        Args:
            code: Authorization code received from callback
            redirect_uri: Same redirect URI used in authorization request

        Returns:
            OAuthToken containing access_token, refresh_token, and other details

        Raises:
            HttpError: If token exchange fails
        """
        params = OAuthTokenExchangeParams(
            client_id=self.client_id,
            client_secret=self.client_secret,
            code=code,
            redirect_uri=redirect_uri,
            grant_type="authorization_code",
        )

        return self._request_token(params.model_dump(exclude_none=True))

    def refresh_token(self, refresh_token: str) -> OAuthToken:
        """
        Refresh an expired access token.

        Args:
            refresh_token: Refresh token from previous token response

        Returns:
            OAuthToken with new access_token and possibly new refresh_token

        Raises:
            HttpError: If token refresh fails
        """
        params = OAuthRefreshTokenParams(
            client_id=self.client_id,
            client_secret=self.client_secret,
            refresh_token=refresh_token,
            grant_type="refresh_token",
        )

        return self._request_token(params.model_dump(exclude_none=True))

    def get_client_credentials_token(
        self,
        *,
        scope: str = "read write",
        app_installation_id: str | None = None,
    ) -> OAuthToken:
        """
        Get access token using client credentials flow.

        Args:
            scope: Space-separated list of scopes (default: "read write")
            app_installation_id: Optional workspace app installation ID to receive
                                 a bot token for that installation

        Returns:
            OAuthToken containing access_token and other details

        Raises:
            HttpError: If token request fails
        """
        params = OAuthClientCredentialsParams(
            client_id=self.client_id,
            client_secret=self.client_secret,
            grant_type="client_credentials",
            scope=scope,
            app_installation_id=app_installation_id,
        )

        return self._request_token(params.model_dump(exclude_none=True))

    def revoke_token(self, token: str) -> None:
        """
        Revoke an access or refresh token.

        Args:
            token: Token to revoke (access_token or refresh_token)

        Raises:
            HttpError: If token revocation fails
        """
        url = urljoin(self.base_url, "/auth/o/revoke-token/")
        data = {
            "token": token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = self.session.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )

        if response.status_code != 200:
            self._handle_error_response(response)

    def _request_token(self, data: Mapping[str, Any]) -> OAuthToken:
        """
        Internal method to request token from OAuth endpoint.

        Args:
            data: Token request parameters

        Returns:
            OAuthToken model

        Raises:
            HttpError: If request fails
        """
        url = urljoin(self.base_url, "/auth/o/token/")
        response = self.session.post(
            url,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=self.timeout,
        )

        if 200 <= response.status_code < 300:
            return OAuthToken.model_validate(response.json())

        self._handle_error_response(response)
        # This line should never be reached due to exception above
        raise RuntimeError("Unexpected flow in _request_token")

    def _handle_error_response(self, response: requests.Response) -> None:
        """
        Handle error responses from OAuth endpoints.

        Args:
            response: HTTP response object

        Raises:
            HttpError: Always raises with error details
        """
        try:
            payload = response.json()
        except Exception:
            payload = response.text

        raise HttpError(
            f"OAuth error: HTTP {response.status_code}: {response.reason}",
            response.status_code,
            payload,
        )

    def __enter__(self) -> OAuthClient:
        """Context manager entry."""
        return self

    def __exit__(self, *args: Any) -> None:
        """Context manager exit, closes session."""
        self.session.close()

    def close(self) -> None:
        """Close the underlying HTTP session."""
        self.session.close()

