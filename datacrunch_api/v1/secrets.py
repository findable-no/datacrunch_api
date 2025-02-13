import requests
from enum import Enum

from ._api_session import ApiSession
from .secret import Secret


class Endpoints(str, Enum):
    """API endpoints"""

    SECRETS = "secrets"


class Secrets:
    class InvalidRequest(Exception):
        pass

    class RequestFailed(Exception):
        pass

    def __init__(self, client_id: str, client_secret: str):
        self.api_session = ApiSession(client_id, client_secret)

    # Secrets
    def list_secrets(self) -> list:
        """Get all secrets"""
        return list(self.api_session.get(Endpoints.SECRETS.value))

    def create_secret(self, secret: Secret) -> None:
        """Create a new secret"""
        response = self.api_session.post_raw(
            Endpoints.SECRETS.value, json=secret.to_dict()
        )
        if response.status_code != 201:
            raise self.RequestFailed(response.json())

    def delete_secret(self, secret_name: str) -> None:
        """Delete a secret"""
        self.api_session.delete(f"{Endpoints.SECRETS.value}/{secret_name}")
