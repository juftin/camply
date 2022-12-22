"""
providers __init__ file
"""

from .base_provider import BaseProvider
from .going_to_camp.going_to_camp_provider import GoingToCampProvider
from .recreation_dot_gov.recdotgov_provider import RecreationDotGov
from .xanterra.yellowstone_lodging import YellowstoneLodging

__all__ = [
    "BaseProvider",
    "GoingToCampProvider",
    "RecreationDotGov",
    "YellowstoneLodging",
]

GOING_TO_CAMP = "goingtocamp"
RECREATION_DOT_GOV = "recreationdotgov"
YELLOWSTONE = "yellowstone"
