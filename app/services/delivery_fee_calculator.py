from fastapi import HTTPException

from app.models.models import (
    DeliveryPriceResponse,
    DeliveryQueryParams,
    GPSCoordinates,
)
from .distance_calculator import DistanceCalculator
from .total_fee_calculator import total_fee_calculator
from .venue_service import VenueService
from app.utils.logging import logger


class DeliveryFeeCalculator:
    def __init__(self, filter_query: DeliveryQueryParams):
        self.filter_query = filter_query
        self.venue_service = VenueService()

    async def read_params(self) -> tuple[DeliveryQueryParams, GPSCoordinates]:
        user_location = self.filter_query.to_gps_coordinates()
        return self.filter_query, user_location

    async def fetch_venue_data(self, venue_slug: str):
        try:
            static_data = await self.venue_service.get_venue_static(venue_slug)
            dynamic_data = await self.venue_service.get_venue_dynamic(venue_slug)
            logger.info(
                f"Fetched venue data: static={static_data}, dynamic={dynamic_data}"
            )
            return static_data, dynamic_data

        except HTTPException as e:
            logger.error(f"HTTP error fetching venue data: {str(e)}")
            raise

    async def valid_delivery_distance(
        self,
        user_location: GPSCoordinates,
        venue_location: GPSCoordinates,
        max_allowed_distance: int,
    ) -> int:

        if user_location == venue_location:
            logger.info("User at venue location, distance: 0m")
            return 0

        distance = DistanceCalculator.calculate_straight_line(
            venue_location, user_location
        )
        logger.info(f"Calculated delivery distance: {distance}m")

        if distance >= max_allowed_distance:
            raise HTTPException(
                status_code=400,
                detail=f"Delivery distance {distance}m is too long. Delivery not available",
            )

        return distance

    async def calculate_price(self) -> DeliveryPriceResponse:
        try:
            params, user_location = await self.read_params()
            static_data, dynamic_data = await self.fetch_venue_data(params.venue_slug)
            distance = await self.valid_delivery_distance(
                user_location,
                static_data.location,
                dynamic_data.delivery_specs.max_allowed_distance,
            )
            result = await total_fee_calculator(
                params.cart_value, dynamic_data.delivery_specs, distance
            )
            return result
        except HTTPException as e:
            logger.error(f"Error calculating delivery price: {str(e)}")
            raise
