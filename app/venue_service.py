from .http_client import HTTPClient
from .models import VenueStatic, VenueDynamic, VenueCoordinates, DeliverySpecs


class VenueService:
    BASE_URL = "https://consumer-api.development.dev.woltapi.com/home-assignment-api/v1/venues/"

    def __init__(self):
        self.client = HTTPClient(self.BASE_URL)

    async def get_venue_static(self, venue_slug: str) -> VenueStatic:
        data = await self.client.get(f"{venue_slug}/static")
        venue_data = data["venue_raw"]["location"]
        return VenueStatic(location=VenueCoordinates(**venue_data))

    async def get_venue_dynamic(self, venue_slug: str) -> VenueDynamic:
        data = await self.client.get(f"{venue_slug}/dynamic")
        venue_data = data["venue_raw"]
        return VenueDynamic(
            delivery_specs=DeliverySpecs(**venue_data["delivery_specs"])
        )
