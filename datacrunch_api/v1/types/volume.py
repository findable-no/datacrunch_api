from dataclasses import dataclass, field
from typing import Literal
from dataclasses_json import config, dataclass_json  # type: ignore


@dataclass_json
@dataclass(frozen=True)
class Volume:
    name: str
    size: int
    type: str
    location_code: str | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    instance_id: str | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    instance_ids: list[str] | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )


@dataclass_json
@dataclass(frozen=True)
class VolumeAction:
    action: Literal[
        "attach", "clone", "delete", "detach", "rename", "resize", "restore"
    ]
    id: str
    instance_id: str | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    instance_ids: list[str] | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    is_permanent: bool | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    location_code: str | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
