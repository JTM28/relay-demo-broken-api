from functools import lru_cache

from app.state import get_demo_state
from services.agent_service import AgentService
from services.analysis_service import ComparisonService
from services.items_service import ItemService
from services.session_service import SessionService


@lru_cache
def _get_item_service() -> ItemService:
    return ItemService(get_demo_state())


@lru_cache
def _get_agent_service() -> AgentService:
    return AgentService(get_demo_state())


@lru_cache
def _get_session_service() -> SessionService:
    return SessionService(get_demo_state())


@lru_cache
def _get_comparison_service() -> ComparisonService:
    return ComparisonService(_get_session_service())


def get_item_service() -> ItemService:
    return _get_item_service()


def get_agent_service() -> AgentService:
    return _get_agent_service()


def get_session_service() -> SessionService:
    return _get_session_service()


def get_comparison_service() -> ComparisonService:
    return _get_comparison_service()
