"""
camply search __init__ file
"""

from typing import Dict, Type

from camply.providers import (
    AZ_STATE_PARKS,
    FLORIDA_STATE_PARKS,
    GOING_TO_CAMP,
    NORTHERN_TERRITORY,
    OREGON_METRO,
    RECREATION_DOT_GOV,
    RECREATION_DOT_GOV_DAILY_TICKET,
    RECREATION_DOT_GOV_DAILY_TIMED_ENTRY,
    RECREATION_DOT_GOV_TICKET,
    RECREATION_DOT_GOV_TIMED_ENTRY,
    RESERVE_CALIFORNIA,
    RESERVE_OHIO,
    RESERVE_VA_PARKS,
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
from camply.search.search_usedirect import (
    SearchAZStateParks,
    SearchFloridaStateParks,
    SearchNorthernTerritory,
    SearchOregonMetro,
    SearchReserveCalifornia,
    SearchReserveOhio,
    SearchReserveVAParks,
)
from camply.search.search_yellowstone import SearchYellowstone

CAMPSITE_SEARCH_PROVIDER: Dict[str, Type[BaseCampingSearch]] = {
    RECREATION_DOT_GOV: SearchRecreationDotGov,
    YELLOWSTONE: SearchYellowstone,
    GOING_TO_CAMP: SearchGoingToCamp,
    RESERVE_CALIFORNIA: SearchReserveCalifornia,
    NORTHERN_TERRITORY: SearchNorthernTerritory,
    FLORIDA_STATE_PARKS: SearchFloridaStateParks,
    OREGON_METRO: SearchOregonMetro,
    RESERVE_OHIO: SearchReserveOhio,
    RESERVE_VA_PARKS: SearchReserveVAParks,
    AZ_STATE_PARKS: SearchAZStateParks,
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
