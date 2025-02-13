from dataclasses import dataclass, field


CommandLine = list[str]
EntrypointOverridesValue = dict[str, str | bool | CommandLine]


@dataclass
class EntrypointOverrides:
    enabled: bool
    entrypoint: CommandLine = field(default_factory=CommandLine)
    command: CommandLine = field(default_factory=CommandLine)

    def to_dict(self) -> EntrypointOverridesValue:
        return {
            "enabled": self.enabled,
            "entrypoint": self.entrypoint,
            "cmd": self.command,
        }
