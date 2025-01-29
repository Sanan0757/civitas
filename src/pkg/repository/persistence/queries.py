from sqlalchemy import text
from uuid import uuid4
from typing import Optional, List

from src.pkg.infrastructure.postgresql import Database
from src.pkg.models.models import Amenity, Building


class AmenityRepository:
    def __init__(self, db: Database):
        self.db = db

    async def load_amenity(
        self,
        overpass_id: int,
        name: Optional[str],
        amenity_type: Optional[str],
        address: Optional[str],
        opening_hours: Optional[str],
        geometry: str,
    ):
        query = text(
            """
            INSERT INTO amenities (id, overpass_id, name, amenity_type, address, opening_hours, geometry)
            VALUES (:id, :overpass_id, :name, :amenity_type, :address, :opening_hours, ST_GeomFromText(:geometry, 4326))
        """
        )
        async with self.db.get_session() as session:
            await session.execute(
                query,
                {
                    "id": str(uuid4()),
                    "overpass_id": overpass_id,
                    "name": name,
                    "amenity_type": amenity_type,
                    "address": address,
                    "opening_hours": opening_hours,
                    "geometry": geometry,
                },
            )
            await session.commit()

    async def get_amenities(self) -> List[Amenity]:
        async with self.db.get_session() as session:
            query = text("SELECT * FROM amenities")
            result = await session.execute(query)
        return [Amenity(**dict(row)) for row in result]

    async def update_name(self, amenity_id: str, new_name: str):
        query = text(
            """
            UPDATE amenities
            SET name = :new_name
            WHERE id = :id
        """
        )
        async with self.db.get_session() as session:
            await session.execute(query, {"new_name": new_name, "id": amenity_id})
            await session.commit()

    async def delete(self, amenity_id: str):
        query = text(
            """
            DELETE FROM amenities
            WHERE id = :id
        """
        )
        async with self.db.get_session() as session:
            await session.execute(query, {"id": amenity_id})
            await session.commit()

    async def update_amenity(self):
        pass


class BuildingRepository:
    def __init__(self, db: Database):
        self.db = db

    async def load_building(self, overpass_id: int, metadata: dict, geometry: str):
        query = text(
            """
            INSERT INTO buildings (id, overpass_id, metadata, geometry)
            VALUES (:id, :overpass_id, :metadata, ST_GeomFromText(:geometry, 4326))
        """
        )
        async with self.db.get_session() as session:
            await session.execute(
                query,
                {
                    "id": str(uuid4()),
                    "overpass_id": overpass_id,
                    "metadata": metadata,
                    "geometry": geometry,
                },
            )
            await session.commit()

    async def get_buildings(self) -> List[Building]:
        query = text("SELECT * FROM buildings")
        async with self.db.get_session() as session:
            result = await session.execute(query)
        return [Building(**row) for row in result]

    async def update_metadata(self, building_id: str, new_metadata: dict):
        query = text(
            """
            UPDATE buildings
            SET metadata = :new_metadata
            WHERE id = :id
        """
        )
        async with self.db.get_session() as session:
            await session.execute(
                query, {"new_metadata": new_metadata, "id": building_id}
            )
            await session.commit()

    async def delete(self, building_id: str):
        query = text(
            """
            DELETE FROM buildings
            WHERE id = :id
        """
        )
        async with self.db.get_session() as session:
            await session.execute(query, {"id": building_id})
            await session.commit()

    async def update_building(self):
        pass
