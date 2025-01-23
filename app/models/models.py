from math import radians
from typing import List, Optional, Tuple
from pydantic import BaseModel, ConfigDict, Field
from app.utils.constants import MIN_LAT, MIN_LON, MAX_LAT, MAX_LON


class DeliveryQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    venue_slug: str = Field(
        min_length=1,
    )
    cart_value: int = Field(ge=0)
    user_lat: float = Field(ge=MIN_LAT, le=MAX_LAT)
    user_lon: float = Field(ge=MIN_LON, le=MAX_LON)

    def to_gps_coordinates(self) -> "GPSCoordinates":
        return GPSCoordinates(longitude=self.user_lon, latitude=self.user_lat)


class DeliveryFeeInfo(BaseModel):
    fee: int = Field(..., description="Delivery fee in cents")
    distance: int = Field(..., description="Delivery distance in meters")


class DeliveryPriceResponse(BaseModel):
    total_price: int = Field(..., description="Total price including delivery fee")
    small_order_surcharge: int = Field(
        ..., description="Additional fee for small orders"
    )
    cart_value: int = Field(..., description="Original cart value")
    delivery: DeliveryFeeInfo
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_price": 1190,
                "small_order_surcharge": 0,
                "cart_value": 1000,
                "delivery": {"fee": 190, "distance": 177},
            }
        }
    )


class GPSCoordinates(BaseModel):
    longitude: float = Field()
    latitude: float = Field()

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


class DistanceRange(BaseModel):
    min: int = Field(..., ge=0, description="Minimum distance in meters")
    max: int = Field(
        ..., ge=0, description="Maximum distance in meters (0 = unavailable)"
    )
    a: int = Field(..., description="Base fee addition")
    b: int = Field(..., description="Distance multiplier")
    flag: Optional[str] = None


class DeliverySpecs(BaseModel):
    order_minimum_no_surcharge: int = Field(
        ..., description="Minimum cart value to avoid surcharge"
    )
    base_price: int = Field(..., description="Base price")
    distance_ranges: List[DistanceRange]

    @property
    def max_allowed_distance(self) -> int:
        return self.distance_ranges[-1].min


class VenueStatic(BaseModel):
    location: GPSCoordinates
    model_config = ConfigDict(extra="allow")


class VenueDynamic(BaseModel):
    delivery_specs: DeliverySpecs
    model_config = ConfigDict(extra="allow")
