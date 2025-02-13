from dataclasses import dataclass


AutoUpdateValue = dict[str, str | bool]


@dataclass
class AutoUpdate:
    enabled: bool
    mode: str
    tag_filter: str | None = None

    def to_dict(self) -> AutoUpdateValue:
        value: AutoUpdateValue = {
            "enabled": self.enabled,
            "mode": self.mode,
        }
        if self.tag_filter:
            value["tag_filter"] = self.tag_filter
        return value
