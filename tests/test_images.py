import pytest
from datacrunch_api.v1 import Images


@pytest.fixture
def images(mocker):
    mocker.patch("datacrunch_api.v1.images.ApiSession")
    return Images("dummy_client_id", "dummy_client_secret")


def test_list_images(mocker, images):
    mock_session = mocker.patch.object(images, "api_session")
    mock_session.get.return_value = [
        {"id": "123", "name": "image1"},
        {"id": "456", "name": "image2"},
    ]
    result = images.list_images()
    assert result == [
        {"id": "123", "name": "image1"},
        {"id": "456", "name": "image2"},
    ]
    mock_session.get.assert_called_once_with("images")
