from typing import Callable

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    LOG_LEVEL: str = "DEBUG"
    DATABASE_PG_URL: PostgresDsn = "postgresql://postgres:s9VV.L*UN$dq.C5@db.vfiqzorqjrncykxfadok.supabase.co:5432/postgres"
    BOUNDING_BOX: tuple[float, ...] = (34.9500, 14.1800, 36.0800, 14.6000)


def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()

    def fn() -> Settings:
        return settings

    return fn


get_settings = _configure_initial_settings()
