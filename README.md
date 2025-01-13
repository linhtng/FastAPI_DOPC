# Wolt Summer 2024 Engineering Internships
# Python Delivery Fee Calculator API
Let's build the Delivery Fee Calculator API using Python and [FastAPI](https://fastapi.tiangolo.com/) as the web framework.

### Specification
Implement an HTTP API (single POST endpoint) which calculates the delivery fee based on the information in the request payload (JSON) and includes the calculated delivery fee in the response payload (JSON).

#### Request
Example: 
```json
{"cart_value": 790, "delivery_distance": 2235, "number_of_items": 4, "time": "2024-01-15T13:00:00Z"}
```

##### Field details

| Field             | Type  | Description                                                               | Example value                             |
|:---               |:---   |:---                                                                       |:---                                       |
|cart_value         |Integer|Value of the shopping cart __in cents__.                                   |__790__ (790 cents = 7.90€)                |
|delivery_distance  |Integer|The distance between the store and customer’s location __in meters__.      |__2235__ (2235 meters = 2.235 km)          |
|number_of_items    |Integer|The __number of items__ in the customer's shopping cart.                   |__4__ (customer has 4 items in the cart)   |
|time               |String |Order time in UTC in [ISO format](https://en.wikipedia.org/wiki/ISO_8601). |__2024-01-15T13:00:00Z__                   |

#### Response
Example:
```json
{"delivery_fee": 710}
```

##### Field details

| Field         | Type  | Description                           | Example value             |
|:---           |:---   |:---                                   |:---                       |
|delivery_fee   |Integer|Calculated delivery fee __in cents__.  |__710__ (710 cents = 7.10€)|

## Development

### With Docker

#### Running the app
Run the app:
```
docker compose up
```

The API documentation is available in http://127.0.0.1:8000/docs.

#### Tests
```
docker compose run DOPC pytest
```

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
pytest
```
