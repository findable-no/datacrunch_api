from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class HealthCheck:
    enabled: bool
    path: str
    port: int
