from dataclasses import dataclass, field
from typing import Literal
from dataclasses_json import config, dataclass_json  # type: ignore
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
    contract: Contract | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    coupon: str | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    existing_volumes: list[str] | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    is_spot: bool | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    location_code: str | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    os_volume: OSVolume | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    pricing: Pricing | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    ssh_key_ids: list[str] | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
    volumes: list[Volume] | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )


@dataclass_json
@dataclass(frozen=True)
class InstanceAction:
    action: Action
    instance_id: str
    volume_ids: list[str] | None = field(
        default=None, metadata=config(exclude=lambda f: f is None)  # type: ignore
    )
