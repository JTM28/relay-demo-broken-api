from enum import Enum


class Priority(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

    @property
    def sort_rank(self) -> int:
        return {
            Priority.HIGH: 0,
            Priority.MEDIUM: 1,
            Priority.LOW: 2,
        }[self]


class WorkItemStatus(str, Enum):
    READY = "ready"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"


class SessionStatus(str, Enum):
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETE = "complete"


class CheckpointStatus(str, Enum):
    PENDING = "pending"
    ACTIVE = "active"
    COMPLETE = "complete"


class ChangeSurface(str, Enum):
    CONTAINED = "contained"
    MODERATE = "moderate"
    BROAD = "broad"


class SignalLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ComparisonConfidence(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
