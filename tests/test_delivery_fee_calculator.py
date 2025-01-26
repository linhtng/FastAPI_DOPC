import pytest
from app.services.total_fee_calculator import (
    total_fee_calculator,
    calculate_distance_fee,
    calculate_small_order_surcharge,
)
from app.models.models import DeliveryPriceResponse, DeliveryFeeInfo
from app.services.total_fee_calculator import total_fee_calculator



@pytest.mark.parametrize(
    "distance,expected_fee",
    [
        (400, 190),  # First range, no extra fee
        (600, 290),  # Second range, a=100, b=0
        (800, 290),  # Second range, a=100, b=0
    ],
)
def test_calculate_distance_fee(test_delivery_specs, distance, expected_fee):
    result = calculate_distance_fee(
        distance=distance,
        base_price=test_delivery_specs.base_price,
        distance_ranges=test_delivery_specs.distance_ranges,
    )
    assert result == expected_fee


@pytest.mark.parametrize(
    "cart_value,minimum_no_surcharge,expected_surcharge",
    [
        (1000, 1000, 0),  # Equal to minimum
        (1200, 1000, 0),  # Above minimum
        (800, 1000, 200),  # Below minimum
        (0, 1000, 1000),  # Zero cart value
    ],
    ids=[
        "equal_minimum",
        "above_minimum",
        "below_minimum",
        "zero_cart",
    ],
)
def test_calculate_small_order_surcharge(
    cart_value: int, minimum_no_surcharge: int, expected_surcharge: int
):
    result = calculate_small_order_surcharge(cart_value, minimum_no_surcharge)
    assert result == expected_surcharge


@pytest.mark.asyncio
async def test_total_fee_calculator(test_delivery_specs):
    """Test complete fee calculation flow"""
    cart_value = 800
    distance = 600

    expected = DeliveryPriceResponse(
        cart_value=cart_value,
        delivery=DeliveryFeeInfo(
            fee=290,
            distance=distance
        ),
        small_order_surcharge=200,
        total_price=1290
    )

    result = await total_fee_calculator(
        cart_value=cart_value, delivery_specs=test_delivery_specs, distance=distance
    )

    assert result == expected
