from fastapi import APIRouter, FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

api_router = APIRouter(prefix="/api")

# function for enabling CORS on web server
def setup_middleware(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_static(app: FastAPI):
    app.mount("/static", StaticFiles(directory="static"), name="static")
