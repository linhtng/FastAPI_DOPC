from fastapi import FastAPI, Query, HTTPException
from .models import DeliveryQueryParams
from .logging import logger
from .dopc_distance import DistanceCalculator
from .delivery_fee_calculator import DeliveryFeeCalculator

# from .calculator import DeliveryCalculator

from typing import Annotated
from .venue_service import VenueService, VenueStatic, VenueDynamic

app = FastAPI(title="Delivery Order Price Calculator (DOPC)")

venue_service = VenueService()


async def read_params(filter_query: DeliveryQueryParams) -> DeliveryQueryParams:
    logger.info(f"Received query parameters: {filter_query}")
    return filter_query


async def fetch_venue_data(venue_slug: str):
    try:
        static_data = await venue_service.get_venue_static(venue_slug)
        dynamic_data = await venue_service.get_venue_dynamic(venue_slug)
        # logger.info(f"Fetched venue data: static={static_data}, dynamic={dynamic_data}")
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


async def validate_delivery_distance(
    params: DeliveryQueryParams, static_data: VenueStatic, dynamic_data: VenueDynamic
) -> int:
    # Get coordinates
    venue_coords = static_data.location.coordinates
    user_coords = (params.user_lon, params.user_lat)

    # Calculate distance
    distance = DistanceCalculator.calculate_straight_line(venue_coords, user_coords)
    logger.info(f"Calculated delivery distance: {distance}m")

    # Get maximum allowed distance
    max_range = dynamic_data.delivery_specs.distance_ranges[-1].min

    if distance >= max_range:
        raise HTTPException(
            status_code=400,
            detail=f"Delivery distance {distance}m exceeds maximum allowed {max_range}m",
        )

    return distance


@app.get("/api/v1/delivery-order-price")
async def handle_delivery_price(filter_query: Annotated[DeliveryQueryParams, Query()]):
    try:
        params = await read_params(filter_query)
        static_data, dynamic_data = await fetch_venue_data(params.venue_slug)
        distance = await validate_delivery_distance(params, static_data, dynamic_data)

        result = await DeliveryFeeCalculator(
            params, static_data, dynamic_data, distance
        )
        # return result
    except HTTPException as e:
        logger.error(f"Error processing request: {e.detail}")
        raise e
