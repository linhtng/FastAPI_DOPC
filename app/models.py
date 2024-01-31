from pydantic import BaseModel, Field

class DeliveryRequest(BaseModel):
    cart_value: int = Field(ge=1, description="The total value of the cart in cents")
    delivery_distance: int = Field(ge=1, description="The delivery distance in meters")
    number_of_items: int = Field(ge=1, description="The number of items in the cart")
    time: str = Field(description="The time of the delivery in ISO format")

class DeliveryResponse(BaseModel):
    delivery_fee: float