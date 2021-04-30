#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Yellowstone Lodging Web Scraping Utilities
"""

import logging
from typing import List, Optional, Union

from camply.containers import AvailableCampsite, SearchWindow
from camply.providers import YellowstoneLodging
from camply.search.base_search import BaseCampingSearch

logger = logging.getLogger(__name__)


class SearchYellowstone(BaseCampingSearch):
    """
    Camping Search Object
    """

    def __init__(self, search_window: Union[SearchWindow, List[SearchWindow]],
                 campgrounds: Optional[Union[List[str], str]] = None,
                 weekends_only: bool = False) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        campgrounds: Optional[Union[List[int], int]]
            Campground ID or List of Campground IDs
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
        """
        super(SearchYellowstone, self).__init__(provider=YellowstoneLodging(),
                                                search_window=search_window,
                                                weekends_only=weekends_only)
        self._campground_object = campgrounds
        self.weekends_only = weekends_only

    def search_matching_campsites_available(self, log: bool = False,
                                            verbose: bool = False) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        campsite_finder = YellowstoneLodging(booking_start=self.search_window.start_date,
                                             number_of_guests=1,  # SET THE MINIMUM FOR NOW
                                             number_of_nights=1,  # SET THE MINIMUM FOR NOW
                                             polling_interval=600)
        campsite_finder.continuously_check_for_availability()
        availability_found = self.check_yellowstone_lodging()
        for hotel_code, lodging_found in availability_found.items():
            logger.info(hotel_code, lodging_found)
