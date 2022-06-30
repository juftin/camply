"""
Project Configuration for Yellowstone Variables
"""

from collections import OrderedDict
from enum import Enum
from typing import Dict


class SearchConfig:
    """
    File Path Storage Class
    """

    POLLING_INTERVAL_MINIMUM: int = 5  # 5 MINUTES
    RECOMMENDED_POLLING_INTERVAL: int = 10  # 10 MINUTES
    ERROR_MESSAGE: str = "No search days configured. Exiting"
    MINIMUM_CAMPSITES_FIRST_NOTIFY: int = 5
    MAXIMUM_NOTIFICATION_BATCH_SIZE: int = 20


class EquipmentOptions(str, Enum):
    """
    Enumeration of the Equipment Options
    """

    tent = "tent"
    rv = "rv"
    trailer = "trailer"
    vehicle = "vehicle"
    other = "other"

    __all_accepted_equipment__ = [tent, rv, trailer, vehicle]


class EquipmentConfig:
    """
    Campsite Equipment Configuration
    """

    EQUIPMENT_MAPPING = OrderedDict()

    EQUIPMENT_MAPPING[EquipmentOptions.tent] = [
        "Tent",
        "Large Tent Over 9X12",
        r"Large Tent Over 9X12`",
        "Small Tent",
    ]
    EQUIPMENT_MAPPING[EquipmentOptions.rv] = [
        "RV",
        "Pop up",
        "Caravan/Camper Van",
        "RV/Motorhome",
        "Fifth Wheel",
    ]
    EQUIPMENT_MAPPING[EquipmentOptions.trailer] = ["Trailer"]
    EQUIPMENT_MAPPING[EquipmentOptions.vehicle] = [
        "Pickup Camper",
        "Vehicle",
        "Car",
    ]
    EQUIPMENT_MAPPING[EquipmentOptions.other] = ["Hammock", "Horse", "Boat", ""]

    EQUIPMENT_REVERSE_MAPPING: Dict[str, str] = {}
    for key, list_of_values in EQUIPMENT_MAPPING.items():
        for value in list_of_values:
            EQUIPMENT_REVERSE_MAPPING[value] = key
