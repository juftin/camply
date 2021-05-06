#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Scraping Utilities
"""

import logging
from random import random
from time import sleep
from typing import List, Optional, Union

from camply.containers import AvailableCampsite, CampgroundFacility, SearchWindow
from camply.providers import RecreationDotGov
from camply.search.base_search import BaseCampingSearch
from camply.utils import make_list

logger = logging.getLogger(__name__)


class SearchRecreationDotGov(BaseCampingSearch):
    """
    Camping Search Object
    """

    def __init__(self, search_window: Union[SearchWindow, List[SearchWindow]],
                 recreation_area: Optional[int] = None,
                 campgrounds: Optional[Union[List[int], int]] = None,
                 weekends_only: bool = False) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        recreation_area: int
            ID of Recreation Area (i.e. 2907 - Rocky Mountain National Park)
        campgrounds: Optional[Union[List[int], int]]
            Campground ID or List of Campground IDs
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
        """
        super(SearchRecreationDotGov, self).__init__(provider=RecreationDotGov(),
                                                     search_window=search_window,
                                                     weekends_only=weekends_only)
        self._recreation_area_id = make_list(recreation_area)
        self._campground_object = campgrounds
        self.weekends_only = weekends_only
        assert any([campgrounds is not None, recreation_area is not None]) is True
        self.campsite_finder: RecreationDotGov
        self.campgrounds = self._get_searchable_campgrounds()

    def _get_searchable_campgrounds(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search, this handles scenarios
        where a recreation area is provided instead of a campground list

        Returns
        -------
        searchable_campgrounds: List[int]
            List of searchable campground IDs
        """
        if self._campground_object is not None:
            returned_sites = list()
            for campground_id in make_list(self._campground_object):
                facility = self.campsite_finder.find_campsites(campground_id=campground_id)
                campground_facility: CampgroundFacility
                campground_data, campground_facility = \
                    self.campsite_finder.process_facilities_responses(facility=facility)
                self.campsite_finder.log_sorted_response(response_array=[campground_facility])
                returned_sites.append(campground_facility)
            return returned_sites
        elif self._recreation_area_id is not None:
            processed_array = list()
            for rec_area in self._recreation_area_id:
                campground_array = self.campsite_finder.find_facilities_per_recreation_area(
                    rec_area_id=rec_area)
                campground_facility: CampgroundFacility
                for campground in campground_array:
                    campground_data, campground_facility = \
                        self.campsite_finder.process_facilities_responses(facility=campground)
                    processed_array.append(campground_facility)
            return processed_array

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return All Monthly Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        found_campsites = list()
        logger.info(f"Searching across {len(self.campgrounds)} campgrounds")
        for index, campground in enumerate(self.campgrounds):
            for month in self.search_months:
                logger.info(f"Searching {campground.facility_name}, {campground.recreation_area} "
                            f"({campground.facility_id}) for availability: "
                            f"{month.strftime('%B, %Y')}")
                availabilities = self.campsite_finder.get_recdotgov_data(
                    campground_id=campground.facility_id, month=month)
                campgrounds = self.campsite_finder.process_campsite_availability(
                    availability=availabilities,
                    recreation_area=campground.recreation_area,
                    recreation_area_id=campground.recreation_area_id,
                    facility_name=campground.facility_name,
                    facility_id=campground.facility_id,
                    month=month)
                found_campsites += campgrounds
                if index + 1 < len(self.campgrounds):
                    sleep(random() + 0.5)
        return found_campsites
