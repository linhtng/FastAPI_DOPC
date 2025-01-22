from math import asin, cos, radians, sin, sqrt
from typing import Tuple

from app.utils.logging import logger
from app.utils.constants import EARTH_RADIUS


class DistanceCalculator:
    @staticmethod
    def _calculate_haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
        """Calculate Haversine formula components.
        Args:
            lat1, lon1: First point coordinates in radians
            lat2, lon2: Second point coordinates in radians
        Returns:
            float: Haversine formula result
        """
        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        distance = int(c * EARTH_RADIUS)
        return distance

    @staticmethod
    def calculate_straight_line(
        venue_coords: Tuple[float, float], user_coords: Tuple[float, float]
    ) -> int:
        """Calculate straight line distance between two coordinates.
        Args:
            venue_coords: Tuple of (longitude, latitude)
            user_coords: Tuple of (longitude, latitude)
        Returns:
            int: Distance in meters
        """
        # Extract and convert coordinates
        venue_lon, venue_lat = venue_coords
        user_lon, user_lat = user_coords

        # Convert to radians and calculate
        lat1, lon1 = radians(venue_lat), radians(venue_lon)
        lat2, lon2 = radians(user_lat), radians(user_lon)

        distance = DistanceCalculator._calculate_haversine(lat1, lon1, lat2, lon2)

        logger.debug("Calculated distance: %dm", distance)
        return distance
