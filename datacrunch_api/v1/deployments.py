import requests
from enum import Enum

from ._api_session import ApiSession
from .deployment import Deployment


BASE_URL = "https://api.datacrunch.io/v1"


class Endpoints(str, Enum):
    """API endpoints"""

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
    class InvalidRequest(Exception):
        pass

    class RequestFailed(Exception):
        pass

    def __init__(self, client_id: str, client_secret: str):
        self.api_session = ApiSession(client_id, client_secret)

    # Container Deployments
    def list_container_deployments(self) -> list:
        """Get all container deployments"""
        return list(self.api_session.get(Endpoints.CONTAINER_DEPLOYMENTS.value))

    def create_container_deployment(self, deployment_config: Deployment) -> dict:
        """Create a new container deployment"""
        return self.api_session.post(
            Endpoints.CONTAINER_DEPLOYMENTS.value,
            json=deployment_config.to_dict(),  # type: ignore
        )

    def get_container_deployment(self, deployment_name: str) -> dict:
        """Get details of a specific container deployment"""
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}"
            )
        )

    def update_container_deployment(
        self, deployment_name: str, deployment_config: Deployment
    ) -> dict:
        """Update a container deployment"""
        return self.api_session.patch(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}",
            json=deployment_config.to_dict(),  # type: ignore
        )

    def delete_container_deployment(self, deployment_name: str) -> None:
        """Delete a container deployment"""
        self.api_session.delete(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}"
        )

    def get_deployment_status(self, deployment_name: str) -> dict:
        """Get status of a container deployment"""
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.STATUS.value}"
            )
        )

    def restart_deployment(self, deployment_name: str) -> None:
        """Restart a container deployment"""
        response = self.api_session.post_raw(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.RESTART.value}",
            json={},
        )
        if response.status_code != 201:
            raise self.RequestFailed(response.json())

    def get_deployment_scaling(self, deployment_name: str) -> dict:
        """Get scaling configuration of a deployment"""
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.SCALING.value}"
            )
        )

    def update_deployment_scaling(
        self, deployment_name: str, scaling_config: dict
    ) -> dict:
        """Update scaling configuration of a deployment"""
        return self.api_session.patch(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.SCALING.value}",
            json=scaling_config,
        )

    def get_deployment_replicas(self, deployment_name: str) -> dict:
        """Get replicas information of a deployment"""
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.REPLICAS.value}"
            )
        )

    def purge_deployment_queue(self, deployment_name: str) -> dict:
        """Purge queue of a deployment"""
        return self.api_session.post(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.PURGE_QUEUE.value}",
            json={},
        )

    def pause_deployment(self, deployment_name: str) -> dict:
        """Pause a deployment"""
        return self.api_session.post(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.PAUSE.value}",
            json={},
        )

    def resume_deployment(self, deployment_name: str) -> dict:
        """Resume a deployment"""
        return self.api_session.post(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.RESUME.value}",
            json={},
        )

    # Environment Variables
    def get_environment_variables(self, deployment_name: str) -> dict:
        """Get environment variables of a deployment"""
        return dict(
            self.api_session.get(
                f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}"
            )
        )

    def create_environment_variables(
        self, deployment_name: str, variables: dict
    ) -> dict:
        """Create environment variables for a deployment"""
        return self.api_session.post(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}",
            json=variables,
        )

    def update_environment_variables(
        self, deployment_name: str, variables: dict
    ) -> dict:
        """Update environment variables of a deployment"""
        return self.api_session.patch(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}",
            json=variables,
        )

    def delete_environment_variables(self, deployment_name: str) -> None:
        """Delete environment variables of a deployment"""
        self.api_session.delete(
            f"{Endpoints.CONTAINER_DEPLOYMENTS.value}/{deployment_name}/{Endpoints.ENVIRONMENT_VARIABLES.value}"
        )

    def validate_response(self, response: dict) -> dict:
        if "code" not in response:
            return response
        match response["code"]:
            case "invalid_request":
                raise self.InvalidRequest(response.get("message"))
            case _:
                return response
