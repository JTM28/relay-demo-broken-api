from dataclasses import dataclass
from datetime import datetime

from models.common import (
    ChangeSurface,
    CheckpointStatus,
    ComparisonConfidence,
    SessionStatus,
    SignalLevel,
)


@dataclass(frozen=True, slots=True)
class ProposalPosition:
    id: str
    label: str
    proposed_by: str
    summary: str
    strengths: tuple[str, ...]
    risks: tuple[str, ...]
    assumptions: tuple[str, ...]
    consequence_profile: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class SessionCheckpoint:
    label: str
    status: CheckpointStatus
    note: str


@dataclass(frozen=True, slots=True)
class NegotiationSession:
    id: str
    item_id: str
    title: str
    summary: str
    status: SessionStatus
    participant_ids: tuple[str, ...]
    checkpoints: tuple[SessionCheckpoint, ...]
    positions: tuple[ProposalPosition, ...]
    next_action: str
    updated_at: datetime


@dataclass(frozen=True, slots=True)
class ComparisonOption:
    label: str
    summary: str
    strengths: tuple[str, ...]
    risks: tuple[str, ...]
    assumptions: tuple[str, ...]
    change_surface: ChangeSurface
    operability: SignalLevel
    adaptability: SignalLevel


@dataclass(frozen=True, slots=True)
class ComparisonSideScore:
    label: str
    total_score: int
    highlights: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ComparisonOutcome:
    session_id: str
    focus_areas: tuple[str, ...]
    leading_option: str
    confidence: ComparisonConfidence
    rationale: tuple[str, ...]
    left: ComparisonSideScore
    right: ComparisonSideScore
