"""
Storage Containers for the Application
"""

import datetime
import logging
from typing import List, Optional, Tuple, Union

from camply.containers.base_container import (
    CamplyModel,
    RecDotGovAttribute,
    RecDotGovEquipment,
)

logger = logging.getLogger(__name__)


class SearchWindow(CamplyModel):
    """
    Search Window for Campsite Search
    """

    start_date: datetime.date
    end_date: datetime.date

    def get_date_range(self) -> List[datetime.date]:
        """
        Generate a List of Dates Between two Dates

        Returns
        -------
        List[datetime.date]
        """
        return [
            self.start_date + datetime.timedelta(days=x)
            for x in range((self.end_date - self.start_date).days)
        ]


class AvailableCampsite(CamplyModel):
    """
    Campsite Storage

    This container should be universal regardless of API Provider
    """

    campsite_id: Union[int, str]
    booking_date: datetime.datetime
    booking_end_date: datetime.datetime
    booking_nights: int
    campsite_site_name: str
    campsite_loop_name: str
    campsite_type: str
    campsite_occupancy: Tuple[int, int]
    campsite_use_type: str
    availability_status: str
    recreation_area: str
    recreation_area_id: int
    facility_name: str
    facility_id: Union[int, str]
    booking_url: str

    permitted_equipment: Optional[List[RecDotGovEquipment]]
    campsite_attributes: Optional[List[RecDotGovAttribute]]

    __unhashable__ = {"permitted_equipment", "campsite_attributes"}


class CampgroundFacility(CamplyModel):
    """
    Campground Facility Data Storage
    """

    facility_name: str
    recreation_area: str
    facility_id: Union[int, str]
    recreation_area_id: int


class RecreationArea(CamplyModel):
    """
    Recreation Area Data Storage
    """

    recreation_area: str
    recreation_area_id: int
    recreation_area_location: str
