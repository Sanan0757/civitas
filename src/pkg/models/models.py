from typing import Optional, List

from pydantic import BaseModel, Json


class Amenity(BaseModel):
    overpass_id: int
    name: Optional[str]
    amenity_type: Optional[str]
    address: Optional[str]
    opening_hours: Optional[str]
    geometry_string: str  # Point


class Building(BaseModel):
    overpass_id: int
    metadata: dict
    geometry_string: str  # Polygon
