# coding: utf-8

"""
OAuth API helpers for Plane SDK using urllib3
"""

import base64
import json
import logging
from typing import Optional
from urllib.parse import urlencode

from plane.configuration import Configuration
from plane.exceptions import ApiException
from plane.rest import RESTClientObject

from .models import PlaneOAuthAppInstallation, PlaneOAuthTokenResponse

logger = logging.getLogger(__name__)


class OAuthApi:
    """OAuth API helper class using urllib3."""

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        base_url: str = "https://api.plane.so",
        configuration: Optional[Configuration] = None,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.base_url = base_url.rstrip("/")

        if configuration is None:
            configuration = Configuration(host=base_url)

        self.configuration = configuration
        self.rest_client = RESTClientObject(configuration)

    def get_authorization_url(
        self,
        response_type: str = "code",
        state: Optional[str] = None,
    ) -> str:
        """Get the authorization URL for the OAuth flow."""
        params = {
            "client_id": self.client_id,
            "response_type": response_type,
            "redirect_uri": self.redirect_uri,
        }

        if state:
            params["state"] = state

        return f"{self.base_url}/auth/o/authorize-app/?{urlencode(params)}"

    def exchange_code_for_token(
        self, code: str, grant_type: str = "authorization_code"
    ) -> PlaneOAuthTokenResponse:
        """Exchange authorization code for access token."""
        data = {
            "grant_type": grant_type,
            "code": code,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "redirect_uri": self.redirect_uri,
        }

        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = self.rest_client.post_request(
                url=f"{self.base_url}/auth/o/token/", headers=headers, post_params=data
            )

            response_data = json.loads(response.data.decode("utf-8"))
            return PlaneOAuthTokenResponse.validate(response_data)

        except ApiException as e:
            logger.error(f"Failed to exchange code for token: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during token exchange: {e}")
            raise ApiException(status=0, reason=str(e))

    def get_refresh_token(self, refresh_token: str) -> PlaneOAuthTokenResponse:
        """Get a new access token using a refresh token."""
        data = {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        try:
            response = self.rest_client.post_request(
                url=f"{self.base_url}/auth/o/token/", headers=headers, post_params=data
            )

            response_data = json.loads(response.data.decode("utf-8"))
            return PlaneOAuthTokenResponse.validate(response_data)

        except ApiException as e:
            logger.error(f"Failed to refresh token: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during token refresh: {e}")
            raise ApiException(status=0, reason=str(e))

    def get_bot_token(self, app_installation_id: str) -> PlaneOAuthTokenResponse:
        """Get a new access token using client credentials for bot/app installations."""
        data = {
            "grant_type": "client_credentials",
            "app_installation_id": app_installation_id,
        }

        headers = {
            "Cache-Control": "no-cache",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {self._get_basic_auth_token()}",
        }

        try:
            response = self.rest_client.post_request(
                url=f"{self.base_url}/auth/o/token/", headers=headers, post_params=data
            )

            response_data = json.loads(response.data.decode("utf-8"))
            return PlaneOAuthTokenResponse.validate(response_data)

        except ApiException as e:
            logger.error(f"Failed to get bot token: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during bot token request: {e}")
            raise ApiException(status=0, reason=str(e))

    def get_app_installation(
        self, token: str, app_installation_id: str
    ) -> PlaneOAuthAppInstallation:
        """Get an app installation by ID using the bot token.
        For token, use the bot token from the get_bot_token method.
        """
        try:
            headers = {
                "Authorization": f"Bearer {token}",
            }
            response = self.rest_client.get_request(
                url=f"{self.base_url}/auth/o/app-installation/?id={app_installation_id}",
                headers=headers,
            )
            if not response.data:
                raise ApiException(status=404, reason="App installation not found")
            return PlaneOAuthAppInstallation.validate(json.loads(response.data)[0])
        except ApiException as e:
            logger.error(f"Failed to get app installation: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during app installation request: {e}")

    def _get_basic_auth_token(self) -> str:
        """Generate basic auth token from client_id and client_secret."""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return encoded_credentials
