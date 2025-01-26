import pytest
from app.models.models import DeliveryQueryParams, GPSCoordinates
from app.utils.constants import (
    EXPECTED_CART_VALUE,
    EXPECTED_USER_LATITUDE,
    EXPECTED_USER_LONGITUDE,
    EXPECTED_VENUE_SLUG,
)


@pytest.fixture
def valid_query_params():
    """Provides valid query parameters for delivery price calculation.
    Returns:
        dict: Valid query parameters with required fields:
            - venue_slug: Test venue identifier
            - cart_value: Cart value in cents (1000 = 10.00€)
            - user_lat: User's latitude
            - user_lon: User's longitude  
    Usage:
        def test_something(valid_query_params):
            response = client.get("/api/v1/delivery-order-price", params=valid_query_params)
    """
    return {
        "venue_slug": EXPECTED_VENUE_SLUG,
        "cart_value": EXPECTED_CART_VALUE,
        "user_lat": EXPECTED_USER_LATITUDE,
        "user_lon": EXPECTED_USER_LONGITUDE,
    }


@pytest.fixture
def test_params(valid_query_params):
    """Converts dictionary query params to DeliveryQueryParams model.
    Usage:
        def test_model(test_params):
            assert test_params.cart_value == 1000
    """
    return DeliveryQueryParams(**valid_query_params)


@pytest.fixture
def test_coords(test_params):
    """Creates GPS coordinates for both venue and user locations.
    Returns:
        dict: Contains two GPSCoordinates objects:
            - venue: Fixed venue location
            - user: User location from test_params
    Usage:
        def test_distance(test_coords):
            distance = calculate_distance(test_coords['venue'], test_coords['user'])
    """
    return {
        "venue": GPSCoordinates(longitude=EXPECTED_USER_LONGITUDE, latitude=EXPECTED_USER_LATITUDE),
        "user": GPSCoordinates(
            longitude=test_params.user_lon, latitude=test_params.user_lat
        ),
    }
