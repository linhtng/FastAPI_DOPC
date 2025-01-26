from typing import List, Optional
from fastapi import HTTPException
from app.utils.logging import logger
from app.utils.constants import DISTANCE_FEE_DIVISOR
from app.models import (
    DeliveryFeeInfo,
    DeliveryPriceResponse,
    DistanceRange,
    DeliverySpecs,
)


def find_applicable_range(
    distance: int, distance_ranges: List[DistanceRange]
) -> Optional[DistanceRange]:
    """Find applicable distance range for given distance.
    Args:
        distance: Distance in meters
        distance_ranges: List of available distance ranges
    Returns:
        DistanceRange if found, None otherwise
    """
    for range_spec in distance_ranges:
        if range_spec.min <= distance < range_spec.max:
            return range_spec
    return None


def calculate_distance_fee(
    distance: int, base_price: int, distance_ranges: List[DistanceRange]
) -> int:
    """Calculate delivery fee by adding base price and distance-based
    components. Distance fee is calculated using ranges:
    - Fixed amount (a) per range
    - Variable amount (b) multiplied by distance
    Total = base_price + a + (b * distance)
    """
    applicable_range = find_applicable_range(distance, distance_ranges)
    if not applicable_range:
        raise ValueError(f"No applicable distance range found for distance {distance}m")
    constant_fee = applicable_range.a
    distance_based_fee = round(applicable_range.b * distance / DISTANCE_FEE_DIVISOR)
    total_distance_fee = base_price + constant_fee + distance_based_fee

    logger.info(
        f"Distance fee calculation: "
        f"distance={distance}, "
        f"base_price={base_price}, "
        f"constant_fee={constant_fee}, "
        f"distance_based_fee={distance_based_fee}, "
        f"total_distance_fee={total_distance_fee}"
    )

    return total_distance_fee


def calculate_small_order_surcharge(cart_value: int, minimum_no_surcharge: int) -> int:
    """Calculate surcharge for orders below minimum amount"""
    surcharge = max(0, minimum_no_surcharge - cart_value)
    logger.info(
        f"Small order surcharge calculation: "
        f"minimum={minimum_no_surcharge}, "
        f"cart_value={cart_value}, "
        f"surcharge={surcharge}"
    )
    return surcharge


async def total_fee_calculator(
    cart_value: int,
    delivery_specs: DeliverySpecs,
    distance: int,
) -> DeliveryPriceResponse:

    # Calculate delivery fee
    try:
        delivery_fee = calculate_distance_fee(
            distance=distance,
            base_price=delivery_specs.base_price,
            distance_ranges=delivery_specs.distance_ranges,
        )
    except ValueError as e:
        logger.error("Error calculating delivery fee: %s", str(e))
        raise HTTPException(
            status_code=400, detail=f"Failed to calculate delivery fee: {str(e)}"
        )

    # Calculate small order surcharge
    small_order_surcharge = calculate_small_order_surcharge(
        cart_value=cart_value,
        minimum_no_surcharge=delivery_specs.order_minimum_no_surcharge,
    )

    # Calculate total price
    total_price = cart_value + delivery_fee + small_order_surcharge

    logger.info(
        f"Total price calculation: "
        f"cart_value={cart_value} + "
        f"delivery_fee={delivery_fee} + "
        f"surcharge={small_order_surcharge} = "
        f"total={total_price}"
    )

    return DeliveryPriceResponse(
        total_price=total_price,
        small_order_surcharge=small_order_surcharge,
        cart_value=cart_value,
        delivery=DeliveryFeeInfo(fee=delivery_fee, distance=distance),
    )
