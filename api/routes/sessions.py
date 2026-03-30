from fastapi import APIRouter, Depends, Query

from app.dependencies import get_comparison_service, get_session_service
from contracts.session import (
    ComparisonRequestContract,
    ComparisonResponseContract,
    ComparisonSideScoreContract,
    SessionCheckpointContract,
    SessionDetailContract,
    SessionListContract,
    SessionProposalContract,
    SessionSummaryContract,
)
from models.common import SessionStatus
from models.session import ComparisonOption
from services.analysis_service import ComparisonService
from services.session_service import SessionService


router = APIRouter(tags=["sessions"])


def _to_summary(session) -> SessionSummaryContract:
    return SessionSummaryContract(
        id=session.id,
        item_id=session.item_id,
        title=session.title,
        summary=session.summary,
        status=session.status,
        participant_ids=list(session.participant_ids),
        next_action=session.next_action,
    )


def _to_detail(session) -> SessionDetailContract:
    return SessionDetailContract(
        **_to_summary(session).model_dump(),
        checkpoints=[
            SessionCheckpointContract(label=checkpoint.label, status=checkpoint.status, note=checkpoint.note)
            for checkpoint in session.checkpoints
        ],
        positions=[
            SessionProposalContract(
                id=position.id,
                label=position.label,
                proposed_by=position.proposed_by,
                summary=position.summary,
                strengths=list(position.strengths),
                risks=list(position.risks),
                assumptions=list(position.assumptions),
                consequence_profile=list(position.consequence_profile),
            )
            for position in session.positions
        ],
        updated_at=session.updated_at.isoformat(),
    )


def _to_option(payload) -> ComparisonOption:
    return ComparisonOption(
        label=payload.label,
        summary=payload.summary,
        strengths=tuple(payload.strengths),
        risks=tuple(payload.risks),
        assumptions=tuple(payload.assumptions),
        change_surface=payload.change_surface,
        operability=payload.operability,
        adaptability=payload.adaptability,
    )


@router.get("/sessions", response_model=SessionListContract)
async def list_sessions(
    status: SessionStatus | None = Query(default=None, description="Optional session status filter."),
    item_id: str | None = Query(default=None, description="Optional work item filter."),
    service: SessionService = Depends(get_session_service),
) -> SessionListContract:
    return SessionListContract(
        sessions=[_to_summary(session) for session in service.list_sessions(status=status, item_id=item_id)]
    )


@router.get("/sessions/{session_id}", response_model=SessionDetailContract)
async def get_session(
    session_id: str,
    service: SessionService = Depends(get_session_service),
) -> SessionDetailContract:
    return _to_detail(service.get_session(session_id))


@router.post("/sessions/{session_id}/compare", response_model=ComparisonResponseContract)
async def compare_session_options(
    session_id: str,
    request: ComparisonRequestContract,
    service: ComparisonService = Depends(get_comparison_service),
) -> ComparisonResponseContract:
    outcome = service.compare(
        session_id=session_id,
        focus_areas=request.focus_areas,
        left=_to_option(request.left),
        right=_to_option(request.right),
    )
    return ComparisonResponseContract(
        session_id=outcome.session_id,
        focus_areas=list(outcome.focus_areas),
        leading_option=outcome.leading_option,
        confidence=outcome.confidence,
        rationale=list(outcome.rationale),
        left=ComparisonSideScoreContract(
            label=outcome.left.label,
            total_score=outcome.left.total_score,
            highlights=list(outcome.left.highlights),
        ),
        right=ComparisonSideScoreContract(
            label=outcome.right.label,
            total_score=outcome.right.total_score,
            highlights=list(outcome.right.highlights),
        ),
    )
