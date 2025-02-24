import requests
from enum import Enum

from ._api_session import ApiSession
from .types.deployment import Deployment


BASE_URL = "https://api.datacrunch.io/v1"


class Endpoints(str, Enum):
    """API endpoints for container deployments and related operations"""

    CONTAINER_DEPLOYMENTS = "container-deployments"
    ENVIRONMENT_VARIABLES = "environment-variables"
    PAUSE = "pause"
    PURGE_QUEUE = "purge-queue"
    REPLICAS = "replicas"
    RESTART = "restart"
    RESUME = "resume"
    SCALING = "scaling"
    STATUS = "status"


class Deployments:
    """
    Client for managing container deployments and their configurations.
    Provides methods for CRUD operations on deployments, scaling, environment variables etc.
    """

    class InvalidRequest(Exception):
        """Raised when a request is malformed or contains invalid data"""

        pass

    class RequestFailed(Exception):
        """Raised when an API request fails for any other reason"""

        pass

    def __init__(self, client_id: str, client_secret: str):
        """
        Initialize deployments client with API credentials

        Args:
            client_id: The client ID for authentication
            client_secret: The client secret for authentication
        """
        self.api_session = ApiSession(client_id, client_secret)

    # Container Deployments
    def list_container_deployments(self) -> list:
        """
        Get all container deployments for the authenticated account

        Returns:
            List of deployment objects
        """
        return list(self.api_session.get(Endpoints.CONTAINER_DEPLOYMENTS.value))

    def create_container_deployment(self, deployment_config: Deployment) -> dict:
        """
        Create a new container deployment with the given configuration

        Args:
            deployment_config: Deployment configuration object

        Returns:
            Created deployment details
        """
        return self.api_session.post(
            Endpoints.CONTAINER_DEPLOYMENTS.value,
            json=deployment_config.to_dict(),  # type: ignore
        )

    def get_container_deployment(self, deployment_name: str) -> dict:
        """
        Get details of a specific container deployment

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Deployment details
        """
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}"
            )
        )

    def update_container_deployment(
        self, deployment_name: str, deployment_config: Deployment
    ) -> dict:
        """
        Update an existing container deployment

        Args:
            deployment_name: Name/ID of the deployment to update
            deployment_config: New deployment configuration

        Returns:
            Updated deployment details
        """
        return self.api_session.patch(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}",
            json=deployment_config.to_dict(),  # type: ignore
        )

    def delete_container_deployment(self, deployment_name: str) -> None:
        """
        Delete a container deployment

        Args:
            deployment_name: Name/ID of the deployment to delete
        """
        self.api_session.delete(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}"
        )

    def get_deployment_status(self, deployment_name: str) -> dict:
        """
        Get current status of a container deployment

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Deployment status information
        """
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.STATUS.value}"
            )
        )

    def restart_deployment(self, deployment_name: str) -> None:
        """
        Restart a container deployment

        Args:
            deployment_name: Name/ID of the deployment to restart

        Raises:
            RequestFailed: If restart operation fails
        """
        response = self.api_session.post_raw(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.RESTART.value}",
            json={},
        )
        if response.status_code != 201:
            raise self.RequestFailed(response.json())

    def get_deployment_scaling(self, deployment_name: str) -> dict:
        """
        Get scaling configuration of a deployment

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Scaling configuration details
        """
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.SCALING.value}"
            )
        )

    def update_deployment_scaling(
        self, deployment_name: str, scaling_config: dict
    ) -> dict:
        """
        Update scaling configuration of a deployment

        Args:
            deployment_name: Name/ID of the deployment
            scaling_config: New scaling configuration

        Returns:
            Updated scaling configuration
        """
        return self.api_session.patch(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.SCALING.value}",
            json=scaling_config,
        )

    def get_deployment_replicas(self, deployment_name: str) -> dict:
        """
        Get information about deployment replicas

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Replicas information
        """
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.REPLICAS.value}"
            )
        )

    def purge_deployment_queue(self, deployment_name: str) -> dict:
        """
        Purge the queue of a deployment

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Response from purge operation
        """
        return dict(
            self.api_session.post(  # type: ignore
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.PURGE_QUEUE.value}",
                json={},
            )
        )

    def pause_deployment(self, deployment_name: str) -> dict:
        """
        Pause a running deployment

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Response from pause operation
        """
        return dict(
            self.api_session.post(  # type: ignore
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.PAUSE.value}",
                json={},
            )
        )

    def resume_deployment(self, deployment_name: str) -> dict:
        """
        Resume a paused deployment

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Response from resume operation
        """
        return dict(
            self.api_session.post(  # type: ignore
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.RESUME.value}",
                json={},
            )
        )

    # Environment Variables
    def get_environment_variables(self, deployment_name: str) -> dict:
        """
        Get environment variables of a deployment

        Args:
            deployment_name: Name/ID of the deployment

        Returns:
            Environment variables configuration
        """
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}"
            )
        )

    def create_environment_variables(
        self, deployment_name: str, variables: dict
    ) -> dict:
        """
        Create environment variables for a deployment

        Args:
            deployment_name: Name/ID of the deployment
            variables: Dictionary of environment variables to create

        Returns:
            Created environment variables
        """
        return dict(
            self.api_session.post(  # type: ignore
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}",
                json=variables,
            )
        )

    def update_environment_variables(
        self, deployment_name: str, variables: dict
    ) -> dict:
        """
        Update environment variables of a deployment

        Args:
            deployment_name: Name/ID of the deployment
            variables: Dictionary of environment variables to update

        Returns:
            Updated environment variables
        """
        return dict(
            self.api_session.patch(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}",
                json=variables,
            )
        )

    def delete_environment_variables(self, deployment_name: str) -> None:
        """
        Delete all environment variables of a deployment

        Args:
            deployment_name: Name/ID of the deployment
        """
        self.api_session.delete(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}"
        )

    def validate_response(self, response: dict) -> dict:
        """
        Validate API response and handle errors

        Args:
            response: API response dictionary

        Returns:
            Validated response

        Raises:
            InvalidRequest: If request is invalid
        """
        if "code" not in response:
            return response
        match response["code"]:
            case "invalid_request":
                raise self.InvalidRequest(response.get("message"))
            case _:
                return response
