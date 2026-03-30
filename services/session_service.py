from app.errors import ResourceNotFoundError
from app.state import DemoState
from models.common import SessionStatus
from models.session import NegotiationSession


class SessionService:
    def __init__(self, state: DemoState) -> None:
        self._state = state

    def list_sessions(
        self,
        *,
        status: SessionStatus | None = None,
        item_id: str | None = None,
    ) -> list[NegotiationSession]:
        sessions = list(self._state.sessions.values())
        if status is not None:
            sessions = [session for session in sessions if session.status is status]
        if item_id:
            sessions = [session for session in sessions if session.item_id == item_id]
        return sorted(sessions, key=lambda session: session.updated_at, reverse=True)

    def get_session(self, session_id: str) -> NegotiationSession:
        session = self._state.sessions.get(session_id)
        if session is None:
            raise ResourceNotFoundError("session", session_id)
        return session
