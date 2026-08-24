import httpx

from complaint_api_testing.client import ENDPOINTS


def test_client_sends_bearer_token_and_parses_current_user(api):
    response = api.request(ENDPOINTS["current_user"])

    assert response.status_code == 200
    assert response.json()["username"] == "demo-user"
    assert response.request.headers["Authorization"] == "Bearer test-token"


def test_basic_endpoint_returns_a_list(api):
    response = api.request(ENDPOINTS["genders"])

    assert response.is_success
    assert isinstance(response.json(), list)
    assert response.json()[0]["id"] == 1


def test_complaint_creation_contract(api):
    response = api.request(
        ENDPOINTS["save_complaint"],
        json={"complaintDTO": {"requestTitle": "Example"}, "complainingDTOs": []},
    )

    assert response.status_code == 201
    assert set(response.json()) >= {"id", "status"}


def test_unknown_endpoint_is_reported_as_not_found(api):
    response = api.request(ENDPOINTS["branches"])

    assert response.status_code == 404
    assert response.json()["message"] == "not found"
