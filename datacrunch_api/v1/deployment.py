from dataclasses import dataclass
from dataclasses_json import dataclass_json

from .container import Container
from .container_registry_settings import ContainerRegistrySettings
from .compute import Compute
from .scaling import Scaling


@dataclass_json
@dataclass(frozen=True)
class Deployment:
    name: str
    containers: list[Container]
    container_registry_settings: ContainerRegistrySettings
    compute: Compute
    scaling: Scaling
