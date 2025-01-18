import pytest
from fastapi import HTTPException
from app.main import read_params, MAX_CART_VALUE
from app.models import DeliveryQueryParams


@pytest.mark.asyncio
async def test_read_params_valid():
    """
    Test read_params with valid input:
    - Valid venue slug
    - Positive cart value
    - Valid coordinates
    """
    # Arrange
    params = DeliveryQueryParams(
        venue_slug="test-venue", cart_value=1000, user_lat=60.17094, user_lon=24.93087
    )
    # Act
    result = await read_params(params)
    # Assert
    assert result == params


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "cart_value,expected_error,expected_msg",
    [
        (0, HTTPException, "Cart value cannot be zero"),
        (
            MAX_CART_VALUE + 1,
            HTTPException,
            f"Cart value cannot exceed {MAX_CART_VALUE} cents",
        ),
        (-100, ValueError, "Input should be greater than or equal to 0"),
        ("abc", ValueError, None),
    ],
    ids=["zero_cart", "exceeds_max", "negative_value", "invalid_type"],
)
async def test_cart_value_validation(cart_value, expected_error, expected_msg):
    """
    Test cart value validation:
    - Zero cart value -> HTTP 400
    - Exceeds max -> HTTP 400
    - Negative value -> ValueError
    - Invalid type -> ValueError
    """
    params_data = {
        "venue_slug": "test-venue",
        "cart_value": cart_value,
        "user_lat": 60.17094,
        "user_lon": 24.93087,
    }

    if expected_error is ValueError:
        with pytest.raises(ValueError) as exc:
            DeliveryQueryParams(**params_data)
        if expected_msg:
            assert expected_msg in str(exc.value)
    else:
        params = DeliveryQueryParams(**params_data)
        with pytest.raises(HTTPException) as exc:
            await read_params(params)
        assert exc.value.status_code == 400
        if expected_msg:
            assert exc.value.detail == expected_msg


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "lat,lon",
    [
        (91, 0),  # Invalid latitude
        (-91, 0),  # Invalid latitude
        (0, 181),  # Invalid longitude
        (0, -181),  # Invalid longitude
    ],
)
async def test_read_params_invalid_coordinates(lat, lon):
    with pytest.raises(ValueError):
        DeliveryQueryParams(
            venue_slug="test-venue", cart_value=1000, user_lat=lat, user_lon=lon
        )


@pytest.mark.asyncio
async def test_read_params_empty_venue():
    with pytest.raises(ValueError):
        DeliveryQueryParams(
            venue_slug="", cart_value=1000, user_lat=60.17094, user_lon=24.93087
        )
