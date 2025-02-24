from dataclasses import dataclass
from typing import Literal
from dataclasses_json import dataclass_json
from .volume import Volume

Action = Literal[
    "boot",
    "configure_spot",
    "delete",
    "discontinue",
    "force_shutdown",
    "hibernate",
    "start",
    "shutdown",
]
Contract = Literal["LONG_TERM", "PAY_AS_YOU_GO", "SPOT"]
Currency = Literal["USD", "EUR"]
Pricing = Literal["DYNAMIC_PRICE", "FIXED_PRICE"]


DEFAULT_CURRENCY = "EUR"


@dataclass_json
@dataclass(frozen=True)
class OSVolume:
    name: str
    size: int


@dataclass_json
@dataclass(frozen=True)
class Instance:
    description: str
    hostname: str
    image: str
    instance_type: str
    contract: Contract | None = None
    coupon: str | None = None
    existing_volumes: list[str] | None = None
    is_spot: bool | None = None
    location_code: str | None = None
    os_volume: OSVolume | None = None
    pricing: Pricing | None = None
    ssh_key_ids: list[str] | None = None
    volumes: list[Volume] | None = None


@dataclass_json
@dataclass(frozen=True)
class InstanceAction:
    action: Action
    instance_id: str
    volume_ids: list[str] | None = None
