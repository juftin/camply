"""
ReserveAmerica search utilities
"""

import logging
from typing import Any, Dict, List, Optional, Union

from camply.containers import (
    AvailableCampsite,
    SearchWindow,
)
from camply.exceptions import SearchError
from camply.providers import ReserveAmerica
from camply.search.base_search import BaseCampingSearch
from camply.utils import logging_utils
from camply.utils.general_utils import make_list
from camply.utils.logging_utils import format_log_string

logger = logging.getLogger(__name__)


class SearchReserveAmerica(BaseCampingSearch):
    """
    Searches on ReserveAmerica.com for Campsites
    """

    provider_class = ReserveAmerica
    list_campsites_supported: bool = False

    def __init__(
        self,
        search_window: Union[SearchWindow, List[SearchWindow]],
        campgrounds: Optional[Union[List[int], int]] = None,
        campsites: Optional[Union[List[int], int]] = None,
        weekends_only: bool = False,
        nights: int = 1,
        offline_search_path: Optional[str] = None,
        **kwargs,
    ) -> None:
        """
        Initialize with Search Parameters

        Parameters
        ----------
        search_window: Union[SearchWindow, List[SearchWindow]]
            Search Window tuple containing start date and End Date
        campgrounds: Optional[Union[List[int], int]]
            Park ID or List of Park IDs
        campsites: Optional[Union[List[int], int]]
            Site ID or List of Site IDs
        weekends_only: bool
            Whether to only search for Camping availabilities on the weekends (Friday /
            Saturday nights)
            # TODO: Implement weekends_only
        nights: int
            minimum number of consecutive nights to search per campsite,defaults to 1
            # TODO: Implement number of nights
        equipment: Optional[List[Tuple[str, Optional[int]]]]
            List of tuples containing equipment name and optional quantity
            # TODO: Document values of equipment
        offline_search: bool
            When set to True, the campsite search will both save the results of the
            campsites it's found, but also load those campsites before beginning a
            search for other campsites.
        offline_search_path: Optional[str]
            When offline search is set to True, this is the name of the file to be saved/loaded.
            When not specified, the filename will default to `camply_campsites.json`

        Returns
        -------
        None
        """
        super(SearchReserveAmerica, self).__init__(
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
            # offline_search=offline_search,
            # offline_search_path=offline_search_path,
            **kwargs,
        )
        try:
            assert campgrounds not in [[], None]
        except AssertionError:
            raise ValueError(
                f"You must provide a Campground ID to {self.provider_class.__name__}"
            ) from None

        self._campground_ids: List[int] = make_list(campgrounds)
        self.campgrounds = self.campsite_finder.find_campgrounds(
            park_ids=self._campground_ids,
        )
        self.campsites = make_list(campsites)
        # TODO: Validate campsites requested are within campgrounds requested

    def get_all_campsites(self, **kwargs: Dict[str, Any]) -> List[AvailableCampsite]:
        """
        Retrieve All Available Campsites from ReserveAmerica

        Parameters
        ----------
        kwargs: Dict[str, Any]
        #TODO: Document kwargs

        Returns
        -------
        List[AvailableCampsite]
        """
        if len(self.campgrounds) == 0:
            error_message = "No campgrounds found to search"
            logger.error(error_message)
            raise SearchError(error_message)

        logger.info("Searching across %d campgrounds", len(self.campgrounds))

        for campground in self.campgrounds:
            log_str = format_log_string(campground)
            logger.info("    %s", log_str)

        campsites_found: List[AvailableCampsite] = []

        for search_window in self.search_window:
            for campground in self.campgrounds:
                start_date = search_window.start_date
                end_date = search_window.end_date

                logger.info(
                    f"Searching {campground.facility_name} "
                    f"({campground.facility_id}) for availability: from "
                    f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
                )

                campsites = self.campsite_finder.get_campsites(
                    park_id=campground.facility_id,
                    start_date=start_date,
                    end_date=end_date,
                    **kwargs,
                )

                logger.info(
                    f"\t{logging_utils.get_emoji(campsites)}\t"
                    f"{len(campsites)} campsites found for {campground.facility_name} "
                    f"from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}"
                )

                if self.campsites not in [None, []]:
                    campsites = [
                        campsite_obj
                        for campsite_obj in campsites
                        if int(campsite_obj.campsite_id) in self.campsites
                    ]
                campsites_found += campsites

        campsite_df = self.campsites_to_df(campsites=campsites_found)
        campsite_df_validated = self._filter_date_overlap(campsites=campsite_df)
        compiled_campsite_df = self._consolidate_campsites(
            campsite_df=campsite_df_validated, nights=self.nights
        )
        compiled_campsites = self.df_to_campsites(campsite_df=compiled_campsite_df)

        return compiled_campsites

    def list_campsite_units(self):
        """
        List Campsite Units

        Retruns
        -------
        List[AvailableCampsite]
        """

        logger.info("Listing campsite units")

        # TODO: Implement the logic to list campsite units from ReserveAmerica
        return super().list_campsite_units()
