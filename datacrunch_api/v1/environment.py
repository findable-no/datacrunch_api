from dataclasses import dataclass
from typing import Literal
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class EnvironmentVariable:
    name: str
    value: str
    type: "EnvironmentVariable.Type"

    Type = Literal["plain", "secret"]


Environment = list[EnvironmentVariable]
