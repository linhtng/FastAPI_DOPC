from .coordinates import GPSCoordinates
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
