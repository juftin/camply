"""
Yellowstone Lodging Web Searching Utilities
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional, Set, Union

import pandas as pd

from camply.config import YellowstoneConfig
from camply.containers import AvailableCampsite, RecreationArea, SearchWindow
from camply.exceptions import SearchError
from camply.providers import YellowstoneLodging
from camply.search.base_search import BaseCampingSearch
from camply.utils import make_list
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)


class SearchYellowstone(BaseCampingSearch):
    """
    Searches on YellowstoneNationalParkLodges.com for Campsites
    """

    recreation_area = YellowstoneLodging.recreation_area
    provider_class = YellowstoneLodging

    # noinspection PyUnusedLocal
    def __init__(
        self,
        search_window: Union[SearchWindow, List[SearchWindow]],
        weekends_only: bool = False,
        campgrounds: Optional[Union[List[str], str]] = None,
        nights: int = 1,
        offline_search: bool = False,
        offline_search_path: Optional[str] = None,
        **kwargs,
    ) -> None:
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
        nights: int
            minimum number of consecutive nights to search per campsite,defaults to 1
        offline_search: bool
            When set to True, the campsite search will both save the results of the
            campsites it's found, but also load those campsites before beginning a
            search for other campsites.
        offline_search_path: Optional[str]
            When offline search is set to True, this is the name of the file to be saved/loaded.
            When not specified, the filename will default to `camply_campsites.json`
        """
        super().__init__(
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
            offline_search=offline_search,
            offline_search_path=offline_search_path,
        )
        self.campgrounds = make_list(campgrounds)

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Search for all matching campsites in Yellowstone.

        Returns
        -------
        List[AvailableCampsite]
        """
        all_campsites = []
        searchable_campgrounds = self._get_searchable_campgrounds()
        this_month = datetime.now().date().replace(day=1)
        for month in self.search_months:
            if month >= this_month:
                all_campsites += self.campsite_finder.get_monthly_campsites(
                    month=month, nights=None if self.nights == 1 else self.nights
                )
        matching_campsites = self._filter_campsites_to_campgrounds(
            campsites=all_campsites, searchable_campgrounds=searchable_campgrounds
        )
        campsite_df = self.campsites_to_df(campsites=matching_campsites)
        campsite_df_validated = self._filter_date_overlap(campsites=campsite_df)
        time_window_end = max(self.search_days) + timedelta(days=1)
        compiled_campsite_df = campsite_df_validated[
            campsite_df_validated.booking_end_date <= pd.Timestamp(time_window_end)
        ]
        compiled_campsites = self.df_to_campsites(campsite_df=compiled_campsite_df)
        return compiled_campsites

    def _get_searchable_campgrounds(self) -> Optional[Set[str]]:
        """
        Return the Campgrounds for the Camping Search

        Returns
        -------
        Optional[Set[str]]
        """
        if self.campgrounds in [None, []]:
            return None
        supported_campsites = set(YellowstoneConfig.YELLOWSTONE_CAMPGROUNDS.keys())
        selected_campsites = set(self.campgrounds)
        searchable_campgrounds = supported_campsites.intersection(selected_campsites)
        if len(searchable_campgrounds) == 0:
            campground_ids = [
                f"`{key}` ({value})"
                for key, value in YellowstoneConfig.YELLOWSTONE_CAMPGROUNDS.items()
            ]
            error_message = (
                "You must supply a YellowstoneNationalParkLodges supported "
                "campground ID. Current supported Campground IDs: "
                f"{', '.join(campground_ids)}"
            )
            logger.error(error_message)
            raise SearchError(error_message)
        logger.info(f"{len(searchable_campgrounds)} Matching Campgrounds Found")
        for campground in searchable_campgrounds:
            logger.info(
                f"⛰  {YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_FORMAL_NAME} "
                f"(#{YellowstoneConfig.YELLOWSTONE_RECREATION_AREA_ID}) - 🏕  "
                f"{YellowstoneConfig.YELLOWSTONE_CAMPGROUNDS[campground]} ({campground})"
            )
        return searchable_campgrounds

    def _filter_campsites_to_campgrounds(
        self, campsites: List[AvailableCampsite], searchable_campgrounds: Set[str]
    ) -> List[AvailableCampsite]:
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
        if self.campgrounds in [None, []]:
            return campsites
        matching_campsites = [
            campsite
            for campsite in campsites
            if campsite.facility_id in searchable_campgrounds
        ]
        return matching_campsites

    @classmethod
    def find_recreation_areas(cls, **kwargs) -> List[RecreationArea]:
        """
        Return the Yellowstone Recreation Area Object
        """
        log_sorted_response([cls.recreation_area])
        return [cls.recreation_area]
