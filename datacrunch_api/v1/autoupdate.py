from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class AutoUpdate:
    enabled: bool
    mode: str
    tag_filter: str | None = None
