from fastapi import APIRouter, Depends, Query

from app.dependencies import get_agent_service
from contracts.agent import AgentDetailContract, AgentListContract, AgentSummaryContract
from services.agent_service import AgentService


router = APIRouter(tags=["agents"])


def _to_summary(agent) -> AgentSummaryContract:
    return AgentSummaryContract(
        id=agent.id,
        display_name=agent.display_name,
        owner=agent.owner,
        specialty=agent.specialty,
        labels=list(agent.labels),
        active_item_ids=list(agent.active_item_ids),
    )


def _to_detail(agent) -> AgentDetailContract:
    return AgentDetailContract(
        **_to_summary(agent).model_dump(),
        focus_summary=agent.focus_summary,
        strengths=list(agent.strengths),
        availability_note=agent.availability_note,
        updated_at=agent.updated_at.isoformat(),
    )


@router.get("/agents", response_model=AgentListContract)
async def list_agents(
    label: str | None = Query(default=None, description="Optional label filter."),
    service: AgentService = Depends(get_agent_service),
) -> AgentListContract:
    return AgentListContract(agents=[_to_summary(agent) for agent in service.list_agents(label=label)])


@router.get("/agents/{agent_id}", response_model=AgentDetailContract)
async def get_agent(agent_id: str, service: AgentService = Depends(get_agent_service)) -> AgentDetailContract:
    return _to_detail(service.get_agent(agent_id))
