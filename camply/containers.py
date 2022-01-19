#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Storage Containers for the Application
"""

from datetime import datetime
import logging
from typing import NamedTuple, Tuple

logger = logging.getLogger(__name__)


class SearchWindow(NamedTuple):
    """
    Search Window for Campsite Search
    """

    start_date: datetime
    end_date: datetime


class AvailableCampsite(NamedTuple):
    """
    Campsite Storage

    This container should be universal regardless of API Provider
    """

    campsite_id: int
    booking_date: datetime
    booking_end_date: datetime
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
    facility_id: int
    booking_url: str


class CampgroundFacility(NamedTuple):
    """
    Campground Facility Data Storage
    """

    facility_name: str
    recreation_area: str
    facility_id: int
    recreation_area_id: int


class RecreationArea(NamedTuple):
    """
    Recreation Area Data Storage
    """

    recreation_area: str
    recreation_area_id: int
    recreation_area_location: str
