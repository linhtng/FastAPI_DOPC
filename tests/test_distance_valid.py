import pytest
from fastapi import HTTPException
from app.main import validate_delivery_distance
from app.models import DeliveryQueryParams, VenueStatic, VenueDynamic
from unittest.mock import patch


@pytest.fixture
def test_params():
    return DeliveryQueryParams(
        venue_slug="test-venue", cart_value=1000, user_lat=60.17094, user_lon=24.93087
    )


@pytest.fixture
def test_static_data():
    return VenueStatic(location={"coordinates": (24.93087, 60.17094)})


@pytest.fixture
def test_dynamic_data():
    return VenueDynamic(
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


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "user_coords,mock_distance,expected_status,check_msg",
    [
        ((24.93087, 60.17094), None, 400, False),  # Same coordinates
        ((24.93088, 60.17095), 0, 400, True),  # Zero distance
        ((25.00000, 61.00000), 1000, 400, False),  # Exceeds max
        ((25.00000, 161.00000), 9740280, 400, False),  # Exceeds max
        ((24.94000, 60.18000), 500, None, False),  # Valid case
    ],
    ids=[
        "same_coords",
        "zero_distance",
        "exceeds_max",
        "exceeds_max",
        "valid_distance",
    ],
)
async def test_validate_delivery_distance(
    test_params,
    test_static_data,
    test_dynamic_data,
    user_coords,
    mock_distance,
    expected_status,
    check_msg,
):
    test_params.user_lon, test_params.user_lat = user_coords

    with patch(
        "app.dopc_distance.DistanceCalculator.calculate_straight_line"
    ) as mock_calc:
        mock_calc.return_value = mock_distance if mock_distance is not None else 0

        if expected_status:
            with pytest.raises(HTTPException) as exc:
                await validate_delivery_distance(
                    test_params, test_static_data, test_dynamic_data
                )
            assert exc.value.status_code == expected_status
            if check_msg:
                assert "delivery distance" in exc.value.detail.lower()
        else:
            result = await validate_delivery_distance(
                test_params, test_static_data, test_dynamic_data
            )
            assert isinstance(result, int)
