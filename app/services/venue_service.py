from fastapi import HTTPException
from app.utils.logging import logger
from app.utils.constants import VENUE_ENDPOINT
from app.utils.http_client import HTTPClient
from app.models.models import DeliverySpecs, VenueCoordinates, VenueDynamic, VenueStatic


class VenueService:
    BASE_URL = VENUE_ENDPOINT

    def __init__(self):
        try:
            self.client = HTTPClient(self.BASE_URL)
        except Exception as e:
            logger.error(f"Failed to initialize HTTP client: {str(e)}")
            raise HTTPException(
                status_code=502, detail=f"Invalid response from venue service: {str(e)}"
            )

    async def get_venue_static(self, venue_slug: str) -> VenueStatic:
        try:
            data = await self.client.get(f"{venue_slug}/static")
            venue_raw = data["venue_raw"]
            location_data = venue_raw["location"]
            coordinates = location_data["coordinates"]
            return VenueStatic(
                location=VenueCoordinates(coordinates=tuple(coordinates))
            )
        except HTTPException as e:
            # Re-raise HTTP exceptions with same status
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
            # Re-raise HTTP exceptions with same status
            raise e
