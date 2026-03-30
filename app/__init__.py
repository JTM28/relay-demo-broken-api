from fastapi import FastAPI

from api.router import api_router
from app.config import get_settings
from app.errors import register_error_handlers
from app.metadata import API_DESCRIPTION, API_TAGS


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description=API_DESCRIPTION,
        openapi_tags=API_TAGS,
        docs_url="/docs",
        redoc_url="/redoc",
    )
    register_error_handlers(app)
    app.include_router(api_router)
    return app
