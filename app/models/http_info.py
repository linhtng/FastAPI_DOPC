from .coordinates import GPSCoordinates
from pydantic import BaseModel, ConfigDict, Field
from app.utils.constants import MIN_LAT, MIN_LON, MAX_LAT, MAX_LON


class DeliveryQueryParams(BaseModel):
    """HTTP query parameters for delivery price calculation.
    
    Attributes:
        venue_slug (str): Unique venue identifier
        cart_value (int): Order value in cents
        user_lat (float): User latitude (-90 to +90)
        user_lon (float): User longitude (-180 to +180)
        
    Example:
        /api/v1/delivery-price?venue_slug=test-venue&cart_value=1000&user_lat=60.17&user_lon=24.93
    """

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
    """HTTP response model for delivery price calculation.
    
    Attributes:
        total_price (int): Final price including all fees
        small_order_surcharge (int): Extra fee for orders below minimum
        cart_value (int): Original order value
        delivery (DeliveryFeeInfo): Delivery details
    """
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
