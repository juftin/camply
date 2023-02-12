"""
camply search __init__ file
"""

from typing import Dict, Type

from camply.providers import (
    GOING_TO_CAMP,
    RECREATION_DOT_GOV,
    RECREATION_DOT_GOV_DAILY_TICKET,
    RECREATION_DOT_GOV_DAILY_TIMED_ENTRY,
    RECREATION_DOT_GOV_TICKET,
    RECREATION_DOT_GOV_TIMED_ENTRY,
    RESERVE_CALIFORNIA,
    YELLOWSTONE,
)
from camply.search.base_search import BaseCampingSearch
from camply.search.search_going_to_camp import SearchGoingToCamp
from camply.search.search_recreationdotgov import (
    SearchRecreationDotGov,
    SearchRecreationDotGovDailyTicket,
    SearchRecreationDotGovDailyTimedEntry,
    SearchRecreationDotGovTicket,
    SearchRecreationDotGovTimedEntry,
)
from camply.search.search_reserve_california import SearchReserveCalifornia
from camply.search.search_yellowstone import SearchYellowstone

CAMPSITE_SEARCH_PROVIDER: Dict[str, Type[BaseCampingSearch]] = {
    RECREATION_DOT_GOV: SearchRecreationDotGov,
    YELLOWSTONE: SearchYellowstone,
    GOING_TO_CAMP: SearchGoingToCamp,
    RESERVE_CALIFORNIA: SearchReserveCalifornia,
    # Tours and Timed Entry (RecDotGov)
    RECREATION_DOT_GOV_TICKET: SearchRecreationDotGovTicket,
    RECREATION_DOT_GOV_TIMED_ENTRY: SearchRecreationDotGovTimedEntry,
    RECREATION_DOT_GOV_DAILY_TICKET: SearchRecreationDotGovDailyTicket,
    RECREATION_DOT_GOV_DAILY_TIMED_ENTRY: SearchRecreationDotGovDailyTimedEntry,
}

__all__ = [
    "BaseCampingSearch",
    "SearchYellowstone",
    "SearchRecreationDotGov",
]
