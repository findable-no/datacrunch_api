from enum import Enum

from ._api_session import ApiSession
from .types.volume import Volume, VolumeAction


class Endpoints(str, Enum):
    """API endpoints for managing volumes"""

    TRASH = "trash"
    VOLUME_TYPES = "volume-types"
    VOLUMES = "volumes"


class Volumes:
    """
    Client for managing volumes in the DataCrunch API.
    """

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize volumes client with API credentials
        """
        self.api_session = ApiSession(client_id, client_secret)

    def action(self, action: VolumeAction) -> dict:
        """
        Perform an action on a volume
        """
        response = self.api_session.put_raw(
            Endpoints.VOLUMES.value, json=action.to_dict()  # type: ignore
        )
        if response.status_code != 202:
            raise self.api_session.RequestFailed(response.json())
        return response.json()

    def create(self, volume: Volume) -> dict:
        """
        Create a new volume
        """
        return self.api_session.post(
            Endpoints.VOLUMES.value, json=volume.to_dict()  # type: ignore
        )

    def delete(self, volume_id: str) -> None:
        """
        Delete a volume by ID
        """
        self.api_session.delete(f"{Endpoints.VOLUMES.value}/{volume_id}")

    def get_volume(self, volume_id: str) -> dict:
        """
        Get a volume by ID
        """
        return dict(self.api_session.get(f"{Endpoints.VOLUMES.value}/{volume_id}"))

    def get_volume_types(self) -> list[dict]:
        """
        Get all volume types
        """
        return list(self.api_session.get(Endpoints.VOLUME_TYPES.value))

    def list_volumes(self) -> list[dict]:
        """
        List all volumes
        """
        return list(self.api_session.get(Endpoints.VOLUMES.value))

    def list_trash(self) -> list[dict]:
        """
        List all volumes in the trash
        """
        return list(
            self.api_session.get(f"{Endpoints.VOLUMES.value}/{Endpoints.TRASH.value}")
        )
