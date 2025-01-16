from pydantic import BaseModel, ConfigDict, Field

# from decimal import Decimal
from typing import List, Optional, Tuple


class DeliveryQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    venue_slug: str
    cart_value: int = Field(ge=0)
    user_lat: float = Field(gt=-90, le=90)
    user_lon: float = Field(gt=-180, le=180)


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


class VenueCoordinates(BaseModel):
    coordinates: Tuple[float, float] = Field(
        ..., description="Venue coordinates [longitude, latitude]"
    )


class DistanceRange(BaseModel):
    min: int = Field(..., description="Minimum distance in meters")
    max: int = Field(..., description="Maximum distance in meters (0 = unavailable)")
    a: int = Field(..., description="Base fee addition")
    b: int = Field(..., description="Distance multiplier")
    flag: Optional[str] = None


class DeliverySpecs(BaseModel):
    order_minimum_no_surcharge: int = Field(
        ..., description="Minimum cart value to avoid surcharge"
    )
    base_price: int = Field(..., description="Base price")
    distance_ranges: List[DistanceRange]


class VenueStatic(BaseModel):
    location: VenueCoordinates
    model_config = ConfigDict(extra="allow")


class VenueDynamic(BaseModel):
    delivery_specs: DeliverySpecs
    model_config = ConfigDict(extra="allow")
