from fastapi import FastAPI

from src.app.web.events import lifespan
from src.pkg.config.env import get_settings
from src.app.web.api import api_router

settings = get_settings()


def create_web_app() -> FastAPI:
    app = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
        # openapi_url=f"{settings.API_V1_STR}/openapi.json",
        # generate_unique_id_function=lambda router: f"{router.tags[0]}-{router.name}",
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app
