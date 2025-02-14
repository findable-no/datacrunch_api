from dataclasses import dataclass
from dataclasses_json import dataclass_json  # type: ignore

from .autoupdate import AutoUpdate
from .entrypoint import EntrypointOverrides
from .environment import Environment
from .healthcheck import HealthCheck
from .volume_mounts import VolumeMounts


@dataclass_json
@dataclass(frozen=True)
class Container:
    autoupdate: AutoUpdate
    environment: Environment
    exposed_port: int
    healthcheck: HealthCheck
    image: str
    name: str
    volume_mounts: VolumeMounts
    entrypoint_overrides: EntrypointOverrides | None = None
