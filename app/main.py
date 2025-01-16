from fastapi import FastAPI, Query, HTTPException
from .models import DeliveryQueryParams
from .logging import logger

# from .calculator import DeliveryCalculator

from typing import Annotated
from .venue_service import VenueService

app = FastAPI(title="Delivery Order Price Calculator (DOPC)")

venue_service = VenueService()


async def read_params(filter_query: DeliveryQueryParams) -> DeliveryQueryParams:
    logger.info(f"Received query parameters: {filter_query}")
    return filter_query


async def fetch_venue_data(venue_slug: str):
    try:
        static_data = await venue_service.get_venue_static(venue_slug)
        dynamic_data = await venue_service.get_venue_dynamic(venue_slug)
        logger.info(f"Fetched venue data: static={static_data}, dynamic={dynamic_data}")
        return static_data, dynamic_data

    except HTTPException as e:
        logger.error(f"HTTP error fetching venue data: {e.detail}")
        raise HTTPException(
            status_code=e.status_code, detail=f"Error fetching venue data: {e.detail}"
        )
    except ValueError as e:
        logger.error(f"Invalid venue data: {str(e)}")
        raise HTTPException(
            status_code=422, detail=f"Invalid venue data format: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Internal server error while fetching venue data"
        )


async def calculate_price(params: DeliveryQueryParams, static_data, dynamic_data):
    # TODO: Implement calculation logic
    logger.info("Calculating delivery price")
    return {"price": 0}  # placeholder


@app.get("/api/v1/delivery-order-price")
async def handle_delivery_price(filter_query: Annotated[DeliveryQueryParams, Query()]):
    try:
        params = await read_params(filter_query)
        static_data, dynamic_data = await fetch_venue_data(params.venue_slug)
        # result = await calculate_price(params, static_data, dynamic_data)
        # return result
    except HTTPException as e:
        logger.error(f"Error processing request: {e}")
        raise e


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
