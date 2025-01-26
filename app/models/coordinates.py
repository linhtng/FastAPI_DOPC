from math import radians
from typing import Tuple
from pydantic import BaseModel, Field
from app.utils.constants import MIN_LAT, MIN_LON, MAX_LAT, MAX_LON

class GPSCoordinates(BaseModel):
    longitude: float = Field(ge=MIN_LON, le=MAX_LON)
    latitude: float = Field(ge=MIN_LAT, le=MAX_LAT)

    @property
    def coordinates(self) -> Tuple[float, float]:
        return (self.longitude, self.latitude)

    @classmethod
    def from_coordinates(cls, coords: Tuple[float, float]) -> "GPSCoordinates":
        """Create from legacy (longitude, latitude) tuple"""
        lon, lat = coords
        return cls(longitude=lon, latitude=lat)

    def to_radians(self) -> tuple[float, float]:
        """Convert coordinates to radians"""
        return (radians(self.latitude), radians(self.longitude))


