from typing import List

import overpy
import asyncio

from shapely.geometry.point import Point
from shapely.geometry.polygon import Polygon
from shapely.io import to_geojson

from src.pkg.models.models import Amenity, Building


class Client:
    def __init__(self, bounding_box):
        """
        Initialize the Overpass API Wrapper.

        :param bounding_box: A tuple representing the bounding box as (south, west, north, east).
        """
        self.api = overpy.Overpass()
        if isinstance(bounding_box, tuple) and len(bounding_box) == 4:
            # Convert tuple to string in Overpass API format
            self.bounding_box = f"{bounding_box[0]},{bounding_box[1]},{bounding_box[2]},{bounding_box[3]}"
        else:
            raise ValueError(
                "Bounding box must be a tuple with four coordinates: (south, west, north, east)."
            )

    async def extract_buildings(self) -> List[Building]:
        """
        Fetch all buildings and their metadata within the bounding box.

        :return: Overpy result object with building data.
        """
        query = f"""
        [out:json];
        way["building"]({self.bounding_box});
        (._;>;);
        out body;
        """
        response = self.api.query(query)

        buildings = []
        for way in response.ways:
            nodes = [
                (node.lon, node.lat) for node in way.nodes
            ]  # Ensure correct (lon, lat) order
            building = Building(
                overpass_id=way.id,
                metadata=way.tags,
                geometry_string=to_geojson(Polygon(nodes)),
            )
            buildings.append(building)
        return buildings

    async def extract_amenities(self) -> List[Amenity]:
        """
        Fetch all amenities (restaurants, cafés, banks, pharmacies, shops, and offices) within the bounding box.

        :return: Overpy result object with amenity data.
        """
        query = f"""
        [out:json];
        (
          node["amenity"~"restaurant|cafe|bank|pharmacy"]({self.bounding_box});
          node["shop"]({self.bounding_box});
          node["office"]({self.bounding_box});
        );
        out body;
        """
        response = self.api.query(query)

        amenities = []

        for node in response.nodes:
            tags = node.tags
            amenity = Amenity(
                overpass_id=node.id,
                name=tags.get("name"),
                amenity_type=tags.get("amenity"),
                address=tags.get("addr:street"),
                opening_hours=tags.get("opening_hours"),
                geometry_string=to_geojson(
                    Point(node.lat, node.lon),
                ),
            )
            amenities.append(amenity)

        return amenities


if __name__ == "__main__":
    # Define the bounding box for Malta as a tuple
    MALTA_BOUNDING_BOX = (34.9500, 14.1800, 36.0800, 14.6000)

    # Create an instance of the OverpassAPIWrapper
    overpass_api = Client(MALTA_BOUNDING_BOX)

    # Fetch and print amenities
    async def main():
        print("Fetching buildings...")
        try:
            buildings = await overpass_api.get_buildings()
            for building in buildings:
                print(building)
        except overpy.exception.OverpassBadRequest as e:
            print(f"Overpass API Error: {e}")

    asyncio.run(main())
