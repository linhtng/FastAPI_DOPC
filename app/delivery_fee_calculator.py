from typing import List
from .dopc_distance import DistanceCalculator
from .models import (
    DeliveryQueryParams,
    VenueStatic,
    VenueDynamic,
    DeliveryPriceResponse,
    DistanceRange,
)
from .logging import logger


def calculate_distance_fee(
    distance: int, base_price: int, distance_ranges: List[DistanceRange]
) -> int:
    """Calculate delivery fee based on distance"""

    # Find applicable distance range
    applicable_range = None
    for range_spec in distance_ranges:
        if range_spec.max == 0:  # Last range
            if distance >= range_spec.min:
                applicable_range = range_spec
                break
        elif range_spec.min <= distance < range_spec.max:
            applicable_range = range_spec
            break

    if not applicable_range:
        raise ValueError(f"No applicable distance range found for distance {distance}m")

    logger.info(f"Applicable distance range: {applicable_range}")

    # Calculate fee components
    constant_fee = applicable_range.a
    distance_based_fee = round(applicable_range.b * distance / 10)
    total_distance_fee = base_price + constant_fee + distance_based_fee

    logger.info(
        f"Delivery fee calculation breakdown: "
        f"base_price={base_price} + "
        f"constant_fee={constant_fee} + "
        f"distance_based_fee={distance_based_fee} = "
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


async def DeliveryFeeCalculator(
    params: DeliveryQueryParams,
    static_data: VenueStatic,
    dynamic_data: VenueDynamic,
    distance: int,
) -> int:

    delivery_specs = dynamic_data.delivery_specs

    # Calculate delivery fee
    delivery_fee = calculate_distance_fee(
        distance=distance,
        base_price=delivery_specs.base_price,
        distance_ranges=delivery_specs.distance_ranges,
    )
    logger.info(f"Calculated delivery fee: {delivery_fee}")

    # Calculate small order surcharge
    small_order_surcharge = calculate_small_order_surcharge(
        cart_value=params.cart_value,
        minimum_no_surcharge=delivery_specs.order_minimum_no_surcharge,
    )

    # Calculate total price
    total_price = params.cart_value + delivery_fee + small_order_surcharge

    logger.info(
        f"Total price calculation: "
        f"cart_value={params.cart_value} + "
        f"delivery_fee={delivery_fee} + "
        f"surcharge={small_order_surcharge} = "
        f"total={total_price}"
    )

    return total_price
    # return DeliveryPriceResponse(
    #     total_price=params.cart_value + delivery_fee,
    #     small_order_surcharge=0,  # TODO: Implement
    #     cart_value=params.cart_value,
    #     delivery=DeliveryFeeInfo(fee=delivery_fee, distance=distance),
    # )
