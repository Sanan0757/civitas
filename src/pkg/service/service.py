from typing import List

from src.pkg.deps.interfaces import ServiceInterface, RepositoryInterface
from src.pkg.repository.persistence.models import Building, Amenity


class Service(ServiceInterface):
    def __init__(self, repository: RepositoryInterface):
        self.repository = repository

    async def sync_buildings(self):
        # try:
        buildings = await self.repository.extract_buildings()
        await self.repository.load_buildings(buildings)
        # except Exception as e:
        #     print(f"Error syncing buildings: {e}")

    async def sync_amenities(self):
        try:
            amenities = await self.repository.extract_amenities()
            await self.repository.load_amenities(amenities)
        except Exception as e:
            print(f"Error syncing amenities: {e}")

    async def get_buildings(self) -> List[Building]:
        return await self.repository.get_buildings()

    async def get_amenities(self) -> List[Amenity]:
        return await self.repository.get_amenities()

    async def update_building(self, building: Building):
        await self.repository.update_building(building)

    async def update_amenity(self, amenity: Amenity):
        await self.repository.update_amenity(amenity)
