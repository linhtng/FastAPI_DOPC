from pydantic import BaseModel, ConfigDict, Field, field_validator

# from decimal import Decimal
from typing import List, Optional, Tuple
from . import constants


class DeliveryQueryParams(BaseModel):
    model_config = {"extra": "forbid"}

    venue_slug: str
    cart_value: int = Field(ge=0)
    user_lat: float = Field(ge=constants.MIN_LAT, le=constants.MAX_LAT)
    user_lon: float = Field(ge=constants.MIN_LON, le=constants.MAX_LON)


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
    # delivery_distance_max: int = Field(ge=0, description="Maximum delivery distance")

    @field_validator("distance_ranges")
    def validate_distance_ranges(
        cls, ranges: List[DistanceRange]
    ) -> List[DistanceRange]:
        if not ranges:
            raise ValueError("Distance ranges cannot be empty")
        # Check first range starts at 0
        if ranges[0].min != 0:
            raise ValueError("First distance range must start at min=0")
        # Check last range ends with max=0
        if ranges[-1].max != 0:
            raise ValueError("Last distance range must end with max=0")
        # Check ranges are sorted and continuous
        for i in range(1, len(ranges)):
            prev_range = ranges[i - 1]
            curr_range = ranges[i]
            # Check sorting
            if curr_range.min <= prev_range.min:
                raise ValueError("Distance ranges must be sorted by min value")
            # Check continuity
            if curr_range.min != prev_range.max:
                raise ValueError(
                    f"Range gap found: range[{i-1}].max ({prev_range.max}) != "
                    f"range[{i}].min ({curr_range.min})"
                )

        return ranges


class VenueStatic(BaseModel):
    location: VenueCoordinates
    model_config = ConfigDict(extra="allow")


class VenueDynamic(BaseModel):
    delivery_specs: DeliverySpecs
    model_config = ConfigDict(extra="allow")
