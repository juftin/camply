"""
Going To Camp API search utilities
"""
import logging
from datetime import datetime, time, timedelta
from typing import List, Optional, Set, Tuple, Union

import pandas as pd

from camply.config import YellowstoneConfig
from camply.containers import AvailableCampsite, CampgroundFacility, SearchWindow
from camply.providers import GoingToCampProvider, RecreationDotGov
from camply.providers.going_to_camp.going_to_camp_provider import RECREATION_AREAS
from camply.search.base_search import BaseCampingSearch, SearchError
from camply.utils import make_list
from camply.utils.logging_utils import log_sorted_response

logger = logging.getLogger(__name__)


class SearchGoingToCamp(BaseCampingSearch):
    """
    Camping Search Object
    """

    # noinspection PyUnusedLocal
    def __init__(
        self,
        search_window: Union[SearchWindow, List[SearchWindow]],
        recreation_area: Optional[Union[List[int], int]] = None,
        campsites: Optional[Union[List[int], int]] = None,
        weekends_only: bool = False,
        campgrounds: Optional[Union[List[str], str]] = None,
        equipment: Optional[List[Tuple[str, Optional[int]]]] = None,
        nights: int = 1,
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
        """
        self.provider = GoingToCampProvider
        super(SearchGoingToCamp, self).__init__(
            provider=GoingToCampProvider(),
            search_window=search_window,
            weekends_only=weekends_only,
            nights=nights,
        )

        self._recreation_area_id = make_list(recreation_area)
        self._campground_object = campgrounds
        self.weekends_only = weekends_only
        assert (
            any(
                [
                    campsites not in [[], None],
                    campgrounds not in [[], None],
                    recreation_area is not None,
                ]
            )
            is True
        )
        self.campsites = make_list(campsites)
        self.campgrounds = self._get_searchable_campgrounds()
        self.equipment = self._get_equipment_category(equipment)

    def _get_equipment_category(self, equipment: List[Tuple[str, int]]):
        our_equipment_name, our_equipment_length = equipment[0]
        our_equipment_length = int(our_equipment_length)  # TODO: gross
        equipment_categories = self.campsite_finder.list_equipment_categories(
            self._recreation_area_id[0]
        )
        matching_category_id = None
        for eq_name, category in equipment_categories.items():
            category_id = category["id"]
            if eq_name.find(our_equipment_name) > 0:
                if our_equipment_length == 0:
                    return category_id
                if (
                    our_equipment_length > 0
                    and our_equipment_length <= category["max_size"]
                ):
                    return category_id

        logger.error("No equipment category found that matches your equipment")
        exit(1)

    def get_all_campsites(self) -> List[AvailableCampsite]:
        """
        Search for all campsites matching search criteria

        Returns
        -------
        List[AvailableCampsite]
        """
        for campground in self.campgrounds:
            sites = self.campsite_finder.list_site_availability(
                campground,
                self.search_window[0].start_date,
                self.search_window[0].end_date,
                self.equipment,
            )
            available_sites = []
            for site in sites:
                site_details = self.campsite_finder.get_site_details(
                    self._recreation_area_id[0], campground.facility_id
                )

                nights = (
                    self.search_window[0].end_date - self.search_window[0].start_date
                ).days
                start_dt = datetime.combine(self.search_window[0].start_date, time.min)
                end_dt = datetime.combine(self.search_window[0].end_date, time.min)
                rec_area = self.campsite_finder.rec_area_lookup(
                    rec_area_id=self._recreation_area_id[0]
                )
                booking_url = self.campsite_finder.get_reservation_link(
                    party_size=1,
                    start_date=self.search_window[0].start_date,
                    end_date=self.search_window[0].end_date,
                    camp_area=campground,
                    resource_location_id=campground.facility_id,
                    equipment_id=-32768,  # TODO don't hard-code/name this value
                    sub_equipment_id=self.equipment,
                )

                available_sites.append(
                    AvailableCampsite(
                        campsite_id=site_details["resourceId"],
                        campsite_site_name=site_details["localizedValues"][0]["name"],
                        booking_date=start_dt,
                        booking_end_date=end_dt,
                        booking_nights=nights,
                        campsite_loop_name="Unknown",
                        campsite_type=site_details["site_attributes"]["Service Type"],
                        campsite_occupancy=(
                            site_details["minCapacity"],
                            site_details["maxCapacity"],
                        ),
                        campsite_use_type="N/A",
                        availability_status="Available",
                        recreation_area=rec_area.recreation_area,
                        recreation_area_id=self._recreation_area_id[0],
                        facility_name=campground.facility_name,
                        facility_id=campground.facility_id,
                        booking_url=booking_url,
                    )
                )

        return available_sites

    def _get_searchable_campgrounds(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search

        Returns
        -------
        searchable_campgrounds: List[CampgroundFacility]
            List of searchable campgrounds
        """
        if self._campground_object in [(), [], None] or self._recreation_area_id in [
            (),
            [],
            None,
        ]:
            logger.error(
                "You must provide a Campground and Recreation Area ID with this provider"
            )
            exit(1)

        if self.campsites not in [(), [], None]:
            self.campsites = [int(campsite_id) for campsite_id in self.campsites]
            return self._get_campgrounds_by_campsite_id()

        return self._get_campgrounds_by_recreation_area_id()

    def _get_campgrounds_by_recreation_area_id(self) -> List[CampgroundFacility]:
        """
        Return a List of Campgrounds to search when provided with Recreation Area IDs

        Returns
        -------
        campgrounds: List[CampgroundFacility]
        """
        if not self._campground_object in [(), [], None]:
            return self._get_campgrounds_by_campground_id()

        return self.campsite_finder.find_campgrounds(
            rec_area_id=self._recreation_area_id
        )

    def _get_campgrounds_by_campground_id(self) -> List[CampgroundFacility]:
        facilities = self.campsite_finder.find_campgrounds(
            rec_area_id=self._recreation_area_id
        )
        filtered_facilities = []
        for facility in facilities:
            if str(facility.facility_id) in self._campground_object:
                filtered_facilities.append(facility)

        return filtered_facilities
