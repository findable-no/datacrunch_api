from enum import Enum

from ._api_session import ApiSession


class Endpoints(str, Enum):
    """API endpoints for managing images"""

    IMAGES = "images"


class Images:
    """
    Client for managing images in the DataCrunch API.
    """

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize images client with API credentials
        """
        self.api_session = ApiSession(client_id, client_secret)

    def list_images(self) -> list:
        """
        List all images
        """
        return list(self.api_session.get(Endpoints.IMAGES.value))
