"""
Base Pydantic Object for Containers
"""

from pydantic import BaseModel


class CamplyModel(BaseModel):
    """
    Hashable Pydantic Model
    """

    def __hash__(self):
        """
        Hash Method for Pydantic BaseModels
        """
        return hash((type(self),) + tuple(self.__dict__.values()))
