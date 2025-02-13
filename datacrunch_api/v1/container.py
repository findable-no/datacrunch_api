from dataclasses import dataclass

from .autoupdate import AutoUpdate, AutoUpdateValue
from .compute import Compute, ComputeValue
from .entrypoint import EntrypointOverrides, EntrypointOverridesValue
from .environment import Environment, EnvironmentValue
from .healthcheck import HealthCheck, HealthCheckValue
from .volume_mounts import VolumeMounts, VolumeMountsValue


ContainerValue = dict[
    str,
    AutoUpdateValue
    | EntrypointOverridesValue
    | EnvironmentValue
    | HealthCheckValue
    | VolumeMountsValue
    | int
    | str,
]


@dataclass
class Container:
    autoupdate: AutoUpdate
    environment: Environment
    exposed_port: int
    healthcheck: HealthCheck
    image: str
    name: str
    volume_mounts: VolumeMounts
    entrypoint_overrides: EntrypointOverrides | None = None

    def to_dict(self) -> ContainerValue:
        response: ContainerValue = {
            "autoupdate": self.autoupdate.to_dict(),
            "env": self.environment.to_list(),
            "exposed_port": self.exposed_port,
            "healthcheck": self.healthcheck.to_dict(),
            "image": self.image,
            "name": self.name,
            "volume_mounts": self.volume_mounts.to_list(),
        }

        if self.entrypoint_overrides:
            response["entrypoint_overrides"] = self.entrypoint_overrides.to_dict()

        return response
