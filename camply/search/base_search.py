#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Searching Utilities
"""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from itertools import groupby, islice, tee
import logging
from operator import itemgetter
from os import getenv
from time import sleep
from typing import Generator, Iterable, List, Optional, Set, Union

from pandas import concat, DataFrame, date_range, Series, Timedelta
import tenacity

from camply.config import CampsiteContainerFields, DataColumns, SearchConfig
from camply.containers import (AvailableCampsite, CampgroundFacility, RecreationArea,
                               SearchWindow)
from camply.notifications.base_notifications import BaseNotifications
from camply.notifications.multi_provider_notifications import MultiNotifierProvider
from camply.providers import RecreationDotGov, YellowstoneLodging
from camply.utils.logging_utils import get_emoji

logger = logging.getLogger(__name__)


class SearchError(Exception):
    """
    Generic Search Error
    """


class CampsiteNotFoundError(SearchError):
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
                 weekends_only: bool = False,
                 nights: int = 1) -> None:
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
        nights: int
            minimum number of consecutive nights to search per campsite,defaults to 1
        """
        self.campsite_finder: Union[RecreationDotGov, YellowstoneLodging] = provider
        # noinspection PyTypeChecker
        self.search_window: List[SearchWindow] = self._make_list(search_window)
        self.weekends_only: bool = weekends_only
        self.search_days: List[datetime] = self._get_search_days()
        self.search_months: List[datetime] = self._get_search_months()
        self.nights = self._validate_consecutive_nights(nights=nights)
        self.campsites_found: Set[AvailableCampsite] = set()

    @abstractmethod
    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return Matching Availabilities.

        This method must be implemented
        on all sub-classes.

        Returns
        -------
        List[AvailableCampsite]
        """

    def _get_intersection_date_overlap(self, date: datetime, periods: int) -> bool:
        """
        Find Date Overlap

        Parameters
        ----------
        date: datetime
        periods: int

        Returns
        -------
        bool
        """
        campsite_date_range = set(date_range(start=date.to_pydatetime(),
                                             periods=periods))
        intersection = campsite_date_range.intersection(self.search_days)
        if intersection:
            return True
        else:
            return False

    def _compare_date_overlap(self, campsite: AvailableCampsite) -> bool:
        """
        See whether a campsite should be returned as found

        Parameters
        ----------
        campsite: AvailableCampsite

        Returns
        -------
        bool
        """
        intersection = self._get_intersection_date_overlap(date=campsite.booking_date,
                                                           periods=campsite.booking_nights)
        return intersection

    def _filter_date_overlap(self, campsites: DataFrame) -> bool:
        """
        See whether a campsite should be returned as found

        Parameters
        ----------
        campsites: DataFrame

        Returns
        -------
        DataFrame
        """
        filtered_campsites = campsites[campsites.apply(
            lambda x: self._get_intersection_date_overlap(date=x.booking_date,
                                                          periods=x.booking_nights),
            axis=1)].copy().reset_index(drop=True)
        return filtered_campsites

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
            if all([self._compare_date_overlap(campsite=camp) is True,
                    camp.booking_nights >= self.nights]):
                matching_campgrounds.append(camp)
        logger.info(f"{(get_emoji(matching_campgrounds) + ' ') * 4}{len(matching_campgrounds)} "
                    "Reservable Campsites Matching Search Preferences")
        self.assemble_availabilities(matching_data=matching_campgrounds,
                                     log=log, verbose=verbose)
        if len(matching_campgrounds) == 0 and raise_error is True:
            campsite_availability_message = "No Campsites were found, we'll continue checking"
            logger.info(campsite_availability_message)
            raise CampsiteNotFoundError(campsite_availability_message)
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

    def _continuous_search_retry(
            self, log: bool, verbose: bool, polling_interval: int,
            continuous_search_attempts: int,
            notification_provider: Union[str, List[str], BaseNotifications, None],
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
        notification_provider: provider: Union[str, List[str]]
            Used with `continuous=True`, Name of notification provider to use. Accepts
            "email", "pushover", and defaults to "silent". Also accepts a list or commma
            separated string of these options or even a notification provider object itself
        notify_first_try: bool
            Used with `continuous=True`, whether to send all non-silent notifications if more
            than 5 matching campsites are found on the first try. Defaults to false which
            only sends the first 5.

        Returns
        -------
        List[AvailableCampsite]
        """
        polling_interval_minutes = self._get_polling_minutes(polling_interval=polling_interval)
        notifier = MultiNotifierProvider(provider=notification_provider)
        logger.info(f"Searching for campsites every {polling_interval_minutes} minutes. ")
        notifier.log_providers()
        retryer = tenacity.Retrying(
            retry=tenacity.retry_if_exception_type(CampsiteNotFoundError),
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
        self._handle_notifications(retryer=retryer, notifier=notifier,
                                   logged_campsites=logged_campsites,
                                   continuous_search_attempts=continuous_search_attempts,
                                   notify_first_try=notify_first_try)
        return list(self.campsites_found)

    @classmethod
    def _handle_notifications(cls,
                              retryer: tenacity.Retrying,
                              notifier: MultiNotifierProvider,
                              logged_campsites: List[AvailableCampsite],
                              continuous_search_attempts: int,
                              notify_first_try: bool,
                              ) -> None:
        """
        Handle sending notifications

        Parameters
        ----------
        retryer: tenacity.Retrying
        notifier: MultiNotifierProvider
        logged_campsites: List[AvailableCampsite]
        continuous_search_attempts: int
        notify_first_try: bool

        Returns
        -------
        None
        """
        attempt_number = retryer.statistics.get("attempt_number", 1)
        minimum_first_notify = SearchConfig.MINIMUM_CAMPSITES_FIRST_NOTIFY
        if max([attempt_number, continuous_search_attempts]) > 1:
            logged_campsites = cls._handle_too_many_campsites_found(
                notifier=notifier,
                logged_campsites=logged_campsites)
            notifier.send_campsites(campsites=logged_campsites)
        elif attempt_number == 1 and notify_first_try is True:
            logged_campsites = cls._handle_too_many_campsites_found(
                notifier=notifier,
                logged_campsites=logged_campsites)
            notifier.send_campsites(campsites=logged_campsites)
        else:
            if len(notifier.providers) > 1 and \
                    len(logged_campsites) > minimum_first_notify:
                error_message = (f"Found more than {minimum_first_notify} "
                                 f"matching campsites ({len(logged_campsites)}) on the "
                                 "first try. Try searching online instead. "
                                 f"camply is only sending the first "
                                 f"{minimum_first_notify} notifications. "
                                 "Go Get your campsite! 🏕")
                logger.warning(error_message)
                notifier.send_message(message=error_message)
                logged_campsites = logged_campsites[:minimum_first_notify]
            notifier.send_campsites(campsites=logged_campsites)

    @classmethod
    def _handle_too_many_campsites_found(
            cls, notifier: MultiNotifierProvider,
            logged_campsites: List[AvailableCampsite]) -> List[AvailableCampsite]:
        """
        Handle Scenarios Where Too Many Campsites are Found

        Parameters
        ----------
        notifier: MultiNotifierProvider
        logged_campsites: List[AvailableCampsite]

        Returns
        -------
        List[AvailableCampsite]
        """
        limit = SearchConfig.MAXIMUM_NOTIFICATION_BATCH_SIZE
        number_campsites = len(logged_campsites)
        if number_campsites > limit:
            warning_message = (
                f"Too many campsites were found during the search ({number_campsites} "
                f"total). camply will only send you the first {limit} notifications."
            )
            logger.warning(warning_message)
            restricted_campsites = logged_campsites[:limit]
            notifier.send_message(warning_message)
        else:
            restricted_campsites = logged_campsites
        return restricted_campsites

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
            Used with `continuous=True`, Name of notification provider to use. Accepts
            "email", "pushover", and defaults to "silent". Also accepts a list or commma
            separated string of these options or even a notification provider object itself
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
            Used with `continuous=True`, Name of notification provider to use. Accepts
            "email", "pushover", and defaults to "silent". Also accepts a list or commma
            separated string of these options or even a notification provider object itself
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
            for index in range(0, (window.end_date - window.start_date).days):
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
            logger.info(f"{len(search_days)} booking nights selected for search, "
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
    def _consolidate_campsites(cls, campsite_df: DataFrame,
                               nights: int) -> List[AvailableCampsite]:
        """
        Consolidate Single Night Campsites into Multiple Night Campsites

        Parameters
        ----------
        campsite_df: DataFrame
            DataFrame of AvailableCampsites

        Returns
        -------
        List[AvailableCampsite]
        """
        composed_groupings = list()
        for _, campsite_slice in campsite_df.groupby(
                [CampsiteContainerFields.CAMPSITE_ID, CampsiteContainerFields.CAMPGROUND_ID]):
            # SORT THE VALUES AND CREATE A COPIED SLICE
            campsite_grouping = campsite_slice.sort_values(by=CampsiteContainerFields.BOOKING_DATE,
                                                           ascending=True).copy()
            # ASSEMBLE THE CAMPSITES AVAILABILITIES INTO GROUPS THAT ARE CONSECUTIVE
            booking_date = campsite_grouping[CampsiteContainerFields.BOOKING_DATE]
            date = Timedelta('1d')
            consecutive_nights = booking_date.diff() != date
            group_identifier = consecutive_nights.cumsum()
            campsite_grouping[CampsiteContainerFields.CAMPSITE_GROUP] = group_identifier
            # USE THE ASSEMBLED GROUPS TO CREATE UPDATED CAMPSITES AND REMOVE DUPLICATES
            for _campsite_group, campsite_group_slice in campsite_grouping.groupby(
                    [CampsiteContainerFields.CAMPSITE_GROUP]):
                composed_grouping = campsite_group_slice.sort_values(
                    by=CampsiteContainerFields.BOOKING_DATE,
                    ascending=True).copy()
                composed_grouping.drop(columns=[CampsiteContainerFields.CAMPSITE_GROUP],
                                       inplace=True)
                nightly_breakouts = cls._find_consecutive_nights(dataframe=composed_grouping,
                                                                 nights=nights)
                composed_groupings.append(nightly_breakouts)
        if len(composed_groupings) == 0:
            composed_groupings = [DataFrame()]
        return concat(composed_groupings, ignore_index=True)

    @classmethod
    def _consecutive_subseq(cls, iterable: Iterable, length: int) -> Generator:
        """
        Find All Sub Sequences by length Given a List

        Parameters
        ----------
        iterable: Iterable
        length: int

        Returns
        -------
        Generator
        """
        for _, consec_run in groupby(enumerate(iterable), lambda x: x[0] - x[1]):
            k_wise = tee(map(itemgetter(1), consec_run), length)
            for n, it in enumerate(k_wise):
                next(islice(it, n, n), None)
            yield from zip(*k_wise)

    @classmethod
    def _find_consecutive_nights(cls, dataframe: DataFrame, nights: int) -> DataFrame:
        """
        Explode a DataFrame of Consecutive Nightly Campsite Availabilities,

        Expand to all unique possibilities given the length of the stay.

        Parameters
        ----------
        dataframe: DataFrame
        nights: int

        Returns
        -------
        DataFrame
        """
        dataframe_slice = dataframe.copy().reset_index(drop=True)
        nights_indexes = dataframe_slice.booking_date.index
        consecutive_generator = cls._consecutive_subseq(iterable=nights_indexes, length=nights)
        sequences = list(consecutive_generator)
        concatted_data = list()
        for sequence in sequences:
            index_list = list(sequence)
            data_copy = dataframe_slice.iloc[index_list].copy()
            data_copy.booking_date = data_copy.booking_date.min()
            data_copy.booking_end_date = data_copy.booking_end_date.max()
            data_copy.booking_url = data_copy.booking_url.loc[index_list[0]]
            data_copy.booking_nights = (data_copy.booking_end_date - data_copy.booking_date).dt.days
            data_copy.drop_duplicates(inplace=True)
            concatted_data.append(data_copy)
        if len(concatted_data) == 0:
            concatted_data = [DataFrame()]
        return concat(concatted_data, ignore_index=True)

    def _validate_consecutive_nights(self, nights: int) -> int:
        """
        Validate the number of consecutive nights to search

        Parameters
        ----------
        nights : int
            Number of nights to check

        Returns
        -------
        int
            The proper number of nights to search
        """
        search_days = Series(self.search_days)
        consecutive_nights = search_days.diff() != Timedelta('1d')
        largest_grouping = consecutive_nights.cumsum().value_counts().max()
        if nights > 1:
            logger.info(f"Searching for availabilities with {nights} consecutive night stays.")
        if nights > largest_grouping:
            logger.warning("Too many consecutive nights selected. "
                           "The consecutive night parameter will be set to "
                           f"the max possible, {largest_grouping}.")
            return largest_grouping
        else:
            return nights

    @staticmethod
    def campsites_to_df(campsites: List[AvailableCampsite]) -> DataFrame:
        """
        Convert Campsite Array to

        Parameters
        ----------
        campsites: List[AvailableCampsite]

        Returns
        -------
        DataFrame
        """
        campsite_df = DataFrame(data=[campsite.__dict__ for campsite in campsites],
                                columns=AvailableCampsite.__fields__)
        return campsite_df

    @staticmethod
    def df_to_campsites(campsite_df: DataFrame) -> List[AvailableCampsite]:
        """
        Convert Campsite DataFrame to array of AvailableCampsite objects

        Parameters
        ----------
        campsite_df: DataFrame

        Returns
        -------
        List[AvailableCampsite]
        """
        composed_campsite_array = list()
        composed_campsite_data_array = campsite_df.to_dict(orient="records")
        for campsite_record in composed_campsite_data_array:
            composed_campsite_array.append(AvailableCampsite(**campsite_record))
        return composed_campsite_array

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
        availability_df = cls.campsites_to_df(campsites=matching_data)
        if log is True:
            cls._log_availabilities(availability_df=availability_df, verbose=verbose)
        return availability_df

    @classmethod
    def _log_availabilities(cls, availability_df: DataFrame, verbose: bool) -> DataFrame:
        """
        Log the Availabilities

        Parameters
        ----------
        availability_df: DataFrame
        verbose: bool

        Returns
        -------
        DataFrame
        """
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
                    for booking_nights, nightly_availability in campground_availability.groupby(
                            [DataColumns.BOOKING_NIGHTS_COLUMN]):
                        unique_urls = nightly_availability[DataColumns.BOOKING_URL_COLUMN].unique()
                        for booking_url in sorted(unique_urls):
                            logger.info(f"\t\t🔗 {booking_url} "
                                        f"({booking_nights} night"
                                        f"{'s' if booking_nights > 1 else ''})")
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
