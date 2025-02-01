from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Amenity(BaseModel):
    osm_id: int
    name: Optional[str]
    amenity_type: Optional[str]
    address: Optional[str]
    opening_hours: Optional[str]
    geometry: str  # Point
    updated_at: datetime = Field(default=datetime.now())
    updated_by: Optional[str] = None


class Building(BaseModel):
    osm_id: int
    metadata: dict
    geometry: str  # Polygon
