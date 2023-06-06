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
    AlabamaStateParks,
    ArizonaStateParks,
    FairfaxCountyParks,
    FloridaStateParks,
    MaricopaCountyParks,
    MinnesotaStateParks,
    MissouriStateParks,
    NorthernTerritory,
    OhioStateParks,
    OregonMetro,
    ReserveCalifornia,
    VirginiaStateParks,
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
    NorthernTerritory,
    FloridaStateParks,
    OregonMetro,
    OhioStateParks,
    VirginiaStateParks,
    ArizonaStateParks,
    MaricopaCountyParks,
    MissouriStateParks,
    AlabamaStateParks,
    FairfaxCountyParks,
    MinnesotaStateParks,
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
    "NorthernTerritory",
    "FloridaStateParks",
    "OregonMetro",
    "OhioStateParks",
    "VirginiaStateParks",
    "ArizonaStateParks",
    "MaricopaCountyParks",
    "MissouriStateParks",
    "AlabamaStateParks",
    "FairfaxCountyParks",
    "MinnesotaStateParks",
]
