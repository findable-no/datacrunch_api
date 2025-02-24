from dataclasses import dataclass
from typing import Literal
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class Volume:
    name: str
    size: int
    type: str
    location_code: str | None = None
    instance_id: str | None = None
    instance_ids: list[str] | None = None


@dataclass_json
@dataclass(frozen=True)
class VolumeAction:
    action: Literal[
        "attach", "clone", "delete", "detach", "rename", "resize", "restore"
    ]
    id: str
    instance_id: str | None = None
    instance_ids: list[str] | None = None
    is_permanent: bool | None = None
    location_code: str | None = None
    name: str | None = None
    size: int | None = None
    type: str | None = None
