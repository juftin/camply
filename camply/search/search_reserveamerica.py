"""
ReserveAmerica search utilities
"""

import logging
from typing import Any, Dict, List, Optional, Union

from camply.containers import (
    AvailableCampsite,
    SearchWindow,
)
from camply.providers import ReserveAmerica
from camply.search.base_search import BaseCampingSearch

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
        assert campgrounds not in [[], None]
        self.campgrounds = campgrounds
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
        logger.info("Searching across %d campgrounds", len(self.campgrounds))

        # TODO: Implement the logic to retrieve all campsites from ReserveAmerica
        return []

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
