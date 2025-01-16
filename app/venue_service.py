from .http_client import HTTPClient
from .models import VenueStatic, VenueDynamic, VenueCoordinates, DeliverySpecs
from .logging import logger
from fastapi import HTTPException


class VenueService:
    BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/"

    def __init__(self):
        self.client = HTTPClient(self.BASE_URL)

    async def get_venue_static(self, venue_slug: str) -> VenueStatic:
        data = await self.client.get(f"{venue_slug}/static")
        # Extract coordinates from nested structure
        venue_raw = data["venue_raw"]
        location_data = venue_raw["location"]
        coordinates = location_data["coordinates"]
        # logger.debug(f"Extracted coordinates: {coordinates}")
        # Create VenueStatic instance with coordinates
        return VenueStatic(location=VenueCoordinates(coordinates=tuple(coordinates)))

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

        except ValueError as e:
            logger.error(f"Distance range validation error: {str(e)}")
            raise HTTPException(
                status_code=422,
                detail=f"Invalid distance ranges configuration: {str(e)}",
            )
