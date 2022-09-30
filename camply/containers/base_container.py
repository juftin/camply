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
        fields_to_hash = sorted(list(set(self.__fields__) - set(self.__unhashable__)))
        values_to_hash = tuple(getattr(self, key) for key in fields_to_hash)
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
