# Wolt Summer 2025 Engineering Internships
# Python Delivery Order Price Calculator (DOPC) API
Let's build the Delivery Order Price Calculator (DOPC) API using Python and [FastAPI](https://fastapi.tiangolo.com/) as the web framework.

### Specification
Implement an HTTP API (single GET endpoint) which calculates the delivery fee based on the information in the request query parameters. The response includes the calculated delivery fee in the response payload (JSON). In order to calculate the values needed for the response, DOPC should request data from Home Assignment API which is another imaginary backend service.

#### Request
Example: 
```
curl http://localhost:8000/api/v1/delivery-order-price?venue_slug=home-assignment-venue-helsinki&cart_value=1000&user_lat=60.17094&user_lon=24.93087
```
Query Parameters (**all are required**):
* `venue_slug` (string): The unique identifier (slug) for the venue from which the delivery order will be placed
* `cart_value`: (integer): The total value of the items in the shopping cart
* `user_lat` (number with decimal point): The latitude of the user's location
* `user_lon` (number with decimal point): The longitude of the user's location
  
#### Response
Example:
```json
{
  "total_price": 1190,
  "small_order_surcharge": 0,
  "cart_value": 1000,
  "delivery": {
    "fee": 190,
    "distance": 177
  }
}
```

## Development

### With Docker

#### Running the app
Run the app:
```
make
```

The API documentation is available in http://127.0.0.1:8000/docs. Here you can test all endpoints directly from your browser and try out requests with different parameters.
Alternatively, you can launch Postman and send request like the example above.

#### Tests
```
make pytest
```

#### Performance Test

Visit: 
```
http://localhost:8089/
```
Change number of users/ramp up if you wish, then start testing.

### Without Docker
**Prerequisites**
* Python 3.10 or later: [https://www.python.org/downloads/](https://www.python.org/downloads/)

#### Setting things up
Create a virtual environment:
```
python3 -m venv venv 
```

Activate the virtual environment:

* Linux / MacOS:
    ```
    source venv/bin/activate
    ```
Install the dependencies
```
pip install -r requirements.txt
```

#### Running the app

Run the server (`--reload` automatically restarts the server when there are changes in the code):
```
uvicorn app.main:app --reload
```

The API documentation is available in http://127.0.0.1:8000/docs.

#### Tests
```
pytest -v --capture=no --verbose
```

#### Performance Test 
```
sh run_load_test.sh
```
