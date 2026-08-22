"""HTTP plumbing for api_v2: URL building, auth, retry, problem+json decoding."""

from collections.abc import Mapping
from typing import Any

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from ....config import Configuration
from .errors import PlaneAPIError

API_V2_PREFIX = "/api/v2"


class V2Transport:
    """One session shared by every v2 resource on a client."""

    def __init__(self, config: Configuration) -> None:
        self.config = config
        self.session = requests.Session()
        if config.retry:
            retry = Retry(
                total=config.retry.total,
                backoff_factor=config.retry.backoff_factor,
                status_forcelist=list(config.retry.status_forcelist),
                allowed_methods=config.retry.allowed_methods,
                respect_retry_after_header=True,
                raise_on_status=False,
            )
            adapter = HTTPAdapter(max_retries=retry)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def request(
        self,
        method: str,
        path: str,
        *,
        params: Mapping[str, Any] | None = None,
        json: Any = None,
    ) -> Any:
        response = self.session.request(
            method,
            f"{self.config.api_root}{API_V2_PREFIX}{path}",
            headers=self._headers(),
            params=params,
            json=json,
            timeout=self.config.timeout,
        )
        return self._handle(response)

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json", "Accept": "application/json"}
        if self.config.api_key:
            headers["X-Api-Key"] = self.config.api_key
        if self.config.access_token:
            headers["Authorization"] = f"Bearer {self.config.access_token}"
        return headers

    def _handle(self, response: requests.Response) -> Any:
        if response.status_code == 204 or not response.content:
            if 200 <= response.status_code < 300:
                return None
        if 200 <= response.status_code < 300:
            return response.json()
        try:
            payload: Any = response.json()
        except ValueError:
            payload = response.text
        raise PlaneAPIError.from_payload(response.status_code, payload)
