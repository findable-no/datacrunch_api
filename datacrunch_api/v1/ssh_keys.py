from enum import Enum

from ._api_session import ApiSession
from .types.ssh_key import SSHKey


class Endpoints(str, Enum):
    """API endpoints for managing SSH keys"""

    SSH_KEYS = "sshkeys"


class SSHKeys:
    """
    Client for managing SSH keys in the DataCrunch API.
    Provides methods for creating, listing and deleting SSH keys.
    """

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize SSH keys client with API credentials

        Args:
            client_id: The client ID for authentication
            client_secret: The client secret for authentication
        """
        self.api_session = ApiSession(client_id, client_secret)

    def add_ssh_key(self, ssh_key: SSHKey) -> str:
        """
        Create a new SSH key

        Args:
            ssh_key: The SSH key object containing name and value

        Raises:
            RequestFailed: If the SSH key creation fails
        """
        response = self.api_session.post_raw(
            Endpoints.SSH_KEYS.value, json=ssh_key.to_dict()  # type: ignore
        )
        if response.status_code != 201:
            raise self.api_session.RequestFailed(response.json())
        return str(response.text)

    def delete_ssh_key(self, key_id: str) -> None:
        """
        Delete an SSH key by ID
        """
        self.api_session.delete(f"{Endpoints.SSH_KEYS.value}/{key_id}")

    def delete_ssh_keys(self, keys: list[str]) -> None:
        """
        Delete an SSH key by name

        Args:
            ssh_key_name: Name of the SSH key to delete

        Raises:
            RequestFailed: If the SSH key deletion fails
        """
        self.api_session.delete(
            f"{Endpoints.SSH_KEYS.value}", json={"keys": keys}  # type: ignore
        )

    def get_ssh_key(self, key_id: str) -> dict[str, str]:
        """
        Get an SSH key by ID
        """
        return dict(self.api_session.get(f"{Endpoints.SSH_KEYS.value}/{key_id}"))

    def list_ssh_keys(self) -> list:
        """
        Get all SSH keys for the authenticated account

        Returns:
            List of SSH keys
        """
        return list(self.api_session.get(Endpoints.SSH_KEYS.value))
