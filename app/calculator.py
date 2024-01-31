from .models import DeliveryRequest
from datetime import datetime

class DeliveryCalculator:
    def __init__(self, request: DeliveryRequest):
         self.cart_value = request.cart_value
         self.delivery_distance = request.delivery_distance
         self.number_of_items = request.number_of_items
         self.time = request.time
         self.delivery_fee = 200
         self.free_ship_cart_value = 20000

    def small_order_surcharge(self):
        small_order_surcharge = 0
        min_cart_value = 1000
        if self.cart_value < min_cart_value:
            small_order_surcharge += min_cart_value - self.cart_value
        return small_order_surcharge

    def distance_based_fee(self):
        base_distance = 1000
        min_extra_fee = 100
        beyond_distance = self.delivery_distance - base_distance
        distance_based_surcharge = 0
        # Add the minimum extra fee for every 500 meters beyond the first kilometer
        while beyond_distance > 0:
            distance_based_surcharge += min_extra_fee
            beyond_distance -= 500
        return distance_based_surcharge

    def item_surcharge(self):
        item_surcharge = 0
        surcharge_free_items = 4
        extra_items = self.number_of_items - surcharge_free_items
        # Add surcharge 50 cents for every item beyond the fourth item and bulk fee 120 cents for more than 12 items
        if extra_items > 0:
            item_surcharge += extra_items * 50 + (120 if extra_items > 8 else 0)
        return item_surcharge

    def rush_hour_multiplier(self):
        request_time = datetime.strptime(self.time, "%Y-%m-%dT%H:%M:%SZ")
        rush_hour_multiplier = 1
        if request_time.weekday() == 4 and 15 <= request_time.hour <= 19:
            rush_hour_multiplier = 1.2
        return rush_hour_multiplier
    
    def cap_fee(self, delivery_fee: int):
        max_delivery_fee = 1500
        return min(delivery_fee, max_delivery_fee)
    
    def total_fee(self):
        if self.cart_value >= self.free_ship_cart_value:
            return 0
        self.delivery_fee += self.small_order_surcharge()
        self.delivery_fee += self.distance_based_fee()
        self.delivery_fee += self.item_surcharge()
        self.delivery_fee *= self.rush_hour_multiplier()
        self.delivery_fee = self.cap_fee(self.delivery_fee)
        return self.delivery_fee