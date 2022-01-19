#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Searching Utilities
"""

import logging
from random import uniform
from time import sleep
from typing import List, Optional, Union

from camply.config import RecreationBookingConfig
from camply.containers import AvailableCampsite, CampgroundFacility, SearchWindow
from camply.providers import RecreationDotGov
from camply.search.base_search import BaseCampingSearch, SearchError

logger = logging.getLogger(__name__)


class SearchRecreationDotGov(BaseCampingSearch):
    """
    Camping Search Object
    """

    def __init__(self, search_window: Union[SearchWindow, List[SearchWindow]],
                 recreation_area: Optional[int] = None,
                 campgrounds: Optional[Union[List[int], int]] = None,
                 weekends_only: bool = False,
                 nights: int = 1) -> None:
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
        nights: int
            minimum number of consecutive nights to search per campsite,defaults to 1
        """
        super().__init__(provider=RecreationDotGov(),
                         search_window=search_window,
                         weekends_only=weekends_only,
                         nights=nights)
        self._recreation_area_id = self._make_list(recreation_area)
        self._campground_object = campgrounds
        self.weekends_only = weekends_only
        assert any([campgrounds not in [[], None], recreation_area is not None]) is True
        self.campsite_finder: RecreationDotGov
        self.campgrounds = self._get_searchable_campgrounds()

    def _get_searchable_campgrounds(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search

        This handles scenarios where a recreation area is provided instead
        of a campground list

        Returns
        -------
        searchable_campgrounds: List[int]
            List of searchable campground IDs
        """
        if self._campground_object not in [[], None]:
            searchable_campgrounds = self._get_campgrounds_by_campground_id()
        elif self._recreation_area_id is not None:
            searchable_campgrounds = self._get_campgrounds_by_recreation_area_id()
        else:
            raise RuntimeError("You must provide a Campground or Recreation Area ID")
        return searchable_campgrounds

    def _get_campgrounds_by_campground_id(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search when provided with campground IDs

        Returns
        -------
        returned_sites: List[int]
            List of searchable campground IDs
        """
        campground_list = self._make_list(self._campground_object)
        facilities = self.campsite_finder.find_campgrounds(campground_id=campground_list)
        return facilities

    def _get_campgrounds_by_recreation_area_id(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search when provided with Recreation Area IDs

        Returns
        -------
        campgrounds: List[CampgroundFacility]
        """
        campgrounds = list()
        for rec_area in self._recreation_area_id:
            campground_array = self.campsite_finder.find_facilities_per_recreation_area(
                rec_area_id=rec_area)
            campgrounds += campground_array
        return campgrounds

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return All Monthly Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        found_campsites = list()
        if len(self.campgrounds) == 0:
            error_message = "No campgrounds found to search"
            logger.error(error_message)
            raise SearchError(error_message)
        logger.info(f"Searching across {len(self.campgrounds)} campgrounds")
        for index, campground in enumerate(self.campgrounds):
            for month in self.search_months:
                logger.info(
                    f"Searching {campground.facility_name}, {campground.recreation_area} "
                    f"({campground.facility_id}) for availability: "
                    f"{month.strftime('%B, %Y')}")
                availabilities = self.campsite_finder.get_recdotgov_data(
                    campground_id=campground.facility_id, month=month)
                campsites = self.campsite_finder.process_campsite_availability(
                    availability=availabilities,
                    recreation_area=campground.recreation_area,
                    recreation_area_id=campground.recreation_area_id,
                    facility_name=campground.facility_name,
                    facility_id=campground.facility_id,
                    month=month)
                found_campsites += campsites
                if index + 1 < len(self.campgrounds):
                    sleep(round(uniform(*RecreationBookingConfig.RATE_LIMITING), 2))
        campsite_df = self.campsites_to_df(campsites=found_campsites)
        campsite_df_validated = self._filter_date_overlap(campsites=campsite_df)
        compiled_campsite_df = self._consolidate_campsites(
            campsite_df=campsite_df_validated,
            nights=self.nights)
        compiled_campsites = self.df_to_campsites(campsite_df=compiled_campsite_df)
        return compiled_campsites
