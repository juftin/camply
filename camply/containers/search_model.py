"""
Pydantic model for YAML files
"""

import datetime
from enum import Enum
from typing import List, Optional, Tuple, Union

from pydantic import Field, validator

from camply.config import SearchConfig
from camply.containers import CamplyModel
from camply.search import CAMPSITE_SEARCH_PROVIDER

ArrayOrSingleInt = Optional[Union[int, List[int]]]
ArrayOrSingleStr = Optional[Union[str, List[str]]]
ArrayOrSingle = Optional[Union[ArrayOrSingleInt, ArrayOrSingleStr]]
EquipmentTuple = Optional[Tuple[str, int]]
ArrayOrSingleEquipment = Optional[Union[EquipmentTuple, List[EquipmentTuple]]]


class StrEnum(str, Enum):
    """
    String Enum
    """


ProviderEnum = StrEnum(
    "ProviderEnum", {value: value for value in CAMPSITE_SEARCH_PROVIDER.keys()}
)
ProviderEnum.__doc__ = "Campsite Provider Names"


class YamlSearchFile(CamplyModel):
    """
    Campsite Search Data Model
    """

    provider: ProviderEnum = Field(
        description="Campsite provider", default="RecreationDotGov"
    )
    recreation_area: ArrayOrSingle = None
    campgrounds: ArrayOrSingle = None
    campsites: ArrayOrSingle = None
    start_date: Union[datetime.date, List[datetime.date]]
    end_date: Union[datetime.date, List[datetime.date]]
    days: Optional[List[str]] = None
    weekends: bool = False
    nights: int = 1
    continuous: bool = True
    polling_interval: int = SearchConfig.RECOMMENDED_POLLING_INTERVAL
    notifications: ArrayOrSingleStr = "silent"
    search_forever: bool = False
    search_once: bool = False
    notify_first_try: bool = False
    equipment: ArrayOrSingleEquipment = None
    offline_search: bool = False
    offline_search_path: Optional[str] = None

    @validator("provider", pre=True)
    def validate_provider(cls, value):
        """
        Validate provider
        """
        lowercase_enum_dict = {
            key.lower(): key for key in ProviderEnum.__members__.keys()
        }
        if value.lower() in lowercase_enum_dict.keys():
            return lowercase_enum_dict[value.lower()]
        else:
            return value

    @validator("equipment", pre=True)
    def validate_equipment(cls, value) -> ArrayOrSingleEquipment:
        """
        Validate equipment
        """
        equipment_tuple_length = 2
        if (
            isinstance(value, list)
            and len(value) == equipment_tuple_length
            and isinstance(value[0], str)
        ):
            return [tuple(value)]
        else:
            return value
