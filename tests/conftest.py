import pytest
from app.models.models import DeliveryQueryParams, GPSCoordinates


@pytest.fixture
def valid_query_params():
    return {
        "venue_slug": "test-venue",
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087,
    }


@pytest.fixture
def test_params(valid_query_params):
    return DeliveryQueryParams(**valid_query_params)


@pytest.fixture
def test_coords(test_params):
    return {
        "venue": GPSCoordinates(longitude=24.93087, latitude=60.17094),
        "user": GPSCoordinates(
            longitude=test_params.user_lon, latitude=test_params.user_lat
        ),
    }
