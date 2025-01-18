import pytest
from app.delivery_fee_calculator import (
    calculate_distance_fee,
    calculate_small_order_surcharge,
    DeliveryFeeCalculator,
)
from app.models import DeliveryQueryParams, VenueStatic, VenueDynamic, DistanceRange


@pytest.fixture
def sample_distance_ranges():
    return [
        DistanceRange(min=0, max=500, a=0, b=0),
        DistanceRange(min=500, max=1000, a=100, b=1),
        DistanceRange(min=1000, max=0, a=0, b=0),
    ]


@pytest.mark.parametrize(
    "distance,base_price,expected_fee",
    [
        (400, 199, 199),  # First range, no extra fee
        (600, 199, 359),  # Second range, a=100, b=1
        (800, 199, 379),  # Second range, a=100, b=1
    ],
)
def test_calculate_distance_fee(
    sample_distance_ranges, distance, base_price, expected_fee
):
    """Test distance-based fee calculation"""
    result = calculate_distance_fee(
        distance=distance, base_price=base_price, distance_ranges=sample_distance_ranges
    )
    assert result == expected_fee


@pytest.mark.parametrize(
    "cart_value,minimum,expected_surcharge",
    [
        (800, 1000, 200),  # Below minimum
        (1000, 1000, 0),  # At minimum
        (1200, 1000, 0),  # Above minimum
    ],
)
def test_calculate_small_order_surcharge(cart_value, minimum, expected_surcharge):
    """Test small order surcharge calculation"""
    result = calculate_small_order_surcharge(cart_value, minimum)
    assert result == expected_surcharge


@pytest.mark.asyncio
async def test_delivery_fee_calculator():
    """Test complete fee calculation flow"""
    # Setup test data
    params = DeliveryQueryParams(
        venue_slug="test-venue", cart_value=800, user_lat=60.17, user_lon=24.93
    )

    static_data = VenueStatic(location={"coordinates": (24.93, 60.17)})

    dynamic_data = VenueDynamic(
        delivery_specs={
            "order_minimum_no_surcharge": 1000,
            "base_price": 199,
            "distance_ranges": [
                {"min": 0, "max": 500, "a": 0, "b": 0},
                {"min": 500, "max": 1000, "a": 100, "b": 1},
                {"min": 1000, "max": 0, "a": 0, "b": 0},
            ],
        }
    )

    distance = 600

    # Calculate
    result = await DeliveryFeeCalculator(params, static_data, dynamic_data, distance)

    # Assert
    assert result.total_price == 1359  # 800 + 359 + 200
    assert result.small_order_surcharge == 200
    assert result.cart_value == 800
    assert result.delivery.fee == 359
    assert result.delivery.distance == 600
