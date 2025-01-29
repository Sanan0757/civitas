import uuid

from sqlalchemy import Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID

from geoalchemy2 import Geometry

Base = declarative_base()


class Amenity(Base):
    __tablename__ = "amenities"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    overpass_id = Column(Integer, unique=True, nullable=False)
    name = Column(String, nullable=True)
    amenity_type = Column(String, nullable=True)
    address = Column(String, nullable=True)
    opening_hours = Column(String, nullable=True)
    geometry = Column(Geometry("POINT"), nullable=False)  # Geometry column for points


class Building(Base):
    __tablename__ = "buildings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
    overpass_id = Column(Integer, unique=True, nullable=False)
    information = Column(JSON, nullable=False)  # Stores metadata as a JSON object
    geometry = Column(
        Geometry("POLYGON"), nullable=False
    )  # Geometry column for polygons
