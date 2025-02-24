from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json  # type: ignore

from .credentials import Credentials


@dataclass_json
@dataclass(frozen=True)
class ContainerRegistrySettings:
    is_private: bool
    credentials: Credentials | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
