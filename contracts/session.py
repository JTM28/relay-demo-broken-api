from pydantic import BaseModel, Field

from models.common import (
    ChangeSurface,
    CheckpointStatus,
    ComparisonConfidence,
    SessionStatus,
    SignalLevel,
)


class SessionCheckpointContract(BaseModel):
    label: str = Field(description="Named milestone or gate in the session.")
    status: CheckpointStatus
    note: str = Field(description="Why the checkpoint matters right now.")


class SessionProposalContract(BaseModel):
    id: str = Field(description="Opaque proposal identifier.")
    label: str = Field(description="Short proposal label.")
    proposed_by: str = Field(description="Agent identifier that originated the position.")
    summary: str = Field(description="What the proposal is trying to accomplish.")
    strengths: list[str]
    risks: list[str]
    assumptions: list[str]
    consequence_profile: list[str] = Field(description="Likely outcomes if the proposal is pursued.")


class SessionSummaryContract(BaseModel):
    id: str = Field(description="Opaque session identifier.")
    item_id: str = Field(description="Related work item identifier.")
    title: str
    summary: str
    status: SessionStatus
    participant_ids: list[str]
    next_action: str


class SessionDetailContract(SessionSummaryContract):
    checkpoints: list[SessionCheckpointContract]
    positions: list[SessionProposalContract]
    updated_at: str = Field(description="UTC timestamp for the most recent session refresh.")


class SessionListContract(BaseModel):
    sessions: list[SessionSummaryContract]


class ComparisonOptionContract(BaseModel):
    label: str = Field(description="Short name for the candidate direction.")
    summary: str = Field(description="Plain-language description of the option.")
    strengths: list[str] = Field(min_length=1)
    risks: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    change_surface: ChangeSurface
    operability: SignalLevel
    adaptability: SignalLevel


class ComparisonRequestContract(BaseModel):
    focus_areas: list[str] = Field(
        default_factory=lambda: ["delivery_speed", "operability", "adaptability"],
        description="Neutral evaluation lenses chosen by the caller.",
    )
    left: ComparisonOptionContract
    right: ComparisonOptionContract


class ComparisonSideScoreContract(BaseModel):
    label: str
    total_score: int
    highlights: list[str]


class ComparisonResponseContract(BaseModel):
    session_id: str
    focus_areas: list[str]
    leading_option: str
    confidence: ComparisonConfidence
    rationale: list[str]
    left: ComparisonSideScoreContract
    right: ComparisonSideScoreContract
