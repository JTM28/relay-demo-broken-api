from fastapi import APIRouter

from api.routes.agents import router as agents_router
from api.routes.health import router as health_router
from api.routes.items import router as items_router
from api.routes.sessions import router as sessions_router


api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(items_router)
api_router.include_router(agents_router)
api_router.include_router(sessions_router)
