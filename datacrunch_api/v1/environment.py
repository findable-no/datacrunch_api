from dataclasses import dataclass


EnvironmentVariableValue = dict[str, str]


@dataclass
class EnvironmentVariable:
    name: str
    value: str
    type: "EnvironmentVariable.Type"

    class Type(str):
        PLAIN = "plain"
        SECRET = "secret"

    def to_dict(self) -> EnvironmentVariableValue:
        return {
            "name": self.name,
            "value_or_reference_to_secret": self.value,
            "type": self.type,
        }


EnvironmentValue = list[EnvironmentVariableValue]


class Environment(list[EnvironmentVariable]):
    def to_list(self) -> EnvironmentValue:
        return [env_var.to_dict() for env_var in self]
