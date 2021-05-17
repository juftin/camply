#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Yellowstone Lodging Web Searching Utilities
"""

from datetime import datetime
import logging
from typing import List, Union

from camply.containers import AvailableCampsite, SearchWindow
from camply.providers import YellowstoneLodging
from camply.search.base_search import BaseCampingSearch

logger = logging.getLogger(__name__)


class SearchYellowstone(BaseCampingSearch):
    """
    Camping Search Object
    """

    # noinspection PyUnusedLocal
    def __init__(self, search_window: Union[SearchWindow, List[SearchWindow]],
                 weekends_only: bool = False,
                 **kwargs) -> None:
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
        super().__init__(provider=YellowstoneLodging(),
                         search_window=search_window,
                         weekends_only=weekends_only)

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Search for all matching campsites in Yellowstone.

        Returns
        -------
        List[AvailableCampsite]
        """
        all_campsites = list()
        this_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        for month in self.search_months:
            if month >= this_month:
                all_campsites += self.campsite_finder.get_monthly_campsites(month=month)
        return all_campsites
