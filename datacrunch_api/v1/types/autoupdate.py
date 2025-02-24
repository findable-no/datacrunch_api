from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json  # type: ignore


@dataclass_json
@dataclass(frozen=True)
class AutoUpdate:
    enabled: bool
    mode: str
    tag_filter: str | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
