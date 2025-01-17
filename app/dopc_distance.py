from math import radians, cos, sin, asin, sqrt
from typing import Tuple
from .logging import logger
from . import constants


class DistanceCalculator:

    @staticmethod
    def calculate_straight_line(
        venue_coords: Tuple[float, float], user_coords: Tuple[float, float]
    ) -> int:
        # Extract coordinates (longitude, latitude)
        venue_lon, venue_lat = venue_coords
        user_lon, user_lat = user_coords
        logger.debug(
            f"Venue coordinates: {venue_coords}, User coordinates: {user_coords}"
        )

        # Convert to radians
        lat1, lon1 = radians(venue_lat), radians(venue_lon)
        lat2, lon2 = radians(user_lat), radians(user_lon)

        # Haversine formula
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))

        # Calculate distance in meters
        distance = int(c * constants.EARTH_RADIUS)
        logger.debug(f"Calculated distance: {distance}m")
        return distance
