from unittest.mock import patch

import pytest
from fastapi import HTTPException

from app.models.models import DeliveryQueryParams, GPSCoordinates
from app.services.delivery_fee_calculator import DeliveryFeeCalculator
from app.utils.constants import (
    EXPECTED_CART_VALUE,
    EXPECTED_USER_LATITUDE,
    EXPECTED_USER_LONGITUDE,
    EXPECTED_VENUE_SLUG,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_coords,mock_distance,expected_status,check_msg",
    [
        ((EXPECTED_USER_LONGITUDE, EXPECTED_USER_LATITUDE), 176, None, False),  # Valid
        ((25.00000, 61.00000), 1000, 400, False),  # Exceeds max
        ((26.00000, 61.00000), 109275, 400, False),  # Exceeds max
        ((24.94000, 60.18000), 999, None, False),  # Valid distance
    ],
    ids=[
        "valid_distance",
        "exceeds_max",
        "exceeds_max",
        "valid_distance",
    ],
)
async def test_validate_delivery_distance(
    test_coords, user_coords, mock_distance, expected_status, check_msg
):
    calculator = DeliveryFeeCalculator(
        DeliveryQueryParams(
            venue_slug=EXPECTED_VENUE_SLUG,
            cart_value=EXPECTED_CART_VALUE,
            user_lat=user_coords[1],
            user_lon=user_coords[0],
        )
    )

    user_location = GPSCoordinates(longitude=user_coords[0], latitude=user_coords[1])

    with patch(
        "app.services.distance_calculator.DistanceCalculator.calculate_straight_line"
    ) as mock_calc:
        mock_calc.return_value = mock_distance if mock_distance is not None else 0

        if expected_status:
            with pytest.raises(HTTPException) as exc:
                await calculator.valid_delivery_distance(
                    user_location=user_location,
                    venue_location=test_coords["venue"],
                    max_allowed_distance=1000,
                )
            assert exc.value.status_code == expected_status
            if check_msg:
                assert "delivery distance" in exc.value.detail.lower()
        else:
            result = await calculator.valid_delivery_distance(
                user_location=user_location,
                venue_location=test_coords["venue"],
                max_allowed_distance=1000,
            )
            assert isinstance(result, int)
