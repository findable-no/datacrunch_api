from dataclasses import dataclass


ComputeValue = dict[str, str]


@dataclass
class Compute:
    name: "Compute.Names"

    class Names(str):
        A100_40GB = "A100 40GB"
        GENERAL = "General Compute"
        H100 = "H100"
        L40S = "L40S"
        RTX6000_ADA = "RTX6000 Ada"

    def to_dict(self) -> ComputeValue:
        return {"name": self.name}
