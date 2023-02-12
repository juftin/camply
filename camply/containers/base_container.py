"""
Base Pydantic Object for Containers
"""

from typing import Any, Set

from pydantic import BaseModel


class CamplyModel(BaseModel):
    """
    Hashable Pydantic Model
    """

    __unhashable__: Set[str] = set()

    def __hash__(self):
        """
        Hash Method for Pydantic BaseModels
        """
        return hash(self.__class__) + hash(
            tuple(
                value
                for key, value in self.__dict__.items()
                if key not in self.__unhashable__
            )
        )

    def __eq__(self, other: Any) -> bool:
        """
        Exclude Unhashable Fields When Evaluating Equality
        """
        if isinstance(other, CamplyModel):
            return self.dict(exclude=self.__unhashable__) == other.dict(
                exclude=other.__unhashable__
            )
        else:
            return self.dict(exclude=self.__unhashable__) == other

    class Config:
        """
        Camply Wide Configuration
        """

        anystr_strip_whitespace = True


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


#############################
# GoingToCamp Base Containers
#############################


class GoingToCampEquipment(CamplyModel):
    """
    Model of GoingToCamp provider equipment
    """

    equipment_name: str
    equipment_type_id: int
