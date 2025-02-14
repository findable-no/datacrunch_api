from dataclasses import dataclass
from typing import Literal
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class Compute:
    name: "Compute.Names"

    Names = Literal["A100 40GB", "General Compute", "H100", "L40S", "RTX6000 Ada"]
