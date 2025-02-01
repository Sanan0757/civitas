from urllib.parse import quote_plus

from typing import Callable

from dotenv import load_dotenv
from pydantic import PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ENV: str = "dev"
    LOG_LEVEL: str = "DEBUG"
    DATABASE_PG_URL: PostgresDsn = "postgresql://neondb_owner:npg_jrUpozuT7g0y@ep-black-sky-a2vsl2a2-pooler.eu-central-1.aws.neon.tech/neondb"
    BOUNDING_BOX: tuple[float, ...] = (34.9500, 14.1800, 36.0800, 14.6000)

    def get_db_url(self) -> str:
        """Return database URL with asyncpg for async SQLAlchemy."""
        return str(self.DATABASE_PG_URL).replace(
            "postgresql://", "postgresql+asyncpg://"
        )


def _configure_initial_settings() -> Callable[[], Settings]:
    load_dotenv()
    settings = Settings()

    def fn() -> Settings:
        return settings

    return fn


get_settings = _configure_initial_settings()
