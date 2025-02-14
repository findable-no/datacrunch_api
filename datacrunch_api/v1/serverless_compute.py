from enum import Enum

from ._api_session import ApiSession


class Endpoints(str, Enum):
    """API endpoints for serverless compute operations"""

    SERVERLESS_COMPUTE = "serverless-compute-resources"


class ServerlessCompute:
    """
    Client for managing serverless compute resources in the DataCrunch API.
    Provides methods for listing and managing serverless compute instances.
    """

    class InvalidRequest(Exception):
        """Raised when a request is malformed or contains invalid data"""

        pass

    class RequestFailed(Exception):
        """Raised when an API request fails for any other reason"""

        pass

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize serverless compute client with API credentials

        Args:
            client_id: The client ID for authentication
            client_secret: The client secret for authentication
        """
        self.api_session = ApiSession(client_id, client_secret)

    def list_serverless_compute_resources(self) -> list:
        """
        Get all serverless compute resources for the authenticated account

        Returns:
            List of serverless compute resources
        """
        return list(self.api_session.get(Endpoints.SERVERLESS_COMPUTE.value))
