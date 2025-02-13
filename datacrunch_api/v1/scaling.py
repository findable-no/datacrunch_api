from dataclasses import dataclass


ScalingPolicyValue = dict[str, int]


@dataclass
class ScalingPolicy:
    delay_seconds: int

    def to_dict(self) -> ScalingPolicyValue:
        return {
            "delay_seconds": self.delay_seconds,
        }


QueueLoadValue = dict[str, int]


@dataclass
class QueueLoad:
    threshold: int

    def to_dict(self) -> QueueLoadValue:
        return {
            "threshold": self.threshold,
        }


ScalingTriggersValue = dict[str, QueueLoadValue]


@dataclass
class ScalingTriggers:
    queue_load: QueueLoad

    def to_dict(self) -> ScalingTriggersValue:
        return {
            "queue_load": self.queue_load.to_dict(),
        }


ScalingValue = dict[str, int | ScalingPolicyValue | ScalingTriggersValue]


@dataclass
class Scaling:
    min_replica_count: int
    max_replica_count: int
    queue_message_ttl_seconds: int
    concurrent_requests_per_replica: int
    scale_down_policy: ScalingPolicy
    scale_up_policy: ScalingPolicy
    scaling_triggers: ScalingTriggers

    def to_dict(self) -> ScalingValue:
        return {
            "min_replica_count": self.min_replica_count,
            "max_replica_count": self.max_replica_count,
            "queue_message_ttl_seconds": self.queue_message_ttl_seconds,
            "concurrent_requests_per_replica": self.concurrent_requests_per_replica,
            "scale_down_policy": self.scale_down_policy.to_dict(),
            "scale_up_policy": self.scale_up_policy.to_dict(),
            "scaling_triggers": self.scaling_triggers.to_dict(),
        }
