from dataclasses import dataclass


VolumeMountValue = dict[str, str]


@dataclass
class VolumeMount:
    type: "VolumeMount.Type"
    mount_path: str

    class Type(str):
        SCRATCH = "scratch"

    def to_dict(self) -> VolumeMountValue:
        return {
            "type": self.type,
            "mount_path": self.mount_path,
        }


VolumeMountsValue = list[VolumeMountValue]


class VolumeMounts(list[VolumeMount]):
    def to_list(self) -> VolumeMountsValue:
        return [volume_mount.to_dict() for volume_mount in self]
