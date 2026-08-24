from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any

import httpx


@dataclass(frozen=True)
class Endpoint:
    method: str
    path: str


ENDPOINTS = {
    "login": Endpoint("POST", "/auth/api/public/v1/login"),
    "current_user": Endpoint("GET", "/auth/api/public/v1/current-user"),
    "genders": Endpoint("GET", "/basic/api/genders/find-all"),
    "locations": Endpoint("GET", "/basic/api/locations/find-all"),
    "save_complaint": Endpoint("POST", "/complaint/api/complaint-composite/v1/save"),
    "committee_calendar": Endpoint(
        "GET", "/organization/api/committee-calendar/v1/find-by-committeeId"
    ),
    "branches": Endpoint("GET", "/tamin/api/branch/find-branches-by-location-and-zone"),
}


class ComplaintApiClient:
    """Small, dependency-injectable client used by tests and examples."""

    def __init__(
        self,
        base_url: str | None = None,
        token: str | None = None,
        transport: httpx.BaseTransport | None = None,
    ) -> None:
        self.base_url = (base_url or os.getenv("API_BASE_URL", "http://127.0.0.1:8000")).rstrip("/")
        self.token = token if token is not None else os.getenv("API_TOKEN", "")
        self._client = httpx.Client(
            base_url=self.base_url,
            transport=transport,
            headers=self._headers(),
            timeout=10.0,
        )

    def _headers(self) -> dict[str, str]:
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def request(self, endpoint: Endpoint, **kwargs: Any) -> httpx.Response:
        return self._client.request(endpoint.method, endpoint.path, **kwargs)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "ComplaintApiClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
