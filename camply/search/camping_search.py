#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Scraping Utilities
"""

from datetime import datetime, timedelta
import logging
from random import random
from time import sleep
from typing import List, Optional, Set, Union

from camply.containers import AvailableCampsite, SearchWindow
from camply.providers import RecreationDotGov
from camply.search.base_search import BaseCampingSearch
from camply.utils import make_list
from camply.utils.logging_utils import get_emoji

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
        self.campgrounds: List[AvailableCampsite] = self._get_searchable_campgrounds()

    def search_matching_campsites_available(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        matching_campgrounds = list()
        monthly_campgrounds = self.search_campsite_months()
        for camp in monthly_campgrounds:
            if camp.booking_date in self.search_days:
                matching_campgrounds.append(camp)
        logger.info(f"{(get_emoji(matching_campgrounds) + ' ') * 4}{len(matching_campgrounds)} "
                    "Campsites Matching Search Preferences")
        return matching_campgrounds

    def _get_searchable_campgrounds(self) -> List[int]:
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
                for campground in campground_array:
                    campground_data, campground_facility = \
                        self.campsite_finder.process_facilities_responses(facility=campground)
                    processed_array.append(campground_facility)
            return processed_array

    def _get_search_months(self) -> List[datetime]:
        """
        Get the Unique Months that need to be Searched

        Returns
        -------
        search_months: Set[datetime]
            Datetime Months to search for reservations
        """
        search_days = self.search_days.copy()
        truncated_months = set([day.replace(day=1) for day in search_days])
        if len(truncated_months) > 1:
            logger.info(f"{len(truncated_months)} different months selected for search, "
                        f"ranging from {min(search_days).strftime('%Y-%m-%d')} to "
                        f"{max(search_days).strftime('%Y-%m-%d')}")
            return sorted(list(truncated_months))
        elif len(truncated_months) == 0:
            logger.info(f"No search days configured. Exiting")
            raise RuntimeError("No search days configured. Exiting")
        else:
            return sorted(list(truncated_months))

    def search_campsite_months(self) -> List[AvailableCampsite]:
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
                availabilities = self.campsite_finder._rec_availability_get_data(
                    campground_id=campground.facility_id, month=month)
                campgrounds = self.campsite_finder._process_campsite_availability(
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
