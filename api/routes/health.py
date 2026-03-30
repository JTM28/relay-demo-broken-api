from fastapi import APIRouter

from app.config import get_settings
from app.state import get_demo_state
from contracts.health import HealthContract


router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthContract)
async def get_health() -> HealthContract:
    settings = get_settings()
    state = get_demo_state()
    return HealthContract(
        service=settings.app_name,
        environment=settings.environment,
        version=settings.app_version,
        seed_version=state.seed_version,
        storage_mode="in_memory",
        resource_counts={
            "items": len(state.items),
            "agents": len(state.agents),
            "sessions": len(state.sessions),
        },
    )
