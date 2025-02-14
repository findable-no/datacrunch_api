from enum import Enum

from ._api_session import ApiSession
from .types.secret import Secret


class Endpoints(str, Enum):
    """API endpoints for managing secrets"""

    SECRETS = "secrets"


class Secrets:
    """
    Client for managing secrets in the DataCrunch API.
    Provides methods for creating, listing and deleting secrets.
    """

    class InvalidRequest(Exception):
        """Raised when a request is malformed or contains invalid data"""

        pass

    class RequestFailed(Exception):
        """Raised when an API request fails for any other reason"""

        pass

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize secrets client with API credentials

        Args:
            client_id: The client ID for authentication
            client_secret: The client secret for authentication
        """
        self.api_session = ApiSession(client_id, client_secret)

    def list_secrets(self) -> list:
        """
        Get all secrets for the authenticated account

        Returns:
            List of secrets
        """
        return list(self.api_session.get(Endpoints.SECRETS.value))

    def create_secret(self, secret: Secret) -> None:
        """
        Create a new secret

        Args:
            secret: The secret object containing name and value

        Raises:
            RequestFailed: If the secret creation fails
        """
        response = self.api_session.post_raw(
            Endpoints.SECRETS.value, json=secret.to_dict()  # type: ignore
        )
        if response.status_code != 201:
            raise self.RequestFailed(response.json())

    def delete_secret(self, secret_name: str) -> None:
        """
        Delete a secret by name

        Args:
            secret_name: Name of the secret to delete

        Raises:
            RequestFailed: If the secret deletion fails
        """
        self.api_session.delete(f"{Endpoints.SECRETS.value}/{secret_name}")
