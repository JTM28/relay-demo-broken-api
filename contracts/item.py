from pydantic import BaseModel, Field

from models.common import Priority, WorkItemStatus


class ItemSummaryContract(BaseModel):
    id: str = Field(description="Opaque item identifier.")
    title: str = Field(description="Short work item title.")
    summary: str = Field(description="Plain-language explanation of the work item.")
    priority: Priority
    status: WorkItemStatus
    labels: list[str] = Field(description="Neutral labels for discovery and filtering.")
    active_session_ids: list[str] = Field(description="Related negotiation sessions.")


class ItemDetailContract(ItemSummaryContract):
    target_outcome: str = Field(description="What a successful outcome looks like.")
    open_questions: list[str] = Field(description="Questions still unresolved for the item.")
    active_agent_ids: list[str] = Field(description="Agents currently involved with the item.")
    updated_at: str = Field(description="UTC timestamp for the most recent item refresh.")


class ItemListContract(BaseModel):
    items: list[ItemSummaryContract]
