import logging
from typing import List
from aiocache import cached, caches

from src.pkg.deps.interfaces import RepositoryInterface
from src.pkg.models import Amenity, Building
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

    async def update_amenity(self, amenity: Amenity):
        """Update amenity and invalidate cache."""
        await self._persistence_repo.update_name(amenity.id, amenity.name)
        await self.invalidate_cache("cached_amenities")  # Clear cache

    async def update_building(self, building: Building):
        """Update building and invalidate cache."""
        await self._persistence_repo.update_metadata(building.id, building.metadata)
        await self.invalidate_cache("cached_buildings")  # Clear cache

    async def load_amenities(self, amenities: List[Amenity]):
        """Load multiple amenities into DB and invalidate cache."""
        logger.info(f"Loading {len(amenities)} amenities...")
        for amenity in amenities:
            await self._persistence_repo.load_amenity(
                amenity.osm_id,
                amenity.name,
                amenity.amenity_type,
                amenity.address,
                amenity.opening_hours,
                amenity.geometry,
                amenity.updated_at,
                amenity.updated_by,
            )
        await self.invalidate_cache("cached_amenities")  # Clear cache after insert

    async def load_buildings(self, buildings: List[Building]):
        """Load multiple buildings into DB and invalidate cache."""
        logger.info(f"Loading {len(buildings)} buildings...")
        for building in buildings:
            await self._persistence_repo.load_building(
                building.osm_id, building.information, building.geometry
            )
        await self.invalidate_cache("cached_buildings")  # Clear cache after insert

    @staticmethod
    async def invalidate_cache(self, key: str):
        """Invalidate cache when data changes."""
        cache = caches.get("default")
        await cache.delete(key)
        logger.info(f"Cache invalidated for key: {key}")
