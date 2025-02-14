from dataclasses import dataclass
from dataclasses_json import dataclass_json

from .credentials import Credentials


@dataclass_json
@dataclass(frozen=True)
class ContainerRegistrySettings:
    is_private: bool
    credentials: Credentials | None = None
