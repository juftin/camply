"""
camply search __init__ file
"""

from typing import Dict

from camply.providers import (
    RecreationDotGovDailyTicket,
    RecreationDotGovDailyTimedEntry,
    RecreationDotGovTicket,
    RecreationDotGovTimedEntry,
)

from .base_search import BaseCampingSearch
from .search_recreationdotgov import SearchRecreationDotGov, SearchRecreationDotGovFor
from .search_yellowstone import SearchYellowstone

CAMPSITE_SEARCH_PROVIDER: Dict[str, object] = {
    "RecreationDotGov": SearchRecreationDotGov,
    "Yellowstone": SearchYellowstone,
    "RecreationDotGovDailyTicket": SearchRecreationDotGovFor(RecreationDotGovDailyTicket),
    "RecreationDotGovDailyTimedEntry": SearchRecreationDotGovFor(RecreationDotGovDailyTimedEntry),
    "RecreationDotGovTicket": SearchRecreationDotGovFor(RecreationDotGovTicket),
    "RecreationDotGovTimedEntry": SearchRecreationDotGovFor(RecreationDotGovTimedEntry),
}

__all__ = [
    "BaseCampingSearch",
    "SearchYellowstone",
    "SearchRecreationDotGov",
]
