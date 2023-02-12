"""
Storage Containers for the Application
"""

import datetime
import logging
from typing import List, Optional, Tuple, Union

from pydantic import validator

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

    @validator("start_date")
    @classmethod
    def start_date_must_be_in_future(cls, v):
        """
        Validate that start_date is in the future.

        Coerece start date to today's date when it is not in the future.
        """
        current_date = datetime.datetime.now().date()
        if v < current_date:
            return current_date

        return v

    @validator("end_date")
    @classmethod
    def end_date_must_be_in_future(cls, v):
        """
        Validate that end_date is in the future
        """
        current_date = datetime.datetime.now().date()
        if v < current_date:
            raise ValueError("must be in the future")

        return v

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

    def get_current_start_date(self) -> datetime.date:
        """
        Return a start date with the current day in mind
        """
        return max((datetime.datetime.now().date(), self.start_date))


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
    campsite_loop_name: Optional[str]
    campsite_type: Optional[str]
    campsite_occupancy: Tuple[int, int]
    campsite_use_type: Optional[str]
    availability_status: str
    recreation_area: str
    recreation_area_id: Union[int, str]
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
    recreation_area_id: Union[int, str]
    map_id: Optional[int]
    coordinates: Optional[Tuple[float, float]]


class RecreationArea(CamplyModel):
    """
    Recreation Area Data Storage
    """

    recreation_area: str
    recreation_area_id: Union[int, str]
    recreation_area_location: str
    coordinates: Optional[Tuple[float, float]]
    description: Optional[str]


class AvailableResource(CamplyModel):
    """
    A resource that is available for booking
    """

    resource_id: int
    map_id: int
