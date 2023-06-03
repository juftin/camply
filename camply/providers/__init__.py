"""
providers __init__ file
"""

from typing import Union

from .base_provider import BaseProvider
from .going_to_camp.going_to_camp_provider import GoingToCampProvider
from .recreation_dot_gov.recdotgov_camps import RecreationDotGov
from .recreation_dot_gov.recdotgov_tours import (
    RecreationDotGovDailyTicket,
    RecreationDotGovDailyTimedEntry,
    RecreationDotGovTicket,
    RecreationDotGovTimedEntry,
)
from .usedirect.variations import (
    FloridaStateParks,
    NorthernTerritory,
    OregonMetro,
    ReserveCalifornia,
    ReserveOhio,
    ReserveVAParks,
)
from .xanterra.yellowstone_lodging import YellowstoneLodging

# Provider Class Names
RECREATION_DOT_GOV = "RecreationDotGov"
YELLOWSTONE = "Yellowstone"
GOING_TO_CAMP = "GoingToCamp"
RECREATION_DOT_GOV_DAILY_TICKET = "RecreationDotGovDailyTicket"
RECREATION_DOT_GOV_DAILY_TIMED_ENTRY = "RecreationDotGovDailyTimedEntry"
RECREATION_DOT_GOV_TICKET = "RecreationDotGovTicket"
RECREATION_DOT_GOV_TIMED_ENTRY = "RecreationDotGovTimedEntry"
RESERVE_CALIFORNIA = "ReserveCalifornia"
NORTHERN_TERRITORY = "NorthernTerritory"
FLORIDA_STATE_PARKS = "FloridaStateParks"
OREGON_METRO = "OregonMetro"
RESERVE_OHIO = "ReserveOhio"
RESERVE_VA_PARKS = "ReserveVAParks"

ProviderType = Union[
    GoingToCampProvider,
    RecreationDotGov,
    RecreationDotGovDailyTicket,
    RecreationDotGovDailyTimedEntry,
    RecreationDotGovTicket,
    RecreationDotGovTimedEntry,
    YellowstoneLodging,
    ReserveCalifornia,
    NorthernTerritory,
    FloridaStateParks,
    OregonMetro,
    ReserveOhio,
    ReserveVAParks,
]

__all__ = [
    "BaseProvider",
    "ProviderType",
    "GoingToCampProvider",
    "GOING_TO_CAMP",
    "RecreationDotGov",
    "RECREATION_DOT_GOV",
    "RecreationDotGovDailyTicket",
    "RECREATION_DOT_GOV_DAILY_TICKET",
    "RecreationDotGovDailyTimedEntry",
    "RECREATION_DOT_GOV_DAILY_TIMED_ENTRY",
    "RecreationDotGovTicket",
    "RECREATION_DOT_GOV_TICKET",
    "RecreationDotGovTimedEntry",
    "RECREATION_DOT_GOV_TIMED_ENTRY",
    "YellowstoneLodging",
    "YELLOWSTONE",
    "ReserveCalifornia",
    "RESERVE_CALIFORNIA",
    "NorthernTerritory",
    "NORTHERN_TERRITORY",
    "FloridaStateParks",
    "FLORIDA_STATE_PARKS",
    "OregonMetro",
    "OREGON_METRO",
    "ReserveOhio",
    "RESERVE_OHIO",
    "ReserveVAParks",
    "RESERVE_VA_PARKS",
]
