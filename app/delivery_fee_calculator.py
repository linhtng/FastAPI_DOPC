from .dopc_distance import DistanceCalculator
from .models import DeliveryQueryParams, VenueStatic, VenueDynamic


async def DeliveryFeeCalculator(
    params: DeliveryQueryParams, static_data: VenueStatic, dynamic_data: VenueDynamic
):
    # Initialize calculator
    distance_calculator = DistanceCalculator()

    # Get coordinates
    user_coordinates = (params.user_lon, params.user_lat)  # longitude first
    venue_coordinates = static_data.location.coordinates

    # Calculate distance
    distance = distance_calculator.calculate_straight_line(
        venue_coordinates, user_coordinates
    )

    logger.info(f"Calculated delivery distance: {distance}m")

    # TODO: Use distance to calculate delivery fee
    return {"price": 0}
