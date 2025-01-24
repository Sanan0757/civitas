from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.app.web.events import lifespan
from src.pkg.config.env import get_settings
from src.app.web.api import api_router

settings = get_settings()


def create_web_app() -> FastAPI:
    # init FastAPI with lifespan
    app = FastAPI(
        lifespan=lifespan,
        title=settings.PROJECT_NAME,
        # openapi_url=f"{settings.API_V1_STR}/openapi.json",
        # generate_unique_id_function=lambda router: f"{router.tags[0]}-{router.name}",
    )
    # set CORS
    # Set all CORS enabled origins
    if settings.BACKEND_CORS_ORIGINS:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    # Include the routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app
