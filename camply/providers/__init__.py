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
from .reserve_california.reserve_california import ReserveCalifornia
from .xanterra.yellowstone_lodging import YellowstoneLodging

RECREATION_DOT_GOV = "RecreationDotGov"
YELLOWSTONE = "Yellowstone"
GOING_TO_CAMP = "GoingToCamp"
RECREATION_DOT_GOV_DAILY_TICKET = "RecreationDotGovDailyTicket"
RECREATION_DOT_GOV_DAILY_TIMED_ENTRY = "RecreationDotGovDailyTimedEntry"
RECREATION_DOT_GOV_TICKET = "RecreationDotGovTicket"
RECREATION_DOT_GOV_TIMED_ENTRY = "RecreationDotGovTimedEntry"
RESERVE_CALIFORNIA = "ReserveCalifornia"

ProviderType = Union[
    GoingToCampProvider,
    RecreationDotGov,
    RecreationDotGovDailyTicket,
    RecreationDotGovDailyTimedEntry,
    RecreationDotGovTicket,
    RecreationDotGovTimedEntry,
    YellowstoneLodging,
    ReserveCalifornia,
]

__all__ = [
    "BaseProvider",
    "ProviderType",
    "GoingToCampProvider",
    "RecreationDotGov",
    "RecreationDotGovDailyTicket",
    "RecreationDotGovDailyTimedEntry",
    "RecreationDotGovTicket",
    "RecreationDotGovTimedEntry",
    "YellowstoneLodging",
    "ReserveCalifornia",
    "RECREATION_DOT_GOV",
    "YELLOWSTONE",
    "GOING_TO_CAMP",
    "RECREATION_DOT_GOV_DAILY_TICKET",
    "RECREATION_DOT_GOV_DAILY_TIMED_ENTRY",
    "RECREATION_DOT_GOV_TICKET",
    "RECREATION_DOT_GOV_TIMED_ENTRY",
    "RESERVE_CALIFORNIA",
]
