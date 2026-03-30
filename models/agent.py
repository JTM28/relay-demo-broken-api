from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class AgentProfile:
    id: str
    display_name: str
    owner: str
    specialty: str
    focus_summary: str
    strengths: tuple[str, ...]
    labels: tuple[str, ...]
    active_item_ids: tuple[str, ...]
    availability_note: str
    updated_at: datetime
