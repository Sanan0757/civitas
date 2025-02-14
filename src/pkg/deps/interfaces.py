from abc import ABC, abstractmethod

from typing import List

from src.pkg.models import Amenity, Building, BuildingUpdate, AmenityUpdate


class RepositoryInterface(ABC):
    @abstractmethod
    async def load_amenities(self, amenities: List[Amenity]):
        raise NotImplementedError

    @abstractmethod
    async def load_buildings(self, buildings: List[Building]):
        raise NotImplementedError

    @abstractmethod
    async def get_amenities(self) -> List[Amenity]:
        raise NotImplementedError

    @abstractmethod
    async def get_buildings(self) -> List[Building]:
        raise NotImplementedError

    @abstractmethod
    async def update_building(self, building_id: str, update: BuildingUpdate):
        raise NotImplementedError

    @abstractmethod
    async def update_amenity(self, amenity_id: str, update: AmenityUpdate):
        raise NotImplementedError


class ServiceInterface(ABC):
    @abstractmethod
    async def sync_buildings(self):
        raise NotImplementedError

    @abstractmethod
    async def sync_amenities(self):
        raise NotImplementedError

    @abstractmethod
    async def get_buildings(self) -> List[Building]:
        raise NotImplementedError

    @abstractmethod
    async def get_amenities(self) -> List[Amenity]:
        raise NotImplementedError
