from pydantic import BaseModel

class DeliveryRequest(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str

class DeliveryResponse(BaseModel):
    delivery_fee: float