from fastapi import HTTPException

from app.models.models import (
    DeliveryPriceResponse,
    DeliveryQueryParams,
    VenueDynamic,
    VenueStatic,
)
from .distance_calculator import DistanceCalculator
from .total_fee_calculator import total_fee_calculator
from .venue_service import VenueService
from app.utils.logging import logger


class DeliveryFeeCalculator:
    def __init__(self, filter_query: DeliveryQueryParams):
        self.filter_query = filter_query
        self.venue_service = VenueService()

    async def read_params(self) -> DeliveryQueryParams:
        return self.filter_query

    async def fetch_venue_data(self, venue_slug: str):
        try:
            static_data = await self.venue_service.get_venue_static(venue_slug)
            dynamic_data = await self.venue_service.get_venue_dynamic(venue_slug)
            logger.info(
                f"Fetched venue data: static={static_data}, dynamic={dynamic_data}"
            )
            return static_data, dynamic_data

        except HTTPException as e:
            logger.error("HTTP error fetching venue data: %s", e.detail)
            raise

    async def validate_delivery_distance(
        self,
        params: DeliveryQueryParams,
        static_data: VenueStatic,
        dynamic_data: VenueDynamic,
    ) -> int:
        # Get coordinates
        venue_coords = static_data.location.coordinates
        user_coords = (params.user_lon, params.user_lat)

        if venue_coords == user_coords:
            raise HTTPException(
                status_code=400, detail="User and venue location are the same"
            )

        # Calculate distance
        distance = DistanceCalculator.calculate_straight_line(venue_coords, user_coords)
        logger.info(f"Calculated delivery distance: {distance}m")
        if distance == 0:
            raise HTTPException(
                status_code=400,
                detail="Zero delivery distance. User and venue location are the same",
            )

        # Get maximum allowed distance
        max_range = dynamic_data.delivery_specs.distance_ranges[-1].min

        if distance >= max_range:
            raise HTTPException(
                status_code=400,
                detail=f"Delivery distance {distance}m is too long. Delivery not available",
            )

        return distance

    async def calculate_price(self) -> DeliveryPriceResponse:
        try:
            params = await self.read_params()
            static_data, dynamic_data = await self.fetch_venue_data(params.venue_slug)
            distance = await self.validate_delivery_distance(
                params, static_data, dynamic_data
            )
            result = await total_fee_calculator(params, dynamic_data, distance)
            return result
        except HTTPException as e:
            logger.error("Error calculating price: %s", e.detail)
            raise
