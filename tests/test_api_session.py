import pytest
import requests
from datacrunch_api.v1._api_session import ApiSession


@pytest.fixture
def api_session(mocker) -> ApiSession:
    mock_session = mocker.patch("datacrunch_api.v1._api_session.requests.Session")
    mock_session.return_value.post.return_value.json.return_value = {
        "access_token": "dummy_access_token"
    }
    return ApiSession("dummy_client_id", "dummy_client_secret")


def test_delete(mocker, api_session):
    mock_session = mocker.patch.object(api_session, "session")
    mock_session.delete.return_value.status_code = 200
    api_session.delete("dummy_url")
    mock_session.delete.assert_called_once_with(
        f"{api_session.base_url}/dummy_url", json=None
    )


def test_get(mocker, api_session):
    expected_response = {"dummy_response"}
    mock_session = mocker.patch.object(api_session, "session")
    mock_session.get.return_value.json.return_value = expected_response
    response = api_session.get("dummy_url")
    assert response == expected_response
    mock_session.get.assert_called_once_with(f"{api_session.base_url}/dummy_url")


def test_post(mocker, api_session):
    expected_response = {"dummy_response"}
    mock_session = mocker.patch.object(api_session, "session")
    mock_session.post.return_value.json.return_value = expected_response
    response = api_session.post("dummy_url", {"dummy_data": "dummy_value"})
    assert response == expected_response
    mock_session.post.assert_called_once_with(
        f"{api_session.base_url}/dummy_url", json={"dummy_data": "dummy_value"}
    )


def test_patch(mocker, api_session):
    expected_response = {"dummy_response"}
    mock_session = mocker.patch.object(api_session, "session")
    mock_session.patch.return_value.json.return_value = expected_response
    response = api_session.patch("dummy_url", {"dummy_data": "dummy_value"})
    assert response == expected_response
    mock_session.patch.assert_called_once_with(
        f"{api_session.base_url}/dummy_url", json={"dummy_data": "dummy_value"}
    )


def test_validate_response(api_session):
    response = {"dummy_response"}
    assert api_session.validate_response(response) == response


def test_validate_response_invalid_request(api_session):
    response = {"code": "invalid_request", "message": "Invalid request"}
    with pytest.raises(ApiSession.InvalidRequest):
        api_session.validate_response(response)


def test_validate_response_conflict(api_session):
    response = {"code": "conflict", "message": "Conflict"}
    with pytest.raises(ApiSession.Conflict):
        api_session.validate_response(response)
