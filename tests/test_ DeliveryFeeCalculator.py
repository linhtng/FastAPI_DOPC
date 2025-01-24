import pytest
from unittest.mock import AsyncMock
from fastapi import HTTPException

from app.services.delivery_fee_calculator import DeliveryFeeCalculator
from app.models.models import (
    DeliveryQueryParams,
    GPSCoordinates,
    VenueStatic,
    VenueDynamic,
    DeliverySpecs,
)


@pytest.fixture
def test_params():
    return DeliveryQueryParams(
        venue_slug="test-venue", cart_value=1000, user_lat=60.17094, user_lon=24.93087
    )


@pytest.fixture
def test_coords():
    return {
        "user": GPSCoordinates(latitude=60.17094, longitude=24.93087),
        "venue": GPSCoordinates(latitude=60.17094, longitude=24.93087),
    }


@pytest.fixture
def test_venue_data():
    return {
        "static": VenueStatic(
            location=GPSCoordinates(latitude=60.17094, longitude=24.93087)
        ),
        "dynamic": VenueDynamic(
            delivery_specs=DeliverySpecs(
                order_minimum_no_surcharge=1000,
                base_price=200,
                distance_ranges=[
                    {"min": 0, "max": 1000, "a": 0, "b": 0},
                    {"min": 1000, "max": 0, "a": 0, "b": 0},
                ],
            )
        ),
    }


@pytest.mark.asyncio
async def test_read_params(test_params):
    calculator = DeliveryFeeCalculator(test_params)
    params, user_location = await calculator.read_params()

    assert params == test_params
    assert isinstance(user_location, GPSCoordinates)
    assert user_location.latitude == test_params.user_lat
    assert user_location.longitude == test_params.user_lon


@pytest.mark.asyncio
async def test_fetch_venue_data(test_params, test_venue_data):
    calculator = DeliveryFeeCalculator(test_params)

    # Mock venue service
    calculator.venue_service.get_venue_static = AsyncMock(
        return_value=test_venue_data["static"]
    )
    calculator.venue_service.get_venue_dynamic = AsyncMock(
        return_value=test_venue_data["dynamic"]
    )

    static, dynamic = await calculator.fetch_venue_data(test_params.venue_slug)

    assert static == test_venue_data["static"]
    assert dynamic == test_venue_data["dynamic"]


@pytest.mark.asyncio
async def test_calculate_price(test_params, test_venue_data):
    calculator = DeliveryFeeCalculator(test_params)

    # Mock venue service and distance calculator
    calculator.venue_service.get_venue_static = AsyncMock(
        return_value=test_venue_data["static"]
    )
    calculator.venue_service.get_venue_dynamic = AsyncMock(
        return_value=test_venue_data["dynamic"]
    )

    result = await calculator.calculate_price()

    assert result.cart_value == test_params.cart_value
    assert isinstance(result.delivery.fee, int)
    assert isinstance(result.delivery.distance, int)
