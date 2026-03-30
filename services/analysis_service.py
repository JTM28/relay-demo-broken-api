from app.errors import InvalidComparisonRequestError
from models.common import ChangeSurface, ComparisonConfidence, SignalLevel
from models.session import ComparisonOption, ComparisonOutcome, ComparisonSideScore
from services.session_service import SessionService


class ComparisonService:
    def __init__(self, session_service: SessionService) -> None:
        self._session_service = session_service

    def compare(
        self,
        *,
        session_id: str,
        focus_areas: list[str],
        left: ComparisonOption,
        right: ComparisonOption,
    ) -> ComparisonOutcome:
        session = self._session_service.get_session(session_id)
        normalized_focus = tuple(self._normalize_focus(focus_areas))
        if not normalized_focus:
            raise InvalidComparisonRequestError("At least one focus area is required for comparison.")

        left_score = self._score_option(left, normalized_focus)
        right_score = self._score_option(right, normalized_focus)

        if left_score.total_score == right_score.total_score:
            leading = left.label
            confidence = ComparisonConfidence.LOW
            rationale = (
                "Both options landed on the same score, so the recommendation is intentionally weak.",
                "Use the session context and open questions to break the tie during follow-up discussion.",
            )
        else:
            delta = abs(left_score.total_score - right_score.total_score)
            leading = left.label if left_score.total_score > right_score.total_score else right.label
            confidence = self._confidence_for_delta(delta)
            rationale = (
                f"{leading} aligned more strongly with the chosen focus areas for session {session.id}.",
                f"Score delta was {delta}, which produced a {confidence.value} confidence recommendation.",
                "This recommendation is advisory only and does not assume any specific persistence design.",
            )

        return ComparisonOutcome(
            session_id=session.id,
            focus_areas=normalized_focus,
            leading_option=leading,
            confidence=confidence,
            rationale=rationale,
            left=left_score,
            right=right_score,
        )

    def _score_option(self, option: ComparisonOption, focus_areas: tuple[str, ...]) -> ComparisonSideScore:
        score = 50 + (len(option.strengths) * 4) - (len(option.risks) * 3) + len(option.assumptions)
        highlights: list[str] = [
            f"{option.label} starts from a neutral base score and is adjusted by stated strengths, risks, and assumptions."
        ]

        for focus in focus_areas:
            if focus == "delivery_speed":
                focus_score = {
                    ChangeSurface.CONTAINED: 8,
                    ChangeSurface.MODERATE: 4,
                    ChangeSurface.BROAD: 1,
                }[option.change_surface]
                score += focus_score
                highlights.append(f"delivery_speed favored a {option.change_surface.value} change surface.")
            elif focus == "operability":
                focus_score = self._level_score(option.operability)
                score += focus_score
                highlights.append(f"operability added {focus_score} points from a {option.operability.value} profile.")
            elif focus == "adaptability":
                focus_score = self._level_score(option.adaptability)
                score += focus_score
                highlights.append(f"adaptability added {focus_score} points from a {option.adaptability.value} profile.")
            elif focus == "change_risk":
                focus_score = {
                    ChangeSurface.CONTAINED: 7,
                    ChangeSurface.MODERATE: 4,
                    ChangeSurface.BROAD: 0,
                }[option.change_surface]
                score += focus_score
                highlights.append(f"change_risk favored the {option.change_surface.value} rollout footprint.")
            elif focus == "team_alignment":
                focus_score = 2 + min(len(option.assumptions), 4)
                score += focus_score
                highlights.append(f"team_alignment rewarded explicit assumptions with {focus_score} points.")

        return ComparisonSideScore(label=option.label, total_score=score, highlights=tuple(highlights))

    def _confidence_for_delta(self, delta: int) -> ComparisonConfidence:
        if delta >= 12:
            return ComparisonConfidence.HIGH
        if delta >= 6:
            return ComparisonConfidence.MEDIUM
        return ComparisonConfidence.LOW

    def _level_score(self, value: SignalLevel) -> int:
        return {
            SignalLevel.LOW: 1,
            SignalLevel.MEDIUM: 4,
            SignalLevel.HIGH: 7,
        }[value]

    def _normalize_focus(self, focus_areas: list[str]) -> list[str]:
        allowed = {
            "adaptability",
            "change_risk",
            "delivery_speed",
            "operability",
            "team_alignment",
        }
        return [focus for focus in focus_areas if focus in allowed]
