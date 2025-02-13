from dataclasses import dataclass


SecretValue = dict[str, str]


@dataclass
class Secret:
    name: str
    value: str

    def to_dict(self) -> SecretValue:
        return {
            "name": self.name,
            "value": self.value,
        }
