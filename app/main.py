
from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

import json

# Open the JSON file
import os

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the relative path to the JSON file
json_file_path = os.path.join(current_dir, 'deliveryRequest.json')

# Open the JSON file
with open(json_file_path) as file:
    # Load the JSON data
    data = json.load(file)

# Access the values from the JSON data
cart_value = data['deliveryRequest'][0]['cart_value']
delivery_distance = data['deliveryRequest'][0]['delivery_distance']
number_of_items = data['deliveryRequest'][0]['number_of_items']
time = data['deliveryRequest'][0]['time']

# Now you can use these values in your code
""" cart_value: int
delivery_distance: int
number_of_items: int
time: datetime """

class DeliveryRequest(BaseModel):
    cart_value: int
    delivery_distance: int
    number_of_items: int
    time: str

class DeliveryResponse(BaseModel):
    delivery_fee: int

app = FastAPI(title="Delivery Fee API")

@app.post("/calculate_delivery_fee", response_model=DeliveryResponse)
def calculate_delivery_fee(request: DeliveryRequest):
    # Calculate small order surcharge
    if request.cart_value < 10:
        small_order_surcharge = 10 - request.cart_value
    else:
        small_order_surcharge = 0

    # Calculate base delivery fee for the first kilometer
    base_delivery_fee = 2

    # Calculate additional fee for every 500 meters beyond the first kilometer
    additional_distance = max(request.delivery_distance - 1000, 0)
    additional_fee = (additional_distance // 500) * 1

    # Calculate surcharge for number of items above the fifth item
    if request.number_of_items >= 5:
        item_surcharge = (request.number_of_items - 5) * 0.5
    else:
        item_surcharge = 0

    # Apply bulk fee for more than 12 items
    if request.number_of_items > 12:
        bulk_fee = 1.2
    else:
        bulk_fee = 1

    # Check if cart value qualifies for free delivery
    if request.cart_value >= 200:
        delivery_fee = 0
    else:
        # Calculate total delivery fee
        delivery_fee = base_delivery_fee + additional_fee + item_surcharge + small_order_surcharge
        delivery_fee *= bulk_fee

        # Apply rush hour multiplier during Friday rush (3 - 7 PM UTC)
        if request.time.weekday() == 4 and request.time.hour >= 15 and request.time.hour < 19:
            delivery_fee *= 1.2

        # Ensure delivery fee does not exceed the maximum of 15€
        delivery_fee = min(delivery_fee, 15)

    return {"delivery_fee": delivery_fee}
