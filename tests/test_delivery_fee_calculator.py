import pytest
from app.services.total_fee_calculator import (
    total_fee_calculator,
    calculate_distance_fee,
    calculate_small_order_surcharge,
)
from app.models.models import DeliverySpecs, DistanceRange


@pytest.fixture
def delivery_specs():
    return DeliverySpecs(
        order_minimum_no_surcharge=1000,
        base_price=199,
        distance_ranges=[
            DistanceRange(min=0, max=500, a=0, b=0),
            DistanceRange(min=500, max=1000, a=100, b=1),
            DistanceRange(min=1000, max=0, a=0, b=0),
        ],
    )


@pytest.mark.parametrize(
    "distance,base_price,expected_fee",
    [
        (400, 199, 199),  # First range, no extra fee
        (600, 199, 359),  # Second range, a=100, b=1
        (800, 199, 379),  # Second range, a=100, b=1
    ],
)
def test_calculate_distance_fee(delivery_specs, distance, base_price, expected_fee):
    result = calculate_distance_fee(
        distance=distance,
        base_price=base_price,
        distance_ranges=delivery_specs.distance_ranges,
    )
    assert result == expected_fee


@pytest.mark.parametrize(
    "cart_value,minimum_no_surcharge,expected_surcharge",
    [
        (1000, 1000, 0),  # Equal to minimum
        (1200, 1000, 0),  # Above minimum
        (800, 1000, 200),  # Below minimum
        (0, 1000, 1000),  # Zero cart value
        (500, 500, 0),  # Edge case - exact minimum
    ],
    ids=[
        "equal_minimum",
        "above_minimum",
        "below_minimum",
        "zero_cart",
        "edge_minimum",
    ],
)
def test_calculate_small_order_surcharge(
    cart_value: int, minimum_no_surcharge: int, expected_surcharge: int
):
    result = calculate_small_order_surcharge(cart_value, minimum_no_surcharge)
    assert result == expected_surcharge


@pytest.mark.asyncio
async def test_total_fee_calculator(delivery_specs):
    """Test complete fee calculation flow"""
    # Given
    cart_value = 800
    distance = 600

    # When
    result = await total_fee_calculator(
        cart_value=cart_value, delivery_specs=delivery_specs, distance=distance
    )

    # Then
    assert result.total_price == 1359  # 800 + 359 + 200
    assert result.small_order_surcharge == 200
    assert result.cart_value == 800
    assert result.delivery.fee == 359
    assert result.delivery.distance == 600
