from dataclasses import dataclass

from .container import Container, ContainerValue
from .container_registry_settings import (
    ContainerRegistrySettings,
    ContainerRegistrySettingsValue,
)
from .compute import Compute, ComputeValue
from .scaling import Scaling, ScalingValue


DeploymentValue = dict[
    str,
    ContainerRegistrySettingsValue
    | list[ContainerValue]
    | ComputeValue
    | ScalingValue
    | str,
]


@dataclass
class Deployment:
    name: str
    containers: list[Container]
    container_registry_settings: ContainerRegistrySettings
    compute: Compute
    scaling: Scaling

    def to_dict(self) -> DeploymentValue:
        return {
            "name": self.name,
            "containers": [container.to_dict() for container in self.containers],
            "container_registry_settings": self.container_registry_settings.to_dict(),
            "compute": self.compute.to_dict(),
            "scaling": self.scaling.to_dict(),
        }
