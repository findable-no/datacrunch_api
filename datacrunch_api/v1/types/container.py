from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json  # type: ignore

from .autoupdate import AutoUpdate
from .entrypoint import EntrypointOverrides
from .environment import Environment
from .healthcheck import HealthCheck
from .volume_mounts import VolumeMounts


@dataclass_json
@dataclass(frozen=True)
class Container:
    autoupdate: AutoUpdate
    env: Environment
    exposed_port: int
    healthcheck: HealthCheck
    image: str
    name: str
    volume_mounts: VolumeMounts
    entrypoint_overrides: EntrypointOverrides | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
