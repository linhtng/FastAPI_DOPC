from fastapi import HTTPException
from app.utils.logging import logger
from app.utils.constants import VENUE_ENDPOINT
from app.utils.http_client import HTTPClient
from app.models import DeliverySpecs, GPSCoordinates, VenueDynamic, VenueStatic


class VenueService:
    """Service for fetching venue data from external API.

    Per API contract:
    - If response status is 200, all required fields are guaranteed in payload
    - Only HTTP errors need handling, re-raised with original status codes
    - Static endpoint returns venue location
    - Dynamic endpoint returns delivery specifications
    """

    BASE_URL = VENUE_ENDPOINT

    def __init__(self):
        try:
            self.client = HTTPClient(self.BASE_URL)
        except Exception as e:
            logger.error(f"Failed to initialize HTTP client: {str(e)}")
            raise HTTPException(
                status_code=503, detail=f"Venue service is not available: {str(e)}"
            )

    async def get_venue_static(self, venue_slug: str) -> VenueStatic:
        try:
            data = await self.client.get(f"{venue_slug}/static")
            venue_raw = data["venue_raw"]
            location_data = venue_raw["location"]
            coordinates = location_data["coordinates"]  # Returns tuple (lon, lat)

            # Convert tuple to GPSCoordinates
            location = GPSCoordinates.from_coordinates(tuple(coordinates))
            return VenueStatic(location=location)
        except HTTPException as e:
            logger.error(f"HTTP error fetching venue data: {str(e)}")
            raise e

    async def get_venue_dynamic(self, venue_slug: str) -> VenueDynamic:
        try:
            data = await self.client.get(f"{venue_slug}/dynamic")
            venue_data = data["venue_raw"]
            delivery_specs_data = venue_data["delivery_specs"]
            delivery_pricing = delivery_specs_data["delivery_pricing"]

            delivery_specs = DeliverySpecs(
                order_minimum_no_surcharge=delivery_specs_data[
                    "order_minimum_no_surcharge"
                ],
                base_price=delivery_pricing["base_price"],
                distance_ranges=delivery_pricing["distance_ranges"],
            )

            logger.debug(f"Constructed delivery specs: {delivery_specs}")
            return VenueDynamic(delivery_specs=delivery_specs)

        except HTTPException as e:
            logger.error(f"HTTP error fetching venue data: {str(e)}")
            raise e
