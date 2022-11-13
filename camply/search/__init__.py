"""
camply search __init__ file
"""

from typing import Dict

from .base_search import BaseCampingSearch
from .search_recreationdotgov import SearchRecreationDotGov, SearchRecreationDotGovTicket, SearchRecreationDotGovTimedEntry
from .search_yellowstone import SearchYellowstone

CAMPSITE_SEARCH_PROVIDER: Dict[str, object] = {
    "RecreationDotGov": SearchRecreationDotGov,
    "Yellowstone": SearchYellowstone,
    "RecreationDotGovTicket": SearchRecreationDotGovTicket,
    "RecreationDotGovTimedEntry": SearchRecreationDotGovTimedEntry,
}

__all__ = [
    "BaseCampingSearch",
    "SearchYellowstone",
    "SearchRecreationDotGov",
]
