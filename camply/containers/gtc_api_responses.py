"""
GoingToCamp provider containers
"""
from typing import Any, Dict, List, Optional

from camply.containers.base_container import CamplyModel


class ResourceLocation(CamplyModel):
    """
    /api/maps
    """

    id: Optional[int]
    rec_area_id: int
    park_alerts: Optional[str]
    resource_categories: Optional[List[int]]
    resource_location_id: Optional[int]
    resource_location_name: str
    region_name: str


class ResourceAvailabilityUnit(CamplyModel):
    """
    /api/availability/map: resourceAvailabilities
    """

    availability: int
    remainingQuota: Optional[int]


class AvailabilityResponse(CamplyModel):
    """
    /api/availability/map
    """

    mapId: int
    mapAvailabilities: List[int] = []
    resourceAvailabilities: Dict[int, List[ResourceAvailabilityUnit]] = {}
    mapLinkAvailabilities: Dict[str, Any] = {}


class SearchFilter(CamplyModel):
    """
    /api/availability/map: API Filter
    """

    mapId: int
    resourceLocationId: int
    bookingCategoryId: int
    startDate: str
    endDate: str
    isReserving: bool
    getDailyAvailability: bool
    partySize: int
    numEquipment: int
    equipmentCategoryId: int
    filterData: List[Any] = []
    subEquipmentCategoryId: Optional[int] = None
