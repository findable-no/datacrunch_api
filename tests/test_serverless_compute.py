import pytest
from datacrunch_api.v1.serverless_compute import ServerlessCompute


@pytest.fixture
def serverless_compute(mocker):
    mocker.patch("datacrunch_api.v1.serverless_compute.ApiSession")
    return ServerlessCompute("dummy_client_id", "dummy_client_secret")


def test_list_serverless_compute_resources(mocker, serverless_compute):
    mock_session = mocker.patch.object(serverless_compute, "api_session")
    mock_session.get.return_value = [{"name": "1"}, {"name": "2"}]
    response = serverless_compute.list_serverless_compute_resources()
    assert response == [{"name": "1"}, {"name": "2"}]
    mock_session.get.assert_called_once_with("serverless-compute-resources")
