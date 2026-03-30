from app.errors import ResourceNotFoundError
from app.state import DemoState
from models.agent import AgentProfile


class AgentService:
    def __init__(self, state: DemoState) -> None:
        self._state = state

    def list_agents(self, *, label: str | None = None) -> list[AgentProfile]:
        agents = list(self._state.agents.values())
        if label:
            normalized = label.strip().lower()
            agents = [agent for agent in agents if normalized in (value.lower() for value in agent.labels)]
        return sorted(agents, key=lambda agent: agent.display_name)

    def get_agent(self, agent_id: str) -> AgentProfile:
        agent = self._state.agents.get(agent_id)
        if agent is None:
            raise ResourceNotFoundError("agent", agent_id)
        return agent
