from dataclasses import dataclass, field
from dataclasses_json import config, dataclass_json  # type: ignore

CommandLine = list[str]


@dataclass_json
@dataclass(frozen=True)
class EntrypointOverrides:
    enabled: bool
    entrypoint: CommandLine | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    cmd: CommandLine | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
