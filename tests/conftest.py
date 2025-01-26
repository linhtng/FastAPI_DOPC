import pytest
from app.models import (
    DeliveryQueryParams, GPSCoordinates, DeliverySpecs, DistanceRange,
    VenueStatic, VenueDynamic
)
from app.utils.constants import (
    EXPECTED_CART_VALUE,
    EXPECTED_USER_LATITUDE,
    EXPECTED_USER_LONGITUDE,
    EXPECTED_VENUE_SLUG,
    EXPECTED_VENUE_LATITUDE,
    EXPECTED_VENUE_LONGITUDE,
    EXPECTED_MIN_ORDER_NO_SURCHARGE,
    EXPECTED_BASE_PRICE
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


@pytest.fixture
def test_delivery_specs():
    """Provides test delivery specifications with predefined ranges and fees.
    Returns:
        DeliverySpecs: Configured with:
            - Minimum order value: 1000 cents (10€)
            - Base delivery price: 200 cents (2€)
            - Distance ranges:
                - 0-500m: No additional fee
                - 500-1000m: 100 cents + 0€/m
                - >1000m: No additional fee
    Usage:
        def test_something(test_delivery_specs):
            assert test_delivery_specs.base_price == 200
    """
    return DeliverySpecs(
        order_minimum_no_surcharge=EXPECTED_MIN_ORDER_NO_SURCHARGE,
        base_price=EXPECTED_BASE_PRICE,
        distance_ranges=[
            {
                "min": 0,
                "max": 500,
                "a": 0,
                "b": 0
            },
            {
                "min": 500,
                "max": 1000,
                "a": 100,
                "b": 0
            },
            {
                "min": 1000,
                "max": 0,
                "a": 0,
                "b": 0
            }
        ]
    )


@pytest.fixture
def test_venue_data(test_delivery_specs):
    """Provides mock venue data for testing.
    Returns:
        dict: Contains:
            - static: VenueStatic with venue location
            - dynamic: VenueDynamic with delivery specs
    Usage:
        def test_something(test_venue_data):
            venue_location = test_venue_data['static'].location
            delivery_specs = test_venue_data['dynamic'].delivery_specs
    """
    return {
        "static": VenueStatic(
            location=GPSCoordinates(latitude=EXPECTED_VENUE_LATITUDE, longitude=EXPECTED_VENUE_LONGITUDE)
        ),
        "dynamic": VenueDynamic(
            delivery_specs=test_delivery_specs
        ),
    }