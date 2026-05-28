"""
Recreation.gov Raw API Pydantic Models
"""

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class RecDotGovEquipment(BaseModel):
    """
    Permitted equipment definition for Recreation.gov campsites
    """

    equipment_name: str
    max_length: float


class RecDotGovAttribute(BaseModel):
    """
    Campsite attributes (e.g. electric hookup, sewer, pets allowed)
    """

    attribute_category: str | None = None
    attribute_id: int
    attribute_name: str
    attribute_value: Any


class RecDotGovCampsite(BaseModel):
    """
    Single campsite entry in Recreation.gov campsite search results
    """

    campsite_id: int
    name: str
    type: str | None = None
    accessible: bool = False
    loop: str = ""
    latitude: float | None = None
    longitude: float | None = None
    permitted_equipment: list[RecDotGovEquipment] = Field(default_factory=list)
    attributes: list[RecDotGovAttribute] = Field(default_factory=list)


class RecDotGovCampsiteResponse(BaseModel):
    """
    Response wrapper for campsite search metadata endpoint
    """

    campsites: list[RecDotGovCampsite]
    size: int
    start: int
    total: int


class CampsiteAvailabilityCampsite(BaseModel):
    """
    Single campsite's monthly availability block
    """

    availabilities: dict[datetime, str] = Field(default_factory=dict)
    loop: str = "Default Loop"
    campsite_type: str | None = None
    max_num_people: int = 1
    min_num_people: int = 1
    type_of_use: str | None = None
    site: str = "Default Site"


class CampsiteAvailabilityResponse(BaseModel):
    """
    Response wrapper for monthly availability endpoint
    """

    campsites: dict[int, CampsiteAvailabilityCampsite]


class RecreationGovCampsiteMetadata(BaseModel):
    """
    Standardized metadata block for Recreation.gov campsites.
    """

    loop: str
    site: str
    type_of_use: str | None = None
    permitted_equipment: list[RecDotGovEquipment] = Field(default_factory=list)
    attributes: list[RecDotGovAttribute] = Field(default_factory=list)
    latitude: float | None = None
    longitude: float | None = None


class RecDotGovCampsiteSearchParams(BaseModel):
    """
    Query parameters for campsite search metadata endpoint
    """

    start: int = 0
    size: int = 1000
    fq: list[str] = Field(default_factory=list)
    include_non_site_specific_campsites: bool = True


class RecDotGovAvailabilityParams(BaseModel):
    """
    Query parameters for campsite availability endpoint
    """

    start_date: str
