"""
Geo-based multi-provider campsite search
"""

import logging
import sys
from typing import Dict, List, Optional, Tuple, Type, Union

from camply.containers import AvailableCampsite, CampgroundFacility, SearchWindow
from camply.exceptions import CamplyError
from camply.providers import RecreationDotGov
from camply.providers.xanterra.yellowstone_lodging import Yellowstone
from camply.search.base_search import BaseCampingSearch
from camply.search.search_recreationdotgov import SearchRecreationDotGov
from camply.search.search_usedirect import (
    SearchAlabamaStateParks,
    SearchArizonaStateParks,
    SearchFairfaxCountyParks,
    SearchFloridaStateParks,
    SearchMaricopaCountyParks,
    SearchMinnesotaStateParks,
    SearchMissouriStateParks,
    SearchNorthernTerritory,
    SearchOhioStateParks,
    SearchOregonMetro,
    SearchReserveCalifornia,
    SearchVirginiaStateParks,
)
from camply.search.search_yellowstone import SearchYellowstone
from camply.utils.geo_utils import geocode_location, haversine_distance_miles

logger = logging.getLogger(__name__)

# (latitude, longitude) of Yellowstone's geographic center
_YELLOWSTONE_CENTER: Tuple[float, float] = (44.4280, -110.5885)

# UseDirect search classes eligible for geo-search (all have lat/lon in cached metadata)
_USEDIRECT_SEARCH_CLASSES = [
    SearchReserveCalifornia,
    SearchAlabamaStateParks,
    SearchArizonaStateParks,
    SearchFloridaStateParks,
    SearchMinnesotaStateParks,
    SearchMissouriStateParks,
    SearchOhioStateParks,
    SearchOregonMetro,
    SearchVirginiaStateParks,
    SearchFairfaxCountyParks,
    SearchMaricopaCountyParks,
    SearchNorthernTerritory,
]


class SearchGeo(BaseCampingSearch):
    """
    Multi-provider campsite search by distance from a geographic point.

    Fans out across RecreationDotGov, all UseDirect providers, and Yellowstone.
    """

    provider_class = RecreationDotGov

    def __init__(
        self,
        search_window: Union[SearchWindow, List[SearchWindow]],
        latitude: float,
        longitude: float,
        radius_miles: float,
        provider_filter: Optional[str] = None,
        weekends_only: bool = False,
        nights: int = 1,
        excluded_campsite_types: Optional[List[str]] = None,
        **kwargs,
    ) -> None:
        super().__init__(
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
            excluded_campsite_types=excluded_campsite_types,
            **kwargs,
        )
        self.latitude = latitude
        self.longitude = longitude
        self.radius_miles = radius_miles
        self._sub_searches: List[BaseCampingSearch] = self._build_sub_searches(
            search_window=search_window,
            provider_filter=provider_filter,
            weekends_only=weekends_only,
            nights=nights,
            **kwargs,
        )
        self.campgrounds = [cg for s in self._sub_searches for cg in s.campgrounds]
        if not self.campgrounds:
            logger.error(
                f"No campgrounds found within {radius_miles} miles of "
                f"({latitude:.4f}, {longitude:.4f})"
            )
            sys.exit(1)

    def _build_sub_searches(
        self,
        search_window: Union[SearchWindow, List[SearchWindow]],
        provider_filter: Optional[str],
        weekends_only: bool,
        nights: int,
        **kwargs,
    ) -> List[BaseCampingSearch]:
        """Discover campgrounds within radius from each applicable provider."""
        sub_searches: List[BaseCampingSearch] = []
        shared = dict(
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
        )

        # RecreationDotGov
        if provider_filter is None or provider_filter == RecreationDotGov.__name__:
            sub_searches += self._build_recdotgov_search(shared, **kwargs)

        # UseDirect variants
        for search_cls in _USEDIRECT_SEARCH_CLASSES:
            provider_name = search_cls.provider_class.__name__
            if provider_filter is None or provider_filter == provider_name:
                sub_searches += self._build_usedirect_search(search_cls, shared, **kwargs)

        # Yellowstone
        if provider_filter is None or provider_filter == Yellowstone.__name__:
            sub_searches += self._build_yellowstone_search(shared, **kwargs)

        return sub_searches

    def _build_recdotgov_search(
        self, shared: dict, **kwargs
    ) -> List[SearchRecreationDotGov]:
        provider = RecreationDotGov()
        campgrounds = provider.find_campgrounds(
            latitude=self.latitude,
            longitude=self.longitude,
            radius=self.radius_miles,
        )
        if not campgrounds:
            return []
        campground_ids = [int(cg.facility_id) for cg in campgrounds]
        logger.info(
            f"RecreationDotGov: {len(campground_ids)} campgrounds within "
            f"{self.radius_miles} miles"
        )
        return [
            SearchRecreationDotGov(
                campgrounds=campground_ids,
                **shared,
                **kwargs,
            )
        ]

    def _build_usedirect_search(
        self,
        search_cls: Type[BaseCampingSearch],
        shared: dict,
        **kwargs,
    ) -> List[BaseCampingSearch]:
        provider = search_cls.provider_class()
        try:
            provider.refresh_metadata()
        except Exception as exc:
            logger.warning(
                f"{search_cls.provider_class.__name__}: skipping — metadata unavailable: {exc}"
            )
            return []
        in_radius = [
            int(cg.facility_id)
            for cg in provider.usedirect_campgrounds.values()
            if cg.coordinates is not None
            and haversine_distance_miles(
                self.latitude, self.longitude, cg.coordinates[0], cg.coordinates[1]
            )
            <= self.radius_miles
        ]
        if not in_radius:
            return []
        logger.info(
            f"{search_cls.provider_class.__name__}: {len(in_radius)} campgrounds "
            f"within {self.radius_miles} miles"
        )
        return [
            search_cls(
                recreation_area=[],
                campgrounds=in_radius,
                **shared,
                **kwargs,
            )
        ]

    def _build_yellowstone_search(
        self, shared: dict, **kwargs
    ) -> List[SearchYellowstone]:
        dist = haversine_distance_miles(
            self.latitude,
            self.longitude,
            _YELLOWSTONE_CENTER[0],
            _YELLOWSTONE_CENTER[1],
        )
        if dist > self.radius_miles:
            return []
        logger.info(
            f"Yellowstone: park center is {dist:.1f} miles away — including in search"
        )
        return [SearchYellowstone(**shared, **kwargs)]

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """Aggregate available campsites from all sub-searches."""
        results: List[AvailableCampsite] = []
        for sub_search in self._sub_searches:
            results.extend(sub_search.get_all_campsites())
        return results

    def list_campsite_units(self) -> None:
        raise NotImplementedError
