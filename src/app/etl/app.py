from src.pkg.config import get_settings

from .etl import ETLApp
from src.pkg.infrastructure.postgresql import Database
from src.pkg.repository.repository import Repository
from src.pkg.service.service import Service


def create_etl_app() -> ETLApp:
    settings = get_settings()
    db = Database(str(settings.DATABASE_PG_URL))
    repo = Repository(bounding_box=settings.BOUNDING_BOX, db=db)
    service = Service(repo)

    return ETLApp(config=settings, service=service)
