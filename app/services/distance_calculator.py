from math import asin, cos, sin, sqrt
from app.models.models import GPSCoordinates
from app.utils.constants import EARTH_RADIUS


class DistanceCalculator:
    @staticmethod
    def _calculate_haversine(
        location_a: GPSCoordinates, location_b: GPSCoordinates
    ) -> int:
        """Haversine formula calculates the great-circle distance between
        two points on a sphere (Earth). Formula: d = 2R * arcsin(sqrt(h)),
        where:
        - h = sin²(Δφ/2) + cos(φ₁)cos(φ₂)sin²(Δλ/2)
        - R is Earth's radius (~6371km)
        - φ is latitude
        - λ is longitude
        """
        # Convert to radians
        lat1, lon1 = location_a.to_radians()
        lat2, lon2 = location_b.to_radians()

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * asin(sqrt(a))
        distance = int(c * EARTH_RADIUS)
        return distance

    @staticmethod
    def calculate_straight_line(
        venue_location: GPSCoordinates, user_location: GPSCoordinates
    ) -> int:
        """Calculate straight line distance between two locations."""
        distance = DistanceCalculator._calculate_haversine(
            venue_location, user_location
        )
        return distance
