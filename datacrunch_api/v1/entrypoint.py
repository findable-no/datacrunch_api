from dataclasses import dataclass, field
from dataclasses_json import dataclass_json  # type: ignore

CommandLine = list[str]


@dataclass_json
@dataclass(frozen=True)
class EntrypointOverrides:
    enabled: bool
    entrypoint: CommandLine = field(default_factory=CommandLine)
    command: CommandLine = field(default_factory=CommandLine)
