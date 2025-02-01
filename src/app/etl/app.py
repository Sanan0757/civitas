from src.pkg.config import get_settings

from src.pkg.infrastructure.postgresql import DatabaseSessionManager
from src.pkg.repository.repository import Repository
from src.pkg.service.service import Service
from src.pkg.deps.interfaces import ServiceInterface


class ETLApp:
    def __init__(self, config, service: ServiceInterface):
        self.config = config
        self.service = service

    async def __call__(self):
        await self.sync()

    async def sync(self):
        # await self.service.sync_buildings()
        await self.service.sync_amenities()


def create_etl_app() -> ETLApp:
    settings = get_settings()
    db = DatabaseSessionManager(str(settings.get_db_url()))
    repo = Repository(bounding_box=settings.BOUNDING_BOX, db=db)
    service = Service(repo)

    return ETLApp(config=settings, service=service)
