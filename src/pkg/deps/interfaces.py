from typing import List

from src.pkg.models.models import Amenity, Building


class RepositoryInterface:
    async def extract_amenities(self) -> List[Amenity]:
        raise NotImplementedError

    async def extract_buildings(self) -> List[Building]:
        raise NotImplementedError

    async def load_amenities(self, amenities: List[Amenity]):
        raise NotImplementedError

    async def load_buildings(self, buildings: List[Building]):
        raise NotImplementedError

    async def get_amenities(self) -> List[Amenity]:
        raise NotImplementedError

    async def get_buildings(self) -> List[Building]:
        raise NotImplementedError

    async def update_amenity(self, amenity: Amenity):
        raise NotImplementedError

    async def update_building(self, building: Building):
        raise NotImplementedError


class ServiceInterface:
    async def sync_buildings(self):
        raise NotImplementedError

    async def sync_amenities(self):
        raise NotImplementedError
