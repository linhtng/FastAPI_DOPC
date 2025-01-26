from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from .models import DeliveryQueryParams
from .services.delivery_fee_calculator import DeliveryFeeCalculator
from .utils.logging import logger

app = FastAPI(title="Delivery Order Price Calculator (DOPC)")


@app.get("/api/v1/delivery-order-price")
async def handle_delivery_price(filter_query: Annotated[DeliveryQueryParams, Query()]):
    try:
        calculator = DeliveryFeeCalculator(filter_query)
        return await calculator.calculate_price()
    except HTTPException as e:
        logger.error(f"Error processing request: {e.detail}")
        raise
