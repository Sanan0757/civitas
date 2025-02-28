import logging
import uuid
from typing import List
from aiocache import cached, caches

from src.pkg.deps.interfaces import RepositoryInterface
from src.pkg.models import Amenity, Building, BuildingUpdate, AmenityUpdate
from src.pkg.models.enums import AmenityCategory
from src.pkg.repository.persistence.queries import PersistenceRepository

logger = logging.getLogger(__name__)


class Repository(RepositoryInterface):
    def __init__(self, db):
        super().__init__()
        self._persistence_repo = PersistenceRepository(db)

    @cached(ttl=3600, key="cached_amenities")  # Cache for 1 hour
    async def get_amenities(self) -> List[Amenity]:
        """Fetch amenities with caching (expires in 1 hour)."""
        logger.info("Fetching amenities from database...")
        return await self._persistence_repo.get_amenities()

    @cached(ttl=3600, key="cached_buildings")  # Cache for 1 hour
    async def get_buildings(self) -> List[Building]:
        """Fetch buildings with caching (expires in 1 hour)."""
        logger.info("Fetching buildings from database...")
        return await self._persistence_repo.get_buildings()

    async def update_amenity(self, amenity_id: str, update: AmenityUpdate):
        """Update amenity and invalidate cache."""
        await self._persistence_repo.update_amenity(uuid.UUID(amenity_id), update)
        await self.invalidate_cache("cached_amenities")  # Clear cache

    async def update_building(self, building_id: str, update: BuildingUpdate):
        """Update building and invalidate cache."""
        await self._persistence_repo.update_building(uuid.UUID(building_id), update)
        await self.invalidate_cache("cached_buildings")  # Clear cache

    async def load_amenities(self, amenities: List[Amenity]):
        """Load multiple amenities into DB and invalidate cache."""
        logger.info(f"Loading {len(amenities)} amenities...")
        await self._persistence_repo.load_amenities(amenities)
        await self.invalidate_cache("cached_amenities")  # Clear cache after insert

    async def load_buildings(self, buildings: List[Building]):
        """Load multiple buildings into DB and invalidate cache."""
        logger.info(f"Loading {len(buildings)} buildings...")

        await self._persistence_repo.load_buildings(buildings)
        await self.invalidate_cache("cached_buildings")  # Clear cache after insert

    async def get_building_amenity(self, building_id: str) -> Amenity:
        return await self._persistence_repo.get_building_amenity(uuid.UUID(building_id))

    async def get_building(self, building_id: str) -> Building:
        return await self._persistence_repo.get_building(uuid.UUID(building_id))

    async def assign_closest_amenities(self):
        return await self._persistence_repo.assign_closest_amenities()

    async def get_closest_amenity(
        self, building_id: str, category: AmenityCategory
    ) -> Amenity:
        return await self._persistence_repo.find_closest_amenity_by_category(
            uuid.UUID(building_id), category
        )

    @staticmethod
    async def invalidate_cache(key: str):
        """Invalidate cache when data changes."""
        cache = caches.get("default")
        await cache.delete(key)
        logger.info(f"Cache invalidated for key: {key}")
