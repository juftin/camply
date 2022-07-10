"""
camply search __init__ file
"""

from typing import Dict

from .base_search import BaseCampingSearch
from .search_going_to_camp import SearchGoingToCamp
from .search_recreationdotgov import SearchRecreationDotGov
from .search_yellowstone import SearchYellowstone

CAMPSITE_SEARCH_PROVIDER: Dict[str, object] = {
    "RecreationDotGov": SearchRecreationDotGov,
    "Yellowstone": SearchYellowstone,
    "GoingToCamp": SearchGoingToCamp,
}

__all__ = [
    "BaseCampingSearch",
    "SearchYellowstone",
    "SearchRecreationDotGov",
]
