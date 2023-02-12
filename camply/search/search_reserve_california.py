"""
Search Implementation: Reserve California
"""

import logging
import sys
from datetime import timedelta
from typing import Any, Dict, List, Optional, Union

from dateutil.relativedelta import relativedelta

from camply.containers import AvailableCampsite, RecreationArea, SearchWindow
from camply.providers.reserve_california import ReserveCalifornia
from camply.search.base_search import BaseCampingSearch
from camply.utils import logging_utils, make_list
from camply.utils.logging_utils import format_log_string, log_sorted_response

logger = logging.getLogger(__name__)


class SearchReserveCalifornia(BaseCampingSearch):
    """
    Searches on ReserveCalifornia.com for Campsites
    """

    provider_class = ReserveCalifornia

    def __init__(
        self,
        search_window: Union[SearchWindow, List[SearchWindow]],
        recreation_area: List[int],
        weekends_only: bool = False,
        campgrounds: Optional[Union[List[str], str]] = None,
        nights: int = 1,
        **kwargs,
    ) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        recreation_area: List[int]
            The IDs of the recreation area to be searched.
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
        campgrounds: Union[List[int], int]
            Campground ID or List of Campground IDs
        nights: int
            minimum number of consecutive nights to search per campsite,defaults to 1
        """
        super().__init__(
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
        )
        self.campsite_finder: ReserveCalifornia
        self._recreation_area_ids: List[int] = make_list(recreation_area)
        self._campground_ids: List[int] = make_list(campgrounds)
        try:
            assert any([self._campground_ids != [], self._recreation_area_ids != []])
        except AssertionError:
            logger.error(
                "You must provide a Campground ID or a Recreation Area ID to ReserveCalifornia"
            )
            sys.exit(1)
        if self._campground_ids:
            self.campgrounds = self.campsite_finder.find_campgrounds(
                campground_id=self._campground_ids,
                verbose=False,
            )
        else:
            self.campgrounds = self.campsite_finder.find_campgrounds(
                rec_area_id=self._recreation_area_ids,
                verbose=False,
            )
        self.campground_ids = [item.facility_id for item in self.campgrounds]
        if len(self.campground_ids) == 0:
            logger.error("No Campsites Found Matching Your Search Criteria")
            sys.exit(1)
        if kwargs.get("equipment", ()):
            logger.warning("ReserveCalifornia Doesn't Support Equipment, yet 🙂")

    def get_all_campsites(self, **kwargs: Dict[str, Any]) -> List[AvailableCampsite]:
        """
        Retrieve All Campsites from the ReserveCalifornia API

        Parameters
        ----------
        kwargs: Dict[str, Any]

        Returns
        -------
        List[AvailableCampsite]
        """
        logger.info(f"Searching across {len(self.campgrounds)} campgrounds")
        for campground in self.campgrounds:
            log_str = format_log_string(campground)
            logger.info("    %s", log_str)
        campsites_found: List[AvailableCampsite] = []
        for month in self.search_months:
            for campground in self.campgrounds:
                logger.info(
                    f"Searching {campground.facility_name}, {campground.recreation_area} "
                    f"({campground.facility_id}) for availability: "
                    f"{month.strftime('%B, %Y')}"
                )
                end_date = month + relativedelta(months=1) - timedelta(days=1)
                campsites = self.campsite_finder.get_campsites(
                    campground_id=campground.facility_id,
                    start_date=month,
                    end_date=end_date,
                )
                logger.info(
                    f"\t{logging_utils.get_emoji(campsites)}\t"
                    f"{len(campsites)} total sites found in month of "
                    f"{month.strftime('%B')}"
                )
                campsites_found += campsites
        campsite_df = self.campsites_to_df(campsites=campsites_found)
        campsite_df_validated = self._filter_date_overlap(campsites=campsite_df)
        consolidated_campsites = self._consolidate_campsites(
            campsite_df=campsite_df_validated, nights=self.nights
        )
        compiled_campsites = self.df_to_campsites(campsite_df=consolidated_campsites)
        return compiled_campsites

    @classmethod
    def find_recreation_areas(
        cls, search_string: str, **kwargs
    ) -> List[RecreationArea]:
        """
        Return the ReserveCalifornia Recreation Areas
        """
        rec_areas = cls.provider_class().search_for_recreation_areas(
            query=search_string, state=kwargs.get("state", "CA")
        )
        logger.info(f"{len(rec_areas)} Matching Recreation Areas Found")
        log_sorted_response(rec_areas)
        return rec_areas
