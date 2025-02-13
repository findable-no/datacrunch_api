import requests
from enum import Enum

from ._api_session import ApiSession


class Endpoints(str, Enum):
    """API endpoints"""

    SERVERLESS_COMPUTE = "serverless-compute-resources"


class ServerlessCompute:
    class InvalidRequest(Exception):
        pass

    class RequestFailed(Exception):
        pass

    def __init__(self, client_id: str, client_secret: str):
        self.api_session = ApiSession(client_id, client_secret)

    # Serverless Compute Resources
    def list_serverless_compute_resources(self) -> list:
        """Get all serverless compute resources"""
        return list(self.api_session.get(Endpoints.SERVERLESS_COMPUTE.value))
