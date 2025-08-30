# coding: utf-8

"""
OAuth API helpers for Plane SDK using urllib3
"""

import base64
import json
import logging
from typing import List, Optional
from urllib.parse import urlencode

from plane.configuration import Configuration
from plane.exceptions import ApiException
from plane.api_client import ApiClient

from .models import OAuthConfig, PlaneOAuthAppInstallation, PlaneOAuthTokenResponse

logger = logging.getLogger(__name__)


class OAuthApi:
    """OAuth API helper class using urllib3."""
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    redirect_uri: Optional[str] = None
    base_url: str = "https://api.plane.so"

    def __init__(
        self,
        oauth_config: Optional[OAuthConfig] = None,
        base_url: str = "https://api.plane.so",
        configuration: Optional[Configuration] = None,
    ):
        if oauth_config:
            self.client_id = oauth_config.client_id
            self.client_secret = oauth_config.client_secret
            self.redirect_uri = oauth_config.redirect_uri
        self.base_url = base_url.rstrip("/")

        if configuration is None:
            configuration = Configuration(host=base_url)

        self.configuration = configuration
        self.api_client = ApiClient(configuration)

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
            response = self.api_client.call_api(
                "POST",
                f"{self.base_url}/auth/o/token/",
                header_params=headers,
                post_params=data,
            )
            response.read()
            json_response = json.loads(response.data)

            return PlaneOAuthTokenResponse.model_validate(json_response)

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
            response = self.api_client.call_api(
                "POST",
                f"{self.base_url}/auth/o/token/",
                header_params=headers,
                post_params=data,
            )
            response.read()
            json_response = json.loads(response.data)

            return PlaneOAuthTokenResponse.model_validate(json_response)

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
            response = self.api_client.call_api(
                "POST",
                f"{self.base_url}/auth/o/token/",
                header_params=headers,
                post_params=data,
            )
            response.read()
            json_response = json.loads(response.data)

            return PlaneOAuthTokenResponse.model_validate(json_response)

        except ApiException as e:
            logger.error(f"Failed to get bot token: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during bot token request: {e}")
            raise ApiException(status=0, reason=str(e))

    def get_app_installations(
        self, token: str, app_installation_id: Optional[str] = None
    ) -> List[PlaneOAuthAppInstallation]:
        """Get an app installation by ID using the bot token.
        For token, use the bot token from the get_bot_token method.
        """
        try:
            headers = {
                "Authorization": f"Bearer {token}",
            }
            path = f"{self.base_url}/auth/o/app-installation/"
            if app_installation_id:
                path += f"?id={app_installation_id}"
            response = self.api_client.call_api(
                "GET",
                path,
                header_params=headers,
            )
            response.read()
            json_response = json.loads(response.data)
            return [
                PlaneOAuthAppInstallation.model_validate(item)
                for item in json_response
            ]

        except ApiException as e:
            logger.error(f"Failed to get app installation: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during app installation request: {e}")
            raise

    def _get_basic_auth_token(self) -> str:
        """Generate basic auth token from client_id and client_secret."""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return encoded_credentials
