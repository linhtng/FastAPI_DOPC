# API URLs
API_BASE_URL = "https://consumer-api.development.dev.woltapi.com"
API_VERSION = "v1"
VENUE_ENDPOINT = f"{API_BASE_URL}/home-assignment-api/{API_VERSION}/venues/"

# API Endpoints
DOPC_ENDPOINT = f"/api/{API_VERSION}/delivery-order-price"

# Business Logic Constants
MAX_CART_VALUE = 1000000 * 100  # 1M EUR in cents

# Venue Service Constants
MIN_LAT = -90
MAX_LAT = 90
MIN_LON = -180
MAX_LON = 180

# Distance Calculation Constants
EARTH_RADIUS = 6371000  # meters

# Delivery Fee Calculation Constants
DISTANCE_FEE_DIVISOR = 10
