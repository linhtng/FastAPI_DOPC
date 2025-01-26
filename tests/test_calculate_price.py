from fastapi import HTTPException
import pytest
from unittest.mock import AsyncMock
from app.services.delivery_fee_calculator import DeliveryFeeCalculator
from app.models import (
    DeliveryPriceResponse,
    DeliveryFeeInfo,
)



@pytest.mark.asyncio
async def test_calculate_price_first_range(test_params, test_venue_data):
    calculator = DeliveryFeeCalculator(test_params)

    # Mock venue service and distance calculator
    calculator.venue_service.get_venue_static = AsyncMock(
        return_value=test_venue_data["static"]
    )
    calculator.venue_service.get_venue_dynamic = AsyncMock(
        return_value=test_venue_data["dynamic"]
    )

    expected = DeliveryPriceResponse(
        cart_value=1000,
        delivery=DeliveryFeeInfo(
            fee=190,
            distance=176
        ),
        small_order_surcharge=0,
        total_price=1190
    )

    result = await calculator.calculate_price()

    assert result == expected

@pytest.mark.asyncio
async def test_calculate_price_second_range(test_params, test_venue_data):
    test_params.user_lon = 24.93704 # 500m from venue
    calculator = DeliveryFeeCalculator(test_params)

    # Mock venue service and distance calculator
    calculator.venue_service.get_venue_static = AsyncMock(
        return_value=test_venue_data["static"]
    )
    calculator.venue_service.get_venue_dynamic = AsyncMock(
        return_value=test_venue_data["dynamic"]
    )

    expected = DeliveryPriceResponse(
        cart_value=1000,
        delivery=DeliveryFeeInfo(
            fee=290,
            distance=500
        ),
        small_order_surcharge=0,
        total_price=1290
    )

    result = await calculator.calculate_price()

    assert result == expected

@pytest.mark.asyncio
async def test_calculate_price_range_exceed(test_params, test_venue_data):
    test_params.user_lon = 24.94615 # 1000m from venue
    calculator = DeliveryFeeCalculator(test_params)

    # Mock venue service and distance calculator
    calculator.venue_service.get_venue_static = AsyncMock(
        return_value=test_venue_data["static"]
    )
    calculator.venue_service.get_venue_dynamic = AsyncMock(
        return_value=test_venue_data["dynamic"]
    )

    # Act & Assert
    with pytest.raises(HTTPException) as exc_info:
        await calculator.calculate_price()
    
    assert exc_info.value.status_code == 400