from app.utils.constants import (
    EXPECTED_CART_VALUE,
    EXPECTED_USER_LATITUDE,
    EXPECTED_USER_LONGITUDE,
    EXPECTED_VENUE_SLUG,
)
from locust import HttpUser, task, between


class DeliveryPriceUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 2)

    @task
    def get_delivery_price(self):
        params = {
            "venue_slug": EXPECTED_VENUE_SLUG,
            "cart_value": EXPECTED_CART_VALUE,
            "user_lat": EXPECTED_USER_LATITUDE,
            "user_lon": EXPECTED_USER_LONGITUDE,
        }
        self.client.get("/api/v1/delivery-order-price", params=params)
