from enum import Enum

from ._api_session import ApiSession


class Endpoints(str, Enum):
    """API endpoints for managing secrets"""

    BALANCE = "balance"


class Balance:
    """
    Client for managing balance in the DataCrunch API.
        Provides methods for getting the balance for the authenticated account.
    """

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize balance client with API credentials

        Args:
            client_id: The client ID for authentication
            client_secret: The client secret for authentication
        """
        self.api_session = ApiSession(client_id, client_secret)

    def get_balance(self) -> dict:
        """
        Get the balance for the authenticated account

        Returns:
            Balance for the authenticated account
        """
        return dict(self.api_session.get(Endpoints.BALANCE.value))
