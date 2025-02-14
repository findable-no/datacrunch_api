from dataclasses import dataclass
from dataclasses_json import dataclass_json  # type: ignore


@dataclass_json
@dataclass(frozen=True)
class ScalingPolicy:
    delay_seconds: int


@dataclass_json
@dataclass(frozen=True)
class QueueLoad:
    threshold: int


@dataclass_json
@dataclass(frozen=True)
class ScalingTriggers:
    queue_load: QueueLoad


@dataclass_json
@dataclass(frozen=True)
class Scaling:
    min_replica_count: int
    max_replica_count: int
    queue_message_ttl_seconds: int
    concurrent_requests_per_replica: int
    scale_down_policy: ScalingPolicy
    scale_up_policy: ScalingPolicy
    scaling_triggers: ScalingTriggers
