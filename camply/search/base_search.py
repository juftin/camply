#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Scraping Utilities
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import logging
from typing import List, Set, Union

from pandas import DataFrame

from camply.containers import AvailableCampsite, SearchWindow
from camply.providers import RecreationDotGov, YellowstoneLodging
from camply.providers.base_provider import BaseProvider
from camply.utils import make_list

logger = logging.getLogger(__name__)


class BaseCampingSearch(ABC):
    """
    Camping Search Object
    """

    def __init__(self, provider: Union[RecreationDotGov,
                                       YellowstoneLodging],
                 search_window: Union[SearchWindow, List[SearchWindow]],
                 weekends_only: bool = False) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        provider: BaseProvider
            API Provider
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
        """
        self.campsite_finder: BaseProvider = provider
        self.search_window: List[SearchWindow] = make_list(search_window)
        self.weekends_only: bool = weekends_only
        self.search_days: List[datetime] = self._get_search_days()
        self.search_months = self._get_search_months()

    @abstractmethod
    def search_matching_campsites_available(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities. This method must be implemented
        on all sub-classes.

        Returns
        -------
        List[AvailableCampsite]
        """
        pass

    def _get_search_days(self) -> List[datetime]:
        """
        Retrieve Specific Days to Search For

        Returns
        -------
        search_days: Set[datetime]
            Datetime days to search for reservations
        """
        search_days = set()
        for window in self.search_window:
            generated_dates = set()
            for index in range(0, (window.end_date - window.start_date).days + 1):
                search_day = window.start_date.replace(hour=0, minute=0, second=0,
                                                       microsecond=0) + timedelta(days=index)
                generated_dates.add(search_day)
            search_days.update(generated_dates)

        if self.weekends_only is True:
            logger.info(f"Limiting Search of Campgrounds to Weekend Availabilities")
            for search_date in list(search_days):
                if search_date.weekday() not in [4, 5]:
                    search_days.remove(search_date)
        number_searches = len(search_days)
        if number_searches > 0:
            logger.info(f"{len(search_days)} dates selected for search, "
                        f"ranging from {min(search_days).strftime('%Y-%m-%d')} to "
                        f"{max(search_days).strftime('%Y-%m-%d')}")
        else:
            logger.info(f"No search days configured. Exiting")
            raise RuntimeError("No search days configured. Exiting")
        return list(sorted(search_days))

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

    @classmethod
    def _assemble_availabilities(cls, matching_data, log: bool = True,
                                 verbose: bool = False) -> DataFrame:
        """
        Prepare a Pandas DataFrame from Array of AvailableCampsite objects

        Returns
        -------
        availability_df: DataFrame
        """
        availability_df = DataFrame(data=matching_data, columns=AvailableCampsite._fields)
        if log is True:
            for booking_date, available_sites in availability_df.groupby("booking_date"):
                logger.info(f"📅 {booking_date.strftime('%a, %B %d')} "
                            f"🏕 {len(available_sites)} sites")
                for location_tuple, campground_availability in \
                        available_sites.groupby(["recreation_area", "facility_name"]):
                    logger.info(f"\t⛰️  {'  🏕  '.join(location_tuple)}: ⛺ "
                                f"{len(campground_availability)} sites")
                    if verbose is True:
                        for _, row in campground_availability.iterrows():
                            logger.info(f"\t\t🔗 {row['booking_url']}")
        return availability_df
