import pytest
from datacrunch_api.v1 import Secret, Secrets


@pytest.fixture
def secrets(mocker):
    mocker.patch("datacrunch_api.v1.secrets.ApiSession")
    return Secrets("dummy_client_id", "dummy_client_secret")


def test_list_secrets(mocker, secrets):
    expected_response = [
        {"name": "secret1", "created_at": "2024-01-01T00:00:00Z"},
        {"name": "secret2", "created_at": "2024-01-01T00:00:00Z"},
    ]
    mock_session = mocker.patch.object(secrets, "api_session")
    mock_session.get.return_value = expected_response

    result = secrets.list_secrets()

    assert result == expected_response
    mock_session.get.assert_called_once_with("secrets")


def test_create_secret(mocker, secrets):
    secret = Secret(name="new-secret", value="secret-value")
    mock_session = mocker.patch.object(secrets, "api_session")
    mock_session.post_raw.return_value.status_code = 201

    secrets.create_secret(secret)

    mock_session.post_raw.assert_called_once_with("secrets", json=secret.to_dict())


def test_delete_secret(mocker, secrets):
    secret_id = "test-secret-id"
    mock_session = mocker.patch.object(secrets, "api_session")
    mock_session.delete.return_value.status_code = 200

    secrets.delete_secret(secret_id)

    mock_session.delete.assert_called_once_with(f"secrets/{secret_id}")
