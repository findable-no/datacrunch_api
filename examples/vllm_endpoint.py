import json

from datacrunch_api.v1 import (
    AutoUpdate,
    Compute,
    Container,
    ContainerRegistrySettings,
    Credentials,
    Deployment,
    Deployments,
    EntrypointOverrides,
    EnvironmentVariable,
    Environment,
    HealthCheck,
    QueueLoad,
    Scaling,
    ScalingPolicy,
    ScalingTriggers,
    VolumeMount,
    VolumeMounts,
)
import typer  # type: ignore
from rich import print  # type: ignore
from rich.panel import Panel  # type: ignore


class VLLMEndpoint:

    def __init__(
        self,
        api: Deployments,
        huggingface_key: str,
        deployment_name: str,
    ):
        self.api = api
        self.huggingface_key = huggingface_key
        self.deployment_name = deployment_name

    def deployment(
        self, container_name: str, image: str, command: list[str]
    ) -> Deployment:
        container = Container(
            name=container_name,
            image=image,
            exposed_port=8000,
            healthcheck=HealthCheck(
                enabled=True,
                port=8000,
                path="/health",
            ),
            entrypoint_overrides=EntrypointOverrides(
                enabled=True,
                command=command,
            ),
            environment=Environment(
                [
                    EnvironmentVariable(
                        name="HF_TOKEN",
                        value=self.huggingface_key,
                        type="secret",
                    ),
                    EnvironmentVariable(
                        name="HF_HOME",
                        value="/data/.huggingface",
                        type="plain",
                    ),
                    EnvironmentVariable(
                        name="HF_HUB_ENABLE_HF_TRANSFER",
                        value="1",
                        type="plain",
                    ),
                ]
            ),
            autoupdate=AutoUpdate(
                enabled=False,
                mode="latest",
            ),
            volume_mounts=VolumeMounts(
                [
                    VolumeMount(
                        type="scratch",
                        mount_path="/data/.huggingface",
                    )
                ]
            ),
        )
        deployment = Deployment(
            name=self.deployment_name,
            containers=[container],
            container_registry_settings=ContainerRegistrySettings(
                is_private=False,
                credentials=Credentials(
                    name="hf-token",
                ),
            ),
            compute=Compute(name="RTX6000 Ada"),
            scaling=Scaling(
                min_replica_count=1,
                max_replica_count=1,
                concurrent_requests_per_replica=10,
                queue_message_ttl_seconds=3600,
                scale_down_policy=ScalingPolicy(
                    delay_seconds=300,
                ),
                scale_up_policy=ScalingPolicy(
                    delay_seconds=300,
                ),
                scaling_triggers=ScalingTriggers(
                    queue_load=QueueLoad(
                        threshold=2,
                    ),
                ),
            ),
        )
        return deployment

    def create_endpoint(
        self, container_name: str, image: str, command: list[str]
    ) -> dict:
        print(
            Panel.fit(
                json.dumps(
                    self.deployment(container_name, image, command).to_dict(), indent=2  # type: ignore
                ),
                title="Request",
                border_style="red",
            )
        )
        return self.api.create_container_deployment(
            self.deployment(container_name, image, command)
        )

    def delete_endpoint(self) -> None:
        self.api.delete_container_deployment(self.deployment_name)

    def restart_endpoint(self) -> None:
        self.api.restart_deployment(self.deployment_name)

    def update_endpoint(
        self, container_name: str, image: str, command: list[str]
    ) -> dict:
        return self.api.update_container_deployment(
            self.deployment_name, self.deployment(container_name, image, command)
        )
