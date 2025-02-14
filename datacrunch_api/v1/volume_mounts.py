from dataclasses import dataclass
from typing import Literal
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class VolumeMount:
    type: "VolumeMount.Type"
    mount_path: str

    Type = Literal["scratch"]


VolumeMounts = list[VolumeMount]
