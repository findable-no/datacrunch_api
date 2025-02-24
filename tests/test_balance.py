import pytest
from datacrunch_api.v1 import Balance


@pytest.fixture
def balance(mocker):
    mocker.patch("datacrunch_api.v1.balance.ApiSession")
    return Balance("dummy_client_id", "dummy_client_secret")


def test_get_balance(mocker, balance):
    mock_session = mocker.patch.object(balance, "api_session")
    mock_session.get.return_value = {"balance": 100}
    result = balance.get_balance()
    assert result == {"balance": 100}
    mock_session.get.assert_called_once_with("balance")
