"""
Unified Data Transfer Objects for Providers
"""

from datetime import date
from enum import StrEnum
from typing import Any

from pydantic import BaseModel, Field


class CampsiteType(StrEnum):
    """
    Standardized Campsite Type Enum
    """

    TENT = "TENT"
    RV = "RV"
    CABIN = "CABIN"
    OTHER = "OTHER"


class CampsiteDTO(BaseModel):
    """
    Standardized Campsite Data Transfer Object
    """

    campsite_id: str
    campsite_name: str
    campsite_type: CampsiteType
    capacity: int
    available_dates: list[date]
    is_electric: bool
    is_accessible: bool
    metadata: dict[str, Any] = Field(default_factory=dict)
