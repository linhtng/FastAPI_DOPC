from locust import HttpUser, task, between


class DeliveryPriceUser(HttpUser):
    host = "http://127.0.0.1:8000"
    wait_time = between(1, 2)

    @task
    def get_delivery_price(self):
        params = {
            "venue_slug": "home-assignment-venue-helsinki",
            "cart_value": 1000,
            "user_lat": 60.17094,
            "user_lon": 24.93087,
        }
        self.client.get("/api/v1/delivery-order-price", params=params)
