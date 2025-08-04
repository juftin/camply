"""
GoingToCamp provider containers
"""
from typing import List, Optional

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
