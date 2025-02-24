import pytest
from datacrunch_api.v1 import SSHKey, SSHKeys


@pytest.fixture
def ssh_keys(mocker):
    mocker.patch("datacrunch_api.v1.ssh_keys.ApiSession")
    return SSHKeys("dummy_client_id", "dummy_client_secret")


def test_add_ssh_key(mocker, ssh_keys):
    ssh_key = SSHKey(name="new-ssh-key", key="ssh-key-value")
    mock_session = mocker.patch.object(ssh_keys, "api_session")
    mock_session.post_raw.return_value.status_code = 201

    ssh_keys.add_ssh_key(ssh_key)

    mock_session.post_raw.assert_called_once_with("sshkeys", json=ssh_key.to_dict())


def test_delete_ssh_key(mocker, ssh_keys):
    ssh_key_id = "test-ssh-key-id"
    mock_session = mocker.patch.object(ssh_keys, "api_session")
    mock_session.delete.return_value.status_code = 200

    ssh_keys.delete_ssh_key(ssh_key_id)

    mock_session.delete.assert_called_once_with(f"sshkeys/{ssh_key_id}")


def test_delete_ssh_keys(mocker, ssh_keys):
    ssh_key_ids = ["test-ssh-key-id-1", "test-ssh-key-id-2"]
    mock_session = mocker.patch.object(ssh_keys, "api_session")
    mock_session.delete.return_value.status_code = 200

    ssh_keys.delete_ssh_keys(ssh_key_ids)

    mock_session.delete.assert_called_once_with("sshkeys", json={"keys": ssh_key_ids})


def test_get_ssh_key(mocker, ssh_keys):
    ssh_key_id = "test-ssh-key-id"
    mock_session = mocker.patch.object(ssh_keys, "api_session")
    mock_session.get.return_value = {
        "id": "123",
        "name": "ssh-key1",
        "created_at": "2024-01-01T00:00:00Z",
    }
    result = ssh_keys.get_ssh_key(ssh_key_id)

    assert result == {
        "id": "123",
        "name": "ssh-key1",
        "created_at": "2024-01-01T00:00:00Z",
    }


def test_list_ssh_keys(mocker, ssh_keys):
    expected_response = [
        {"id": "123", "name": "ssh-key1", "created_at": "2024-01-01T00:00:00Z"},
        {"id": "456", "name": "ssh-key2", "created_at": "2024-01-01T00:00:00Z"},
    ]
    mock_session = mocker.patch.object(ssh_keys, "api_session")
    mock_session.get.return_value = expected_response

    result = ssh_keys.list_ssh_keys()

    assert result == expected_response
    mock_session.get.assert_called_once_with("sshkeys")
