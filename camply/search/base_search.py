#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Searching Utilities
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import logging
from os import getenv
from time import sleep
from typing import List, Optional, Set, Union

from pandas import DataFrame
import tenacity

from camply.config import DataColumns, SearchConfig
from camply.containers import AvailableCampsite, CampgroundFacility, RecreationArea, SearchWindow
from camply.notifications import CAMPSITE_NOTIFICATIONS, SilentNotifications
from camply.providers import RecreationDotGov, YellowstoneLodging
from camply.utils.logging_utils import get_emoji

logger = logging.getLogger(__name__)


class SearchError(Exception):
    """
    Generic Search Error
    """


class CampsiteNotFound(SearchError):
    """
    Campsite not found Error
    """


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
        provider: Union[RecreationDotGov, YellowstoneLodging]
            API Provider
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
        """
        self.campsite_finder: Union[RecreationDotGov, YellowstoneLodging] = provider
        # noinspection PyTypeChecker
        self.search_window: List[SearchWindow] = self._make_list(search_window)
        self.weekends_only: bool = weekends_only
        self.search_days: List[datetime] = self._get_search_days()
        self.search_months: List[datetime] = self._get_search_months()
        self.campsites_found: Set[AvailableCampsite] = set()

    @abstractmethod
    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities. This method must be implemented
        on all sub-classes.

        Returns
        -------
        List[AvailableCampsite]
        """

    def _search_matching_campsites_available(self, log: bool = False,
                                             verbose: bool = False,
                                             raise_error: bool = False) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities

        Parameters
        ----------
        log: bool
            Whether to log found campsites
        verbose: bool
            Used with `log` to enhance the amount of info logged to the console
        raise_error: bool
            Whether to raise an error if nothing is found. Defaults to False.

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

    @classmethod
    def _get_polling_minutes(cls, polling_interval: Optional[int]) -> int:
        """
        Return the Nu,ber of Minutes to Search

        Parameters
        ----------
        polling_interval: Optional[int]
            Used with `continuous=True`, the amount of time to wait between searches.
            Defaults to 10 if not provided, cannot be less than 5

        Returns
        -------
        int
        """
        if polling_interval is None:
            polling_interval = getenv("POLLING_INTERVAL", SearchConfig.RECOMMENDED_POLLING_INTERVAL)
        if int(polling_interval) < SearchConfig.POLLING_INTERVAL_MINIMUM:
            polling_interval = SearchConfig.POLLING_INTERVAL_MINIMUM
        polling_interval_minutes = int(round(float(polling_interval), 2))
        return polling_interval_minutes

    def _continuous_search_retry(self, log: bool, verbose: bool, polling_interval: int,
                                 continuous_search_attempts: int,
                                 notification_provider: str,
                                 notify_first_try: bool) -> List[AvailableCampsite]:
        """
        Search for Campsites until at least one is found

        Parameters
        ----------
        log: bool
            Whether to log found campsites
        verbose: bool
            Used with `log` to enhance the amount of info logged to the console
        polling_interval: Optional[int]
            Used with `continuous=True`, the amount of time to wait between searches.
            Defaults to 10 if not provided, cannot be less than 5
        continuous_search_attempts: int
            Number of preexisting search attempts
        notification_provider: str
            Used with `continuous=True`, Name of notification provider to use. Accepts "email",
            "pushover", and defaults to "silent"
        notify_first_try: bool
            Used with `continuous=True`, whether to send all non-silent notifications if more
            than 5 matching campsites are found on the first try. Defaults to false which
            only sends the first 5.

        Returns
        -------
        List[AvailableCampsite]
        """
        polling_interval_minutes = self._get_polling_minutes(polling_interval=polling_interval)
        notifier = CAMPSITE_NOTIFICATIONS.get(notification_provider.lower(),
                                              SilentNotifications)()
        logger.info(f"Searching for campsites every {polling_interval_minutes} minutes. "
                    f"Notifications active via {notifier}")
        retryer = tenacity.Retrying(
            retry=tenacity.retry_if_exception_type(CampsiteNotFound),
            wait=tenacity.wait.wait_fixed(int(polling_interval_minutes) * 60))
        matching_campsites = retryer.__call__(self._search_matching_campsites_available,
                                              False, False, True)
        found_campsites = set(matching_campsites)
        new_campsites = found_campsites.difference(self.campsites_found)
        self.assemble_availabilities(matching_data=list(new_campsites), log=log,
                                     verbose=verbose)
        logger.info(f"{len(new_campsites)} New Campsites Found.")
        self.campsites_found.update(new_campsites)
        logged_campsites = list(new_campsites)
        if max([retryer.statistics.get("attempt_number", 1), continuous_search_attempts]) > 1:
            notifier.send_campsites(campsites=logged_campsites)
        elif retryer.statistics.get("attempt_number", 1) == 1 and notify_first_try is True:
            notifier.send_campsites(campsites=logged_campsites)
        else:
            if not isinstance(notifier, SilentNotifications) and \
                    len(logged_campsites) > SearchConfig.MINIMUM_CAMPSITES_FIRST_NOTIFY:
                error_message = (f"Found more than {SearchConfig.MINIMUM_CAMPSITES_FIRST_NOTIFY} "
                                 f"matching campsites ({len(logged_campsites)}) on the "
                                 "first try. Try searching online instead. "
                                 f"camply is only sending the first "
                                 f"{SearchConfig.MINIMUM_CAMPSITES_FIRST_NOTIFY} notifications. "
                                 "Go Get your campsite! 🏕")
                logger.warning(error_message)
                notifier.send_message(message=error_message)
                logged_campsites = logged_campsites[:SearchConfig.MINIMUM_CAMPSITES_FIRST_NOTIFY]
            notifier.send_campsites(campsites=logged_campsites)
        return list(self.campsites_found)

    def _search_campsites_continuous(self, log: bool = True, verbose: bool = False,
                                     polling_interval: Optional[int] = None,
                                     notification_provider: str = "silent",
                                     notify_first_try: bool = False,
                                     search_forever: bool = False):
        """
        Continuously Search For Campsites

        Parameters
        ----------
        log: bool
            Whether to log found campsites
        verbose: bool
            Used with `log` to enhance the amount of info logged to the console
        polling_interval: Optional[int]
            Used with `continuous=True`, the amount of time to wait between searches.
            Defaults to 10 if not provided, cannot be less than 5
        notification_provider: str
            Used with `continuous=True`, Name of notification provider to use. Accepts "email",
            "pushover", and defaults to "silent"
        notify_first_try: bool
            Used with `continuous=True`, whether to send all non-silent notifications if more
            than 5 matching campsites are found on the first try. Defaults to false which
            only sends the first 5.
        search_forever: bool
            Used with `continuous=True`, This option searches for new campsites forever, with
            the caveat being that it will never notify about the same campsite.

        Returns
        -------
        List[AvailableCampsite]
        """
        polling_interval_minutes = self._get_polling_minutes(polling_interval=polling_interval)
        continuous_search = True
        continuous_search_attempts = 1
        while continuous_search is True:
            self._continuous_search_retry(log=log, verbose=verbose,
                                          polling_interval=polling_interval,
                                          notification_provider=notification_provider,
                                          notify_first_try=notify_first_try,
                                          continuous_search_attempts=continuous_search_attempts)
            continuous_search_attempts += 1
            if search_forever is True:
                sleep(int(polling_interval_minutes) * 60)
            else:
                continuous_search = False
        return list(self.campsites_found)

    def get_matching_campsites(self, log: bool = True, verbose: bool = False,
                               continuous: bool = False,
                               polling_interval: Optional[int] = None,
                               notification_provider: str = "silent",
                               notify_first_try: bool = False,
                               search_forever: bool = False) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities

        Parameters
        ----------
        log: bool
            Whether to log found campsites
        verbose: bool
            Used with `log` to enhance the amount of info logged to the console
        continuous: bool
            Whether to continue searching beyond just the first time
        polling_interval: Optional[int]
            Used with `continuous=True`, the amount of time to wait between searches.
            Defaults to 10 if not provided, cannot be less than 5
        notification_provider: str
            Used with `continuous=True`, Name of notification provider to use. Accepts "email",
            "pushover", and defaults to "silent"
        notify_first_try: bool
            Used with `continuous=True`, whether to send all non-silent notifications if more
            than 5 matching campsites are found on the first try. Defaults to false which
            only sends the first 5.
        search_forever: bool
            Used with `continuous=True`, This option searches for new campsites forever, with
            the caveat being that it will never notify about the same campsite.

        Returns
        -------
        List[AvailableCampsite]
        """
        if continuous is True:
            self._search_campsites_continuous(log=log, verbose=verbose,
                                              polling_interval=polling_interval,
                                              notification_provider=notification_provider,
                                              notify_first_try=notify_first_try,
                                              search_forever=search_forever)
        else:
            matching_campsites = self._search_matching_campsites_available(log=log, verbose=True)
            self.campsites_found.update(set(matching_campsites))
        return list(self.campsites_found)

    def _get_search_days(self) -> List[datetime]:
        """
        Retrieve Specific Days to Search For

        Returns
        -------
        search_days: List[datetime]
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
            logger.info("Limiting Search of Campgrounds to Weekend Availabilities")
            for search_date in list(search_days):
                if search_date.weekday() not in [4, 5]:
                    search_days.remove(search_date)
        number_searches = len(search_days)
        if number_searches > 0:
            logger.info(f"{len(search_days)} dates selected for search, "
                        f"ranging from {min(search_days).strftime('%Y-%m-%d')} to "
                        f"{max(search_days).strftime('%Y-%m-%d')}")
        else:
            logger.info(SearchConfig.ERROR_MESSAGE)
            raise RuntimeError(SearchConfig.ERROR_MESSAGE)
        return list(sorted(search_days))

    def _get_search_months(self) -> List[datetime]:
        """
        Get the Unique Months that need to be Searched

        Returns
        -------
        search_months: List[datetime]
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
            logger.info(SearchConfig.ERROR_MESSAGE)
            raise RuntimeError(SearchConfig.ERROR_MESSAGE)
        else:
            return sorted(list(truncated_months))

    @classmethod
    def assemble_availabilities(cls, matching_data: List[AvailableCampsite], log: bool = True,
                                verbose: bool = False) -> DataFrame:
        """
        Prepare a Pandas DataFrame from Array of AvailableCampsite objects

        Parameters
        ----------
        matching_data: List[AvailableCampsite]
            List of campsites to assemble
        log: bool
            Whether to log found campsites
        verbose: bool
            Used with `log` to enhance the amount of info logged to the console

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

    @classmethod
    def _make_list(cls, obj) -> Optional[List]:
        """
        Make Anything An Iterable Instance

        Parameters
        ----------
        obj: object

        Returns
        -------
        List[object]
        """
        if obj is None:
            return None
        elif isinstance(obj, (SearchWindow, AvailableCampsite, RecreationArea, CampgroundFacility)):
            return [obj]
        elif isinstance(obj, (set, list, tuple)):
            return obj
        else:
            return [obj]
