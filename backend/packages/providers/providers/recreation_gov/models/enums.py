"""
Recreation.gov Specific Enums
"""

from enum import StrEnum


class RecDotGovAvailabilityStatus(StrEnum):
    """
    Availability status values returned by Recreation.gov availability API.
    """

    AVAILABLE = "Available"
    RESERVED = "Reserved"
    NOT_AVAILABLE = "Not Available"
    NOT_RESERVABLE = "Not Reservable"
    NOT_RESERVABLE_MANAGEMENT = "Not Reservable Management"
    NOT_AVAILABLE_CUTOFF = "Not Available Cutoff"
    LOTTERY = "Lottery"
    OPEN = "Open"
    NYR = "NYR"
    CLOSED = "Closed"


class RecDotGovEquipmentType(StrEnum):
    """
    Equipment type keywords used to classify RV campsites.
    """

    RV = "rv"
    TRAILER = "trailer"
    MOTORHOME = "motorhome"
    FIFTH_WHEEL = "fifth wheel"
    PICKUP_CAMPER = "pickup camper"
    POP_UP = "pop up"
    CARAVAN = "caravan"


class TentKeywords(StrEnum):
    """
    Keywords indicating tent campsites.
    """

    TENT = "tent"


class RVKeywords(StrEnum):
    """
    Keywords indicating RV/trailer campsites.
    """

    RV = "rv"
    TRAILER = "trailer"
    MOTORHOME = "motorhome"


class CabinKeywords(StrEnum):
    """
    Keywords indicating cabin/shelter campsites.
    """

    CABIN = "cabin"
    YURT = "yurt"
    SHELTER = "shelter"
