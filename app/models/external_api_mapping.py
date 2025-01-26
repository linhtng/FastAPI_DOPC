from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from .coordinates import GPSCoordinates

"""Models mapping Venue API responses.

Endpoints:
- /static/{venue_id} -> VenueStatic
- /dynamic/{venue_id} -> VenueDynamic

DeliverySpecs and DistanceRange model the fee calculation rules
returned by the dynamic endpoint.
"""

class DistanceRange(BaseModel):
    min: int = Field(..., ge=0, description="Minimum distance in meters")
    max: int = Field(
        ..., ge=0, description="Maximum distance in meters (0 = unavailable)"
    )
    a: int = Field(..., description="Base fee addition")
    b: int = Field(..., description="Distance multiplier")
    flag: Optional[str] = None

class DeliverySpecs(BaseModel):
    order_minimum_no_surcharge: int = Field(
        ..., description="Minimum cart value to avoid surcharge"
    )
    base_price: int = Field(..., description="Base price")
    distance_ranges: List[DistanceRange]

    @property
    def max_allowed_distance(self) -> int:
        return self.distance_ranges[-1].min
    
class VenueStatic(BaseModel):
    location: GPSCoordinates
    model_config = ConfigDict(extra="allow")


class VenueDynamic(BaseModel):
    delivery_specs: DeliverySpecs
    model_config = ConfigDict(extra="allow")

class DistanceRange(BaseModel):
    min: int = Field(..., ge=0, description="Minimum distance in meters")
    max: int = Field(
        ..., ge=0, description="Maximum distance in meters (0 = unavailable)"
    )
    a: int = Field(..., description="Base fee addition")
    b: int = Field(..., description="Distance multiplier")
    flag: Optional[str] = None