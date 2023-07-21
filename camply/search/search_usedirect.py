"""
Search Implementation: Reserve California
"""

import logging
import sys
from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any, Dict, List, Optional, Type, Union

from dateutil.relativedelta import relativedelta

from camply.containers import AvailableCampsite, RecreationArea, SearchWindow
from camply.containers.data_containers import ListedCampsite
from camply.providers.usedirect.variations import (
    AlabamaStateParks,
    ArizonaStateParks,
    FairfaxCountyParks,
    FloridaStateParks,
    MaricopaCountyParks,
    MinnesotaStateParks,
    MissouriStateParks,
    NorthernTerritory,
    OhioStateParks,
    OregonMetro,
    ReserveCalifornia,
    VirginiaStateParks,
)
from camply.search.base_search import BaseCampingSearch
from camply.utils import logging_utils, make_list
from camply.utils.logging_utils import format_log_string, log_sorted_response

logger = logging.getLogger(__name__)


class SearchUseDirect(BaseCampingSearch, ABC):
    """
    Searches on UseDirect.com for Campsites
    """

    @property
    @abstractmethod
    def provider_class(self) -> Type[BaseCampingSearch]:
        """
        Provider Class to be used for Search
        """
        pass

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
            **kwargs,
        )
        self._recreation_area_ids: List[int] = make_list(recreation_area, coerce=int)
        self._campground_ids: List[int] = make_list(campgrounds, coerce=int)
        campsites = make_list(kwargs.get("campsites", []), coerce=int) or []
        if len(campsites) > 0:
            self.campsite_finder.validate_campsites(
                campsites=campsites, facility_ids=self._campground_ids
            )
        try:
            assert any(
                [
                    self._campground_ids not in (None, []),
                    self._recreation_area_ids not in (None, []),
                ]
            )
        except AssertionError:
            logger.error(
                f"You must provide a Campground ID or a Recreation Area ID to {self.provider_class.__name__}"
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
            logger.warning(
                "%s Doesn't Support Equipment, yet 🙂", self.provider_class.__name__
            )

    def get_all_campsites(self, **kwargs: Dict[str, Any]) -> List[AvailableCampsite]:
        """
        Retrieve All Campsites from the UseDirect API

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
        Return the UseDirect Recreation Areas
        """
        rec_areas = cls.provider_class().search_for_recreation_areas(
            query=search_string, state=kwargs.get("state")
        )
        logger.info(f"{len(rec_areas)} Matching Recreation Areas Found")
        log_sorted_response(rec_areas)
        return rec_areas

    def list_campsite_units(self) -> List[ListedCampsite]:
        """
        List Campsite Units

        Returns
        -------
        List[ListedCampsite]
        """
        if not self.campsite_finder.usedirect_campsites:
            self.campsite_finder.get_campsite_metadata(facility_ids=self.campground_ids)
        sorted_campsites = sorted(
            self.campsite_finder.usedirect_campsites.values(),
            key=lambda x: x.OrderByRaw,
        )
        logged_campsites = [
            ListedCampsite(id=item.UnitId, name=item.Name, facility_id=item.FacilityId)
            for item in sorted_campsites
        ]
        self.log_listed_campsites(
            campsites=logged_campsites,
            facilities=self.campgrounds,
        )
        return logged_campsites


class SearchReserveCalifornia(SearchUseDirect):
    """
    Search ReserveCalifornia
    """

    provider_class = ReserveCalifornia


class SearchNorthernTerritory(SearchUseDirect):
    """
    Searches the Australian Northern Territory for Campsites
    """

    provider_class = NorthernTerritory


class SearchFloridaStateParks(SearchUseDirect):
    """
    Searches on FloridaStateParks.org for Campsites
    """

    provider_class = FloridaStateParks


class SearchOregonMetro(SearchUseDirect):
    """
    Searches on OregonMetro.gov for Campsites (Portland Metro)
    """

    provider_class = OregonMetro


class SearchOhioStateParks(SearchUseDirect):
    """
    Searches on ReserveOhio.com for Campsites
    """

    provider_class = OhioStateParks


class SearchVirginiaStateParks(SearchUseDirect):
    """
    Searches on ReserveVAParks.com for Campsites
    """

    provider_class = VirginiaStateParks


class SearchArizonaStateParks(SearchUseDirect):
    """
    Searches on AZStateParks.com for Campsites
    """

    provider_class = ArizonaStateParks


class SearchMaricopaCountyParks(SearchUseDirect):
    """
    Searches on MaricopaCountyParks.org for Campsites (Arizona)
    """

    provider_class = MaricopaCountyParks


class SearchMissouriStateParks(SearchUseDirect):
    """
    Searches on icampmo1.usedirect.com for Campsites
    """

    provider_class = MissouriStateParks


class SearchAlabamaStateParks(SearchUseDirect):
    """
    Searches on ReserveAlaPark.com for Campsites
    """

    provider_class = AlabamaStateParks


class SearchFairfaxCountyParks(SearchUseDirect):
    """
    Searches on fairfax.usedirect.com for Campsites (Virginia)
    """

    provider_class = FairfaxCountyParks


class SearchMinnesotaStateParks(SearchUseDirect):
    """
    Searches on ReserveMN.usedirect.com for Campsites
    """

    provider_class = MinnesotaStateParks
