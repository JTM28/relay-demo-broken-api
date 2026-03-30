from pydantic import BaseModel, Field


class AgentSummaryContract(BaseModel):
    id: str = Field(description="Opaque agent identifier.")
    display_name: str = Field(description="Friendly display name for the agent.")
    owner: str = Field(description="Developer or team responsible for the agent.")
    specialty: str = Field(description="Primary operating area for the agent.")
    labels: list[str] = Field(description="Neutral labels describing role and focus.")
    active_item_ids: list[str] = Field(description="Backlog items the agent is currently touching.")


class AgentDetailContract(AgentSummaryContract):
    focus_summary: str = Field(description="Current working posture for the agent.")
    strengths: list[str] = Field(description="Capabilities the agent tends to contribute.")
    availability_note: str = Field(description="How the agent prefers to work with others.")
    updated_at: str = Field(description="UTC timestamp for the most recent profile refresh.")


class AgentListContract(BaseModel):
    agents: list[AgentSummaryContract]
