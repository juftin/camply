"""
providers __init__ file
"""

from typing import Union

from .base_provider import BaseProvider
from .going_to_camp.going_to_camp_provider import GoingToCamp
from .recreation_dot_gov.recdotgov_camps import RecreationDotGov
from .recreation_dot_gov.recdotgov_tours import (
    RecreationDotGovDailyTicket,
    RecreationDotGovDailyTimedEntry,
    RecreationDotGovTicket,
    RecreationDotGovTimedEntry,
)
from .usedirect.variations import (
    ReserveCalifornia,
)
from .xanterra.yellowstone_lodging import Yellowstone

ProviderType = Union[
    GoingToCamp,
    RecreationDotGov,
    RecreationDotGovDailyTicket,
    RecreationDotGovDailyTimedEntry,
    RecreationDotGovTicket,
    RecreationDotGovTimedEntry,
    Yellowstone,
    ReserveCalifornia,
]

__all__ = [
    "BaseProvider",
    "ProviderType",
    "GoingToCamp",
    "RecreationDotGov",
    "RecreationDotGovDailyTicket",
    "RecreationDotGovDailyTimedEntry",
    "RecreationDotGovTicket",
    "RecreationDotGovTimedEntry",
    "Yellowstone",
    "ReserveCalifornia",
]
