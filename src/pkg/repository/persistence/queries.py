import json
from datetime import datetime

from sqlalchemy import text
from uuid import uuid4
from typing import Optional, List

from src.pkg.infrastructure.postgresql import DatabaseSessionManager
from src.pkg.models.models import Amenity, Building


class PersistenceRepository:
    def __init__(self, db: DatabaseSessionManager):
        self.db = db

    async def load_amenity(
        self,
        osm_id: int,
        name: Optional[str],
        amenity_type: Optional[str],
        address: Optional[str],
        opening_hours: Optional[str],
        geometry: str,
        updated_at: datetime,
        updated_by: str,
    ):
        query = text(
            """
            INSERT INTO amenities (id, osm_id, name, amenity_type, address, opening_hours, geometry, updated_at, updated_by)
            VALUES (:id, :osm_id, :name, :amenity_type, :address, :opening_hours, ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326), :updated_at, :updated_by)
            ON CONFLICT (osm_id) DO NOTHING
        """
        )
        async with self.db.session() as session:
            await session.execute(
                query,
                {
                    "id": str(uuid4()),
                    "osm_id": osm_id,
                    "name": name,
                    "amenity_type": amenity_type,
                    "address": address,
                    "opening_hours": opening_hours,
                    "geometry": geometry,
                    "updated_at": updated_at,
                    "updated_by": updated_by,
                },
            )
            await session.commit()

    async def get_amenities(self) -> List[Amenity]:
        async with self.db.session() as session:
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
        async with self.db.session() as session:
            await session.execute(query, {"new_name": new_name, "id": amenity_id})
            await session.commit()

    async def delete_amenity(self, amenity_id: str):
        query = text(
            """
            DELETE FROM amenities
            WHERE id = :id
        """
        )
        async with self.db.session() as session:
            await session.execute(query, {"id": amenity_id})
            await session.commit()

    async def update_amenity(self):
        pass

    async def load_building(self, osm_id: int, metadata: dict, geometry: str):
        print(geometry)
        query = text(
            """
            INSERT INTO buildings (id, osm_id, information, geometry)
            VALUES (:id, :osm_id, :information, ST_SetSRID(ST_GeomFromGeoJSON(:geometry), 4326))
            ON CONFLICT (osm_id) DO NOTHING
        """
        )
        async with self.db.session() as session:
            await session.execute(
                query,
                {
                    "id": str(uuid4()),
                    "osm_id": osm_id,
                    "information": json.dumps(metadata),
                    "geometry": geometry,
                },
            )
            await session.commit()

    async def get_buildings(self) -> List[Building]:
        query = text("SELECT * FROM buildings")
        async with self.db.session() as session:
            result = await session.execute(query)
        return [Building(**row) for row in result]

    async def update_metadata(self, building_id: str, new_metadata: dict):
        query = text(
            """
            UPDATE buildings
            SET information = :new_metadata
            WHERE id = :id
        """
        )
        async with self.db.session() as session:
            await session.execute(
                query, {"information": new_metadata, "id": building_id}
            )
            await session.commit()

    async def delete_building(self, building_id: str):
        query = text(
            """
            DELETE FROM buildings
            WHERE id = :id
        """
        )
        async with self.db.session() as session:
            await session.execute(query, {"id": building_id})
            await session.commit()

    async def update_building(self):
        pass
