"""
Base Pydantic Object for Containers
"""

from typing import Any, List

from pydantic import BaseModel


class CamplyModel(BaseModel):
    """
    Hashable Pydantic Model
    """

    __unhashable__: List[str] = []

    def __hash__(self):
        """
        Hash Method for Pydantic BaseModels
        """
        values_to_hash = tuple(
            getattr(self, key)
            for key in self.__fields__
            if key not in self.__unhashable__
        )
        return hash((type(self),) + values_to_hash)


############################
# RecDotGov Base Containers
############################


class RecDotGovAttribute(CamplyModel):
    """
    Attribute Object on the Recreation.gov Campsite
    """

    attribute_category: str
    attribute_id: int
    attribute_name: str
    attribute_value: Any


class RecDotGovEquipment(CamplyModel):
    """
    Equipment Object on the Recreation.gov Campsite
    """

    equipment_name: str
    max_length: float
