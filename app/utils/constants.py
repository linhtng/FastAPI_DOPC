# API URLs
API_BASE_URL = "https://consumer-api.development.dev.woltapi.com"
VENUE_ENDPOINT = f"{API_BASE_URL}/home-assignment-api/v1/venues/"

# Query param ranges Constants
MIN_LAT = -90
MAX_LAT = 90
MIN_LON = -180
MAX_LON = 180

# Distance Calculation Constants
EARTH_RADIUS = 6371000  # meters

# Delivery Fee Calculation Constants
DISTANCE_FEE_DIVISOR = 10

# Example Query parameters
EXPECTED_VENUE_SLUG = "home-assignment-venue-helsinki"
EXPECTED_CART_VALUE = 1000
EXPECTED_USER_LATITUDE = 60.17094
EXPECTED_USER_LONGITUDE = 24.93087

# Example Venue GPS Coordinates
EXPECTED_VENUE_LATITUDE = 60.17012143
EXPECTED_VENUE_LONGITUDE = 24.92813512

# Example Distance Fee components
EXPECTED_BASE_PRICE = 190
EXPECTED_MIN_ORDER_NO_SURCHARGE = 1000