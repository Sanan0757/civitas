from typing import List

from src.pkg.deps.interfaces import RepositoryInterface
from src.pkg.models.models import Amenity, Building
from src.pkg.repository.overpass.client import Client
from src.pkg.repository.persistence.queries import AmenityRepository, BuildingRepository


class Repository(RepositoryInterface):
    def __init__(self, bounding_box, db):
        super().__init__()
        self.buildings_repo = BuildingRepository(db)
        self.amenities_repo = AmenityRepository(db)
        self.osm_client = Client(bounding_box)

    async def extract_amenities(self) -> List[Amenity]:
        return await self.osm_client.extract_amenities()

    async def extract_buildings(self) -> List[Building]:
        return await self.osm_client.extract_buildings()

    async def get_amenities(self) -> List[Amenity]:
        return await self.amenities_repo.get_amenities()

    async def get_buildings(self) -> List[Building]:
        return await self.buildings_repo.get_buildings()

    async def update_amenity(self, amenity: Amenity):
        await self.amenities_repo.update_name(amenity.id, amenity.name)

    async def update_building(self, building: Building):
        await self.buildings_repo.update_metadata(building.id, building.metadata)

    async def load_amenities(self, amenities: List[Amenity]):
        for amenity in amenities:
            await self.amenities_repo.load_amenity(
                amenity.overpass_id,
                amenity.name,
                amenity.amenity_type,
                amenity.address,
                amenity.opening_hours,
                amenity.geometry,
            )

    async def load_buildings(self, buildings: List[Building]):
        print(f"Loading buildings {len(buildings)}")
        for building in buildings:
            await self.buildings_repo.load_building(
                building.overpass_id, building.metadata, building.geometry_string
            )
