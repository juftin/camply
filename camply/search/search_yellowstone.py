#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Yellowstone Lodging Web Searching Utilities
"""

from datetime import datetime
import logging
from typing import List, Optional, Set, Union

from camply.config import YellowstoneConfig
from camply.containers import AvailableCampsite, SearchWindow
from camply.providers import YellowstoneLodging
from camply.search.base_search import BaseCampingSearch, SearchError

logger = logging.getLogger(__name__)


class SearchYellowstone(BaseCampingSearch):
    """
    Camping Search Object
    """

    # noinspection PyUnusedLocal
    def __init__(self, search_window: Union[SearchWindow, List[SearchWindow]],
                 weekends_only: bool = False,
                 campgrounds: Optional[Union[List[str], str]] = None,
                 **kwargs) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
        campgrounds: Optional[Union[List[str], str]]
            Campground ID or List of Campground IDs
        """
        super().__init__(provider=YellowstoneLodging(),
                         search_window=search_window,
                         weekends_only=weekends_only)
        self.campgrounds = self._make_list(campgrounds)

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Search for all matching campsites in Yellowstone.

        Returns
        -------
        List[AvailableCampsite]
        """
        all_campsites = list()
        searchable_campgrounds = self._get_searchable_campgrounds()
        this_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        for month in self.search_months:
            if month >= this_month:
                all_campsites += self.campsite_finder.get_monthly_campsites(month=month)
        matching_campsites = self._filter_campsites_to_campgrounds(
            campsites=all_campsites, searchable_campgrounds=searchable_campgrounds)
        return matching_campsites

    def _get_searchable_campgrounds(self) -> Set[str]:
        """
        Return the Campgrounds for the Camping Search

        Returns
        -------

        """
        supported_campsites = set(YellowstoneConfig.CAMPGROUNDS.keys())
        selected_campsites = set(self.campgrounds)
        searchable_campgrounds = supported_campsites.intersection(selected_campsites)
        if len(searchable_campgrounds) == 0:
            campground_ids = [f"`{key}` ({value})" for key, value in
                              YellowstoneConfig.CAMPGROUNDS.items()]
            error_message = ("You must supply a YellowstoneNationalParkLodges supported "
                             "campground ID. Current supported Campground IDs: "
                             f"{', '.join(campground_ids)}")

            logger.error(error_message)
            raise SearchError(error_message)
        logger.info(f"{len(searchable_campgrounds)} Matching Campgrounds Found")
        for campground in searchable_campgrounds:
            logger.info(f"⛰  Yellowstone National Park, USA (#1) - 🏕  "
                        f"{YellowstoneConfig.CAMPGROUNDS[campground]} ({campground})")
        return searchable_campgrounds

    def _filter_campsites_to_campgrounds(
            self, campsites: List[AvailableCampsite],
            searchable_campgrounds: Set[str]) -> List[AvailableCampsite]:
        """
        Filter Campsites Down to Matching Campgrounds

        Parameters
        ----------
        campsites: List[AvailableCampsite]
        searchable_campgrounds: Set[str]

        Returns
        -------
        List[AvailableCampsite]
        """
        if self.campgrounds is None:
            return campsites
        matching_campsites = [campsite for campsite in campsites if
                              campsite.facility_id in searchable_campgrounds]
        return matching_campsites
