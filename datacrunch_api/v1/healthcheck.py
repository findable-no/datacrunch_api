from dataclasses import dataclass


HealthCheckValue = dict[str, bool | str | int]


@dataclass
class HealthCheck:
    enabled: bool
    path: str
    port: int

    def to_dict(self) -> HealthCheckValue:
        return {
            "enabled": self.enabled,
            "path": self.path,
            "port": self.port,
        }
