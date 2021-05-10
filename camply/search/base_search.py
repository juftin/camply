#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Scraping Utilities
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import logging
from os import getenv
from typing import List, Optional, Set, Union

from pandas import DataFrame
import tenacity

from camply.config import DataColumns, SearchConfig
from camply.containers import AvailableCampsite, SearchWindow
from camply.notifications import CAMPSITE_NOTIFICATIONS, SilentNotifications
from camply.providers import RecreationDotGov, YellowstoneLodging
from camply.providers.base_provider import BaseProvider
from camply.utils import make_list
from camply.utils.logging_utils import get_emoji

logger = logging.getLogger(__name__)


class SearchError(Exception):
    """
    Generic Search Error
    """
    pass


class CampsiteNotFound(SearchError):
    """
    Campsite not found Error
    """
    pass


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
        self.campsite_finder: Union[RecreationDotGov, YellowstoneLodging] = provider
        # noinspection PyTypeChecker
        self.search_window: List[SearchWindow] = make_list(search_window)
        self.weekends_only: bool = weekends_only
        self.search_days = self._get_search_days()
        self.search_months = self._get_search_months()

    @abstractmethod
    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities. This method must be implemented
        on all sub-classes.

        Returns
        -------
        List[AvailableCampsite]
        """
        pass

    def _search_matching_campsites_available(self, log: bool = False,
                                             verbose: bool = False,
                                             raise_error: bool = False) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        matching_campgrounds = list()
        for camp in self.get_all_campsites():
            if camp.booking_date in self.search_days:
                matching_campgrounds.append(camp)
        logger.info(f"{(get_emoji(matching_campgrounds) + ' ') * 4}{len(matching_campgrounds)} "
                    "Reservable Campsites Matching Search Preferences")
        self.assemble_availabilities(matching_data=matching_campgrounds,
                                     log=log, verbose=verbose)
        if len(matching_campgrounds) == 0 and raise_error is True:
            campsite_availability_message = "No Campsites were found, we'll continue checking"
            logger.info(campsite_availability_message)
            raise CampsiteNotFound(campsite_availability_message)
        return matching_campgrounds

    def get_matching_campsites(self, log: bool = True, verbose: bool = False,
                               continuous: bool = False,
                               polling_interval: Optional[int] = None,
                               notify_first_try: bool = False,
                               notification_provider: Union["pushover", "email"] = "silent") -> \
            List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        if polling_interval is None:
            polling_interval = getenv("POLLING_INTERVAL", SearchConfig.RECOMMENDED_POLLING_INTERVAL)
        if int(polling_interval) < SearchConfig.POLLING_INTERVAL_MINIMUM:
            polling_interval = SearchConfig.POLLING_INTERVAL_MINIMUM
        polling_interval_minutes = int(round(float(polling_interval), 2))

        if continuous is True:
            notifier = CAMPSITE_NOTIFICATIONS.get(notification_provider.lower(),
                                                  SilentNotifications)()
            logger.info(f"Searching for campsites every {polling_interval_minutes} minutes. "
                        f"Notifications active via {notifier}")
            retryer = tenacity.Retrying(
                retry=tenacity.retry_if_exception_type(CampsiteNotFound),
                wait=tenacity.wait.wait_fixed(int(polling_interval_minutes) * 60))
            matching_campsites = retryer.__call__(self._search_matching_campsites_available, log,
                                                  verbose, True)
            if retryer.statistics.get("attempt_number", 1) > 1:
                notifier.send_campsites(campsites=matching_campsites)
            elif retryer.statistics.get("attempt_number", 1) == 1 and notify_first_try is True:
                notifier.send_campsites(campsites=matching_campsites)
            else:
                logger.warning(f"Found matching campsites on the first try! "
                               "Switching to Silent Notifications. Go Get your campsite! 🏕")
                silent_notifier = SilentNotifications()
                silent_notifier.send_campsites(campsites=matching_campsites)
        else:
            matching_campsites = self._search_matching_campsites_available(log=log, verbose=True)
        return matching_campsites

    def _get_search_days(self) -> List[datetime]:
        """
        Retrieve Specific Days to Search For

        Returns
        -------
        search_days: Set[datetime]
            Datetime days to search for reservations
        """
        now = datetime.now()
        current_date = datetime(year=now.year, month=now.month, day=now.day)
        search_days = set()
        for window in self.search_window:
            generated_dates = set()
            for index in range(0, (window.end_date - window.start_date).days + 1):
                search_day = window.start_date
                search_day = search_day.replace(hour=0, minute=0, second=0,
                                                microsecond=0) + timedelta(days=index)
                if search_day >= current_date:
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
    def assemble_availabilities(cls, matching_data, log: bool = True,
                                verbose: bool = False) -> DataFrame:
        """
        Prepare a Pandas DataFrame from Array of AvailableCampsite objects

        Returns
        -------
        availability_df: DataFrame
        """
        availability_df = DataFrame(data=matching_data, columns=AvailableCampsite._fields)
        if log is True:
            booking_date: datetime
            for booking_date, available_sites in availability_df.groupby("booking_date"):
                logger.info(f"📅 {booking_date.strftime('%a, %B %d')} "
                            f"🏕  {len(available_sites)} sites")
                location_tuple: tuple
                for location_tuple, campground_availability in \
                        available_sites.groupby([DataColumns.RECREATION_AREA_COLUMN,
                                                 DataColumns.FACILITY_NAME_COLUMN]):
                    logger.info(f"\t⛰️  {'  🏕  '.join(location_tuple)}: ⛺ "
                                f"{len(campground_availability)} sites")
                    if verbose is True:
                        for booking_url in campground_availability[
                            DataColumns.BOOKING_URL_COLUMN
                        ].unique():
                            logger.info(f"\t\t🔗 {booking_url}")
        return availability_df
