"""
camply search __init__ file
"""

from typing import Dict, List, Type

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
    SearchAlabamaStateParks,
    SearchAZStateParks,
    SearchFloridaStateParks,
    SearchMaricopaCountyParks,
    SearchMissouriStateParks,
    SearchNorthernTerritory,
    SearchOregonMetro,
    SearchReserveCalifornia,
    SearchReserveOhio,
    SearchReserveVAParks,
)
from camply.search.search_yellowstone import SearchYellowstone

# Register Providers Here with their Search class
__search_providers__: List[Type[BaseCampingSearch]] = [
    SearchRecreationDotGov,
    SearchYellowstone,
    SearchGoingToCamp,
    # UseDirect
    SearchReserveCalifornia,
    SearchNorthernTerritory,
    SearchFloridaStateParks,
    SearchOregonMetro,
    SearchReserveOhio,
    SearchReserveVAParks,
    SearchAZStateParks,
    SearchMaricopaCountyParks,
    SearchMissouriStateParks,
    SearchAlabamaStateParks,
    # Tours and Timed Entry (RecDotGov)
    SearchRecreationDotGovTicket,
    SearchRecreationDotGovTimedEntry,
    SearchRecreationDotGovDailyTicket,
    SearchRecreationDotGovDailyTimedEntry,
]

CAMPSITE_SEARCH_PROVIDER: Dict[str, Type[BaseCampingSearch]] = {
    provider.provider_class.__name__: provider for provider in __search_providers__
}
