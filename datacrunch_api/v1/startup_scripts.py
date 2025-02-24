from enum import Enum

from ._api_session import ApiSession
from .types.startup_script import StartupScript


class Endpoints(str, Enum):
    """API endpoints for managing startup scripts"""

    STARTUP_SCRIPTS = "scripts"


class StartupScripts:
    """
    Client for managing startup scripts in the DataCrunch API.
    """

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize startup scripts client with API credentials
        """
        self.api_session = ApiSession(client_id, client_secret)

    def add_startup_script(self, startup_script: StartupScript) -> str:
        """
        Create a new startup script

        Args:
            startup_script: The StartupScript object containing name and script content

        Returns:
            The ID of the created startup script

        Raises:
            RequestFailed: If the startup script creation fails
        """
        response = self.api_session.post_raw(
            Endpoints.STARTUP_SCRIPTS.value, json=startup_script.to_dict()  # type: ignore
        )
        if response.status_code != 201:
            raise self.api_session.RequestFailed(response.json())
        return str(response.text)

    def delete_startup_script(self, startup_script_id: str) -> None:
        """
        Delete a startup script by ID
        """
        self.api_session.delete(
            f"{Endpoints.STARTUP_SCRIPTS.value}/{startup_script_id}"
        )

    def delete_startup_scripts(self, startup_script_ids: list[str]) -> None:
        """
        Delete multiple startup scripts by ID
        """
        self.api_session.delete(
            f"{Endpoints.STARTUP_SCRIPTS.value}", json={"scripts": startup_script_ids}  # type: ignore
        )

    def get_startup_script(self, startup_script_id: str) -> dict:
        """
        Get a startup script by ID
        """
        return dict(
            self.api_session.get(
                f"{Endpoints.STARTUP_SCRIPTS.value}/{startup_script_id}"
            )
        )

    def list_startup_scripts(self) -> list[dict[str, str]]:
        """
        Get all startup scripts
        """
        return list(self.api_session.get(Endpoints.STARTUP_SCRIPTS.value))
