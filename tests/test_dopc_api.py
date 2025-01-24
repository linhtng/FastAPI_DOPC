from unittest.mock import AsyncMock, patch
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException

from app.main import app
from app.models.models import DeliveryPriceResponse

client = TestClient(app)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "query_params,expected_status,expected_response",
    [
        # Valid request
        (
            {
                "venue_slug": "home-assignment-venue-helsinki",
                "cart_value": 1000,
                "user_lat": 60.17094,
                "user_lon": 24.93087,
            },
            200,
            {
                "total_price": 1190,
                "small_order_surcharge": 0,
                "cart_value": 1000,
                "delivery": {"fee": 190, "distance": 177},
            },
        ),
        # Venue not found
        (
            {
                "venue_slug": "home-assignment-venue-helsingi",
                "cart_value": 1000,
                "user_lat": 60.17094,
                "user_lon": 24.93087,
            },
            404,
            {
                "total_price": 1190,
                "small_order_surcharge": 0,
                "cart_value": 1000,
                "delivery": {"fee": 190, "distance": 177},
            },
        ),
        # Invalid coordinates
        (
            {
                "venue_slug": "test-venue",
                "cart_value": 1000,
                "user_lat": 91,
                "user_lon": 181,
            },
            422,
            {"detail": "Invalid coordinates"},
        ),
        # Missing parameters
        ({}, 422, {"detail": "Missing required parameters"}),
    ],
)
async def test_delivery_price_endpoint(
    query_params, expected_status, expected_response
):
    with patch(
        "app.services.delivery_fee_calculator.DeliveryFeeCalculator"
    ) as MockCalculator:
        instance = MockCalculator.return_value
        if expected_status == 200:
            instance.calculate_price = AsyncMock(
                return_value=DeliveryPriceResponse(**expected_response)
            )
        else:
            instance.calculate_price = AsyncMock(
                side_effect=HTTPException(status_code=expected_status)
            )

        response = client.get("/api/v1/delivery-order-price", params=query_params)
        assert response.status_code == expected_status
