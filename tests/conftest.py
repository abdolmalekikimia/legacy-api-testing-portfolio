import httpx
import pytest

from complaint_api_testing import ComplaintApiClient


@pytest.fixture
def api():
    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path == "/auth/api/public/v1/current-user":
            return httpx.Response(200, json={"id": 2, "username": "demo-user"})
        if request.url.path == "/basic/api/genders/find-all":
            return httpx.Response(200, json=[{"id": 1, "title": "Example"}])
        if request.url.path == "/complaint/api/complaint-composite/v1/save":
            return httpx.Response(201, json={"id": 1001, "status": "CREATED"})
        return httpx.Response(404, json={"message": "not found"})

    with ComplaintApiClient(
        base_url="https://example.test",
        token="test-token",
        transport=httpx.MockTransport(handler),
    ) as client:
        yield client
