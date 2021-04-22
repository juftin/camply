#!/usr/bin/env python3

# Author::    Justin Flannery  (mailto:juftin@juftin.com)

"""
Recreation.gov Web Scraping Utilities
"""

from datetime import datetime, timedelta
import logging
from time import sleep
from typing import List, Optional, Set, Union

from pandas import DataFrame

from camply.containers import AvailableCampsite, SearchWindow
from camply.utils.logging_utils import get_emoji

logger = logging.getLogger(__name__)


class Provider(object):
    pass


class CampingSearch(object):
    """
    Camping Search Object
    """

    def __init__(self, provider: Provider, search_window: Union[SearchWindow, List[SearchWindow]],
                 recreation_area: Optional[int] = None,
                 campgrounds: Optional[Union[List[int], int]] = None,
                 weekends_only: bool = False) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        provider: Provider
            Campground API BaseProvider (i.e RecreationDotGov)
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
        if isinstance(search_window, SearchWindow):
            self.search_window = [search_window]
        elif isinstance(search_window, list):
            for window in search_window:
                assert isinstance(window, SearchWindow) is True
            self.search_window = search_window
        else:
            raise NotImplementedError("Pass a proper SearchWindow")

        self._recreation_area_id = recreation_area
        self._campground_object = campgrounds
        self.campsite_finder = provider
        self.weekends_only = weekends_only
        assert any([campgrounds is not None, recreation_area is not None]) is True
        self.search_days = self._get_search_days()
        self.search_months = self._get_search_months()
        self.campgrounds: List[AvailableCampsite] = self._get_searchable_campgrounds()

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
            if isinstance(self._campground_object, list):
                returned_sites = list()
                for campground in self._campground_object:
                    facility = self.campsite_finder.find_campsites(campsite_id=campground)
                    campground_data, campground_facility = \
                        self.campsite_finder.process_facilities_responses(facility=facility)
                    self.campsite_finder._log_sorted_response(response_array=[campground_facility])
                    returned_sites.append(campground_facility)
                return returned_sites
            else:
                facility = self.campsite_finder.find_campsites(campsite_id=self._campground_object)
                campground_data, campground_facility = \
                    self.campsite_finder.process_facilities_responses(facility=facility)
                self.campsite_finder._log_sorted_response(response_array=[campground_facility])
                return [campground_facility]
        elif self._recreation_area_id is not None:
            processed_array = list()
            campground_array = self.campsite_finder.find_facilities_per_recreation_area(
                rec_area_id=self._recreation_area_id)
            for campground in campground_array:
                campground_data, campground_facility = \
                    self.campsite_finder.process_facilities_responses(facility=campground)
                processed_array.append(campground_facility)
            return processed_array

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
            generated_dates = {
                window.start_date.replace(hour=0, minute=0, second=0,
                                          microsecond=0) + timedelta(days=x) for x in
                range(0, (window.end_date - window.start_date).days + 1)}
            search_days.update(generated_dates)

        if self.weekends_only is True:
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

    def search_campsite_months(self) -> List[AvailableCampsite]:
        """
        Perform the Search and Return All Monthly Availabilities

        Returns
        -------
        List[AvailableCampsite]
        """
        found_campsites = list()
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
                    sleep(2)
        return found_campsites

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
        logger.info(f"{get_emoji(matching_campgrounds) * 5}  {len(matching_campgrounds)} "
                    "Campsites Matching Search Preferences")
        return matching_campgrounds

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
                    logger.info(f"\t⛰️ {' 🏕 '.join(location_tuple)}: ⛺️ "
                                f"{len(campground_availability)} sites")
                    if verbose is True:
                        for _, row in campground_availability.iterrows():
                            logger.info(f"\t\t🔗 {row['booking_url']}")
        return availability_df
