
from fastapi import FastAPI
from .models import DeliveryRequest, DeliveryResponse
from .calculator import DeliveryCalculator

app = FastAPI(title="Delivery Fee API")

@app.post("/calculate_delivery_fee", response_model=DeliveryResponse)
def calculate_delivery_fee(request: DeliveryRequest):
    """
    Calculate the delivery fee based on the request JSON
    """
    calculator = DeliveryCalculator(request)
    delivery_fee = calculator.total_fee()

    return DeliveryResponse(delivery_fee=delivery_fee)
