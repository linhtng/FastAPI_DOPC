import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def valid_query_params():
    return {
        "venue_slug": "test-venue",
        "cart_value": 1000,
        "user_lat": 60.17094,
        "user_lon": 24.93087,
    }
