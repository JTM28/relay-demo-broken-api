from dataclasses import dataclass
from datetime import datetime

from models.common import Priority, WorkItemStatus


@dataclass(frozen=True, slots=True)
class WorkItem:
    id: str
    title: str
    summary: str
    priority: Priority
    status: WorkItemStatus
    target_outcome: str
    open_questions: tuple[str, ...]
    labels: tuple[str, ...]
    active_agent_ids: tuple[str, ...]
    active_session_ids: tuple[str, ...]
    updated_at: datetime
