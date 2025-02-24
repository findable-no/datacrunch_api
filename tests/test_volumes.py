import pytest
from datacrunch_api.v1 import Volume, VolumeAction, Volumes


@pytest.fixture
def volumes(mocker):
    mocker.patch("datacrunch_api.v1.volumes.ApiSession")
    return Volumes("dummy_client_id", "dummy_client_secret")


def test_list_volumes(mocker, volumes):
    mock_session = mocker.patch.object(volumes, "api_session")
    mock_session.get.return_value = [
        {"id": "123", "name": "volume1"},
        {"id": "456", "name": "volume2"},
    ]
    result = volumes.list_volumes()
    assert result == [
        {"id": "123", "name": "volume1"},
        {"id": "456", "name": "volume2"},
    ]
    mock_session.get.assert_called_once_with("volumes")


def test_get_volume(mocker, volumes):
    mock_session = mocker.patch.object(volumes, "api_session")
    mock_session.get.return_value = {"id": "123", "name": "volume1"}
    result = volumes.get_volume("123")
    assert result == {"id": "123", "name": "volume1"}
    mock_session.get.assert_called_once_with("volumes/123")


def test_get_volume_types(mocker, volumes):
    mock_session = mocker.patch.object(volumes, "api_session")
    mock_session.get.return_value = [
        {"id": "123", "name": "volume1"},
        {"id": "456", "name": "volume2"},
    ]
    result = volumes.get_volume_types()
    assert result == [
        {"id": "123", "name": "volume1"},
        {"id": "456", "name": "volume2"},
    ]
    mock_session.get.assert_called_once_with("volume-types")


def test_create_volume(mocker, volumes):
    mock_session = mocker.patch.object(volumes, "api_session")
    mock_session.post.return_value = {"id": "123"}
    result = volumes.create(
        Volume(name="test-volume", size=10, type="test-volume-type")
    )
    assert result == {"id": "123"}
    mock_session.post.assert_called_once_with(
        "volumes",
        json={
            "name": "test-volume",
            "size": 10,
            "type": "test-volume-type",
            "location_code": None,
            "instance_id": None,
            "instance_ids": None,
        },
    )


def test_delete_volume(mocker, volumes):
    mock_session = mocker.patch.object(volumes, "api_session")
    volumes.delete("123")
    mock_session.delete.assert_called_once_with("volumes/123")


def test_action(mocker, volumes):
    mock_session = mocker.patch.object(volumes, "api_session")
    mock_session.put_raw.return_value.status_code = 202
    volumes.action(VolumeAction(action="delete", id="123"))
    mock_session.put_raw.assert_called_once_with(
        "volumes",
        json={
            "action": "delete",
            "id": "123",
            "instance_id": None,
            "instance_ids": None,
            "is_permanent": None,
            "location_code": None,
            "name": None,
            "size": None,
            "type": None,
        },
    )


def test_list_trash(mocker, volumes):
    mock_session = mocker.patch.object(volumes, "api_session")
    mock_session.get.return_value = [
        {"id": "123", "name": "volume1"},
        {"id": "456", "name": "volume2"},
    ]
    result = volumes.list_trash()
    assert result == [
        {"id": "123", "name": "volume1"},
        {"id": "456", "name": "volume2"},
    ]
    mock_session.get.assert_called_once_with("volumes/trash")
