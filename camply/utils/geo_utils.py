"""
Geo-coding and distance utilities
"""

import math
from typing import Tuple

from geopy.geocoders import Nominatim

from camply.exceptions import CamplyError

_EARTH_RADIUS_MILES = 3958.8
_GEOCODER = Nominatim(user_agent="camply")


def haversine_distance_miles(
    lat1: float, lon1: float, lat2: float, lon2: float
) -> float:
    """Return the great-circle distance in miles between two lat/lon points."""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    return _EARTH_RADIUS_MILES * 2 * math.asin(math.sqrt(a))


def geocode_location(place_name: str) -> Tuple[float, float]:
    """Convert a place name to (latitude, longitude) using Nominatim.

    Raises CamplyError if the place cannot be geocoded.
    """
    location = _GEOCODER.geocode(place_name)
    if location is None:
        raise CamplyError(f"Could not geocode location: {place_name!r}")
    return location.latitude, location.longitude
