from fastapi import FastAPI
from .models import DeliveryRequest, DeliveryResponse
from .calculator import DeliveryCalculator
from typing import Annotated, Literal

app = FastAPI(title="Delivery Order Price Calculator (DOPC)")


# @app.get("/")
# def index():
#     return {"Hello": "Welcome to the Delivery Order Price Calculator (DOPC)!"}


# @app.post("/DOPC", response_model=DeliveryResponse)
# def DOPC(request: DeliveryRequest):
#     """
#     Calculate the delivery fee based on the request JSON
#     """
#     calculator = DeliveryCalculator(request)
#     delivery_fee = calculator.total_fee()

#     return DeliveryResponse(delivery_fee=delivery_fee)
