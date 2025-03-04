from dataclasses import dataclass
from typing import Literal
from dataclasses_json import dataclass_json  # type: ignore


@dataclass_json
@dataclass(frozen=True)
class EnvironmentVariable:
    name: str
    value_or_reference_to_secret: str
    type: "EnvironmentVariable.Type"

    Type = Literal["plain", "secret"]


Environment = list[EnvironmentVariable]
